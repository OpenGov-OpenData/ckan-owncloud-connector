import json
import os
import shutil

import sys

import owncloud
import urllib3
import ckan_file_upload
import zipfile
import config
import time

urllib3.disable_warnings()


class TestFileAccess(object):
    def __init__(self):
        self.client = owncloud.Client(config.Config['owncloud_url'], dav_endpoint_version=0)
        self.client.login(config.Config['owncloud_login'], config.Config['owncloud_password'])

    def test_upload_directory(self, ownclouddirectory, localdirectory):
        self.client.put_directory(ownclouddirectory + '/', localdirectory + '/')

    def test_download_dir(self, ownclouddirectory, localdirectory):
        self.client.get_directory_as_zip(ownclouddirectory, localdirectory)

    def delete_file(self, ownclouddirectory, filename):
        self.client.delete(ownclouddirectory + '/' + filename)

    def get_file_listing(self, ownclouddirectory):
        self.client.list(ownclouddirectory)

    def test_get_file_listing(self, ownclouddirectory):
        return self.client.list(ownclouddirectory)


def zip_file_extractor(zip_file_path, destination_file_path):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(destination_file_path)
    zip_ref.close()
    os.remove(zip_file_path)


def file_upload_fail(zip_file, local_upload_directory, orginization, error_message):
    print(error_message + ' in ' + zip_file.name + '.  Upload failed')
    f = open(local_upload_directory + '/result.txt', 'w')
    f.write(error_message + ' in ' + zip_file.name + '.  Upload failed')
    f.close()
    shutil.make_archive(local_upload_directory, 'zip', local_upload_directory)
    ownCloudMethods.test_upload_directory(orginization + '/Failure', local_upload_directory)
    shutil.rmtree(local_upload_directory)


def file_upload_success(zip_file, local_upload_directory, orginization):
    print(zip_file.name + ' successfully uploaded')
    f = open(local_upload_directory + '/result.txt', 'w')
    f.write(zip_file.name + ' successfully uploaded')
    f.close()
    shutil.make_archive(local_upload_directory, 'zip', local_upload_directory)
    ownCloudMethods.test_upload_directory(orginization + '/Success', local_upload_directory)
    shutil.rmtree(local_upload_directory)


if __name__ == '__main__':
    ownCloudMethods = TestFileAccess()
    current_timestamp = (time.strftime('%Y%m%d%H%M%S'))
    localDownloadDirectory = config.Config['localDownloadDirectory'] + '/owncloud ' + current_timestamp

    try:
        OrganizationDirectories = ownCloudMethods.test_get_file_listing('')
    except:
        print('Problems with owncloud connection. Process aborting')
        sys.exit(0)

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
                try:
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'Incorrect number of files')
                except:
                    print('File re-upload failed.  Check ' + organization.name + ' Failure directory')
                continue
            elif not (os.path.isfile(localUploadDirectory + '/job.json')):
                try:
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No job.json file')
                except:
                    print('File re-upload failed.  Check Owncloud Failure directory')
                continue
            else:
                open(localUploadDirectory + '/job.json').read()
                with open(localUploadDirectory + '/job.json') as data_file:
                    data = json.load(data_file)

                resource_name = data['resource_name']
                resource_id = data['resource_id']
                package_id = data['package_id']
                base_url = data['ckan_url']
                file_name = data['file_name']
                api_key = data['ckan_api_key']
                file_type = data['file_type']
                resource_dict = {'package_id': data['package_id'], 'name': data['resource_name'], 'url': '',
                                 'description': data['resource_description'],
                                 }
                package_dict = {'id': data['package_id']}
                fullFilePath = localUploadDirectory + '/' + file_name

                if not api_key:
                    print('No API key.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No API key in job.json')
                if not resource_name:
                    print('No resource name.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No resource name in job.json')
                if not base_url:
                    print('No base url.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No base url in job.json')
                if not package_id:
                    print('No package ID.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No package id in job.json')
                if not file_type:
                    print('No file type.  Aborting')
                    file_upload_fail(zipFile, localUploadDirectory, organization.name, 'No file type in job.json')

                if not resource_id:
                    if ckan_file_upload.package_show(base_url, api_key, package_dict):
                        print localUploadDirectory + '/' + file_name
                        ckan_file_upload.upload_resource_create(base_url, api_key, resource_dict,
                                                                fullFilePath,
                                                                file_name)
                #     else:
                #         ckan_file_upload.upload_package()
                #         ckan_file_upload.upload_resource_create()

                else:
                    ckan_file_upload.upload_resource_patch(base_url, api_key, resource_dict,
                                                           fullFilePath, resource_name)
                shutil.rmtree(localUploadDirectory, ignore_errors=True)
            shutil.rmtree(localDownloadDirectory + '/' + organization.name, ignore_errors=True)
    shutil.rmtree(localDownloadDirectory, ignore_errors=True)
