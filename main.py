import json
import os
import shutil
import sys
import urllib3
import zipfile
from config import Config
import time

import src.owncloud as owncloud
import src.ckan_action as ckan_action

urllib3.disable_warnings()

owncloudConfig = Config.get('owncloud')

class TestFileAccess(object):
    def __init__(self):
        try:
            self.client = owncloud.Client(owncloudConfig.get('url'), dav_endpoint_version=0)
            self.client.login(owncloudConfig.get('username'), owncloudConfig.get('password'))
            self.root = owncloudConfig.get('root')
        except:
           print('Problems with owncloud connection. Process aborting')
           sys.exit(0)

    def test_upload_directory(self,
     ownclouddirectory, localdirectory):
        self.client.put_directory(self.root + '/' + ownclouddirectory + '/', localdirectory + '/')

    def test_download_dir(self, ownclouddirectory, localdirectory):
        self.client.get_directory_as_zip(self.root + '/' + ownclouddirectory, localdirectory)

    def delete_file(self, ownclouddirectory, filename):
        self.client.delete(self.root + '/' + ownclouddirectory + '/' + filename)

    def get_file_listing(self, ownclouddirectory):
        self.client.list(self.root + '/' + ownclouddirectory)

    def test_get_file_listing(self, ownclouddirectory):
        return self.client.list(self.root + '/' + ownclouddirectory)


def zip_file_extractor(zip_file_path, destination_file_path):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(destination_file_path)
    zip_ref.close()
    os.remove(zip_file_path)


def file_upload_fail(zip_file, local_upload_directory, organization_name, error_message):
    try:
        print(error_message + ' in ' + zip_file.name + '.  Upload failed')
        f = open(local_upload_directory + '/result.txt', 'w')
        f.write(error_message + ' in ' + zip_file.name + '.  Upload failed')
        f.close()
        shutil.make_archive(local_upload_directory, 'zip', local_upload_directory)
        ownCloudMethods.test_upload_directory(organization_name + '/Failure', local_upload_directory)
        shutil.rmtree(local_upload_directory)
    except:
        print('File re-upload failed.  Check ' + organization_name + ' Failure directory')


def file_upload_success(zip_file, local_upload_directory, organization_name):
    try:
        print(zip_file.name + ' successfully uploaded')
        f = open(local_upload_directory + '/result.txt', 'w')
        f.write(zip_file.name + ' successfully uploaded')
        f.close()
        shutil.make_archive(local_upload_directory, 'zip', local_upload_directory)
        ownCloudMethods.test_upload_directory(organization_name + '/Success', local_upload_directory)
        shutil.rmtree(local_upload_directory)
    except:
        print('File re-upload failed.  Check ' + organization_name + ' Success directory')


if __name__ == '__main__':
    ownCloudMethods = TestFileAccess()
    current_timestamp = (time.strftime('%Y%m%d%H%M%S'))
    localDownloadDirectory = owncloudConfig.get('download') + '/owncloud ' + current_timestamp

    OrganizationDirectories = ownCloudMethods.test_get_file_listing('')

    try:
        os.mkdir(localDownloadDirectory)
    except:
        print('Problem accessing local file directory.  Process aborting.')
        sys.exit(0)

    for organization in OrganizationDirectories:
        fileListing = ownCloudMethods.test_get_file_listing(organization.name)
        for file in fileListing[:]:
            if os.path.splitext(file.name)[1] != '.zip':
                fileListing.remove(file)
        if len(fileListing) == 0:
            print('No zip files in ' + organization.name + ' directory. Checking next directory.')
            continue

        ownCloudMethods.test_download_dir(organization.name,
                                          localDownloadDirectory + '/' + organization.name + '.zip')
        zip_file_extractor(localDownloadDirectory + '/' + organization.name + '.zip', localDownloadDirectory)

        for zipFile in fileListing:
            localUploadDirectory = localDownloadDirectory + '/result ' + os.path.splitext(zipFile.name)[0]
            os.mkdir(localUploadDirectory)
            zip_file_extractor(localDownloadDirectory + '/' + organization.name + '/' + zipFile.name,
                               localUploadDirectory)
            fileListing = os.listdir(localUploadDirectory)

            if len(fileListing) != 2:
                file_upload_fail(zipFile, localUploadDirectory, organization.name, 'Incorrect number of files')
                continue
            elif not (os.path.isfile(localUploadDirectory + '/job.json')):
                file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No job.json file')
                continue
            else:
                open(localUploadDirectory + '/job.json').read()
                with open(localUploadDirectory + '/job.json') as data_file:
                    data = json.load(data_file)

                resource_name = data.get('resource_name')
                resource_id = data.get('resource_id')
                package_id = data.get('package_id')
                base_url = data.get('ckan_url')
                file_name = data.get('file_name')
                api_key = data.get('ckan_api_key')
                file_type = data.get('file_type')
                resource_dict = {'package_id': data.get('package_id'), 'name': data.get('resource_name'), 'url': '',
                                 'description': data.get('resource_description'),
                                 }
                fullFilePath = localUploadDirectory + '/' + file_name

                if not api_key:
                    print('No API key.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No API key in job.json')
                    continue
                if not resource_name:
                    print('No resource name.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No resource name in job.json')
                    continue
                if not base_url:
                    print('No base url.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No base url in job.json')
                    continue
                if not package_id:
                    print('No package ID.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No package id in job.json')
                    continue
                if not file_type:
                    print('No file type.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No file type in job.json')
                    continue

                if resource_id:
                    try:
                        print(ckan_action.action('resource_patch', resource_dict, { 'name': resource_name, 'path': fullFilePath }))

                    except:
                        file_upload_fail(zipFile, localUploadDirectory, organization.name, 'CKAN file patch failed')

                elif package_id:
                    try:
                        print(ckan_action.action('resource_create', resource_dict, { 'name': file_name, 'path': fullFilePath }))
                    except:
                        file_upload_fail(zipFile, localUploadDirectory, organization.name,
                                         'CKAN file upload failed')
                else:
                    dataset_dict = {
                        'name': data.get('dataset_name'),
                        'notes': data.get('dataset_notes'),
                        'owner_org': data.get('owner_org')
                    }
                    try:
                        print(ckan_action.action('package_create', dataset_dict))
                        resource_dict['package_id'] = dataset_dict['name']
                        print(ckan_action.action('resousece_create', resource_dict, { 'name': file_name, 'path': fullFilePath }))
                    except:
                        file_upload_fail(zipFile, localUploadDirectory, organization.name,
                                         'CKAN file upload failed')
                shutil.rmtree(localUploadDirectory, ignore_errors=True)
            shutil.rmtree(localDownloadDirectory + '/' + organization.name, ignore_errors=True)
    shutil.rmtree(localDownloadDirectory, ignore_errors=True)
