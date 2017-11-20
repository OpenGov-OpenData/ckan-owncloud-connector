import json
import os
import shutil
import sys
import urllib3

from config import Config
import time

import src.ckan_action as ckan_action
import utils
from owncloud_methods import OwnCloudWrapper

urllib3.disable_warnings()

owncloudConfig = Config.get('owncloud')
ckanConfig = Config.get('ckan')

if __name__ == '__main__':

    owncloud = OwnCloudWrapper()
    current_timestamp = time.strftime('%Y%m%d%H%M%S')

    paths={
        'temp': './temp_' + current_timestamp
    }

    rootFileList = owncloud.get_file_listing(owncloudConfig.get('root'))

    try:
        os.mkdir(paths.get('temp'))
    except:
        print('Problem accessing local file directory.  Process aborting.')
        sys.exit(0)

    # this will loop through all directories in root directory for each organization
    #  and will look for zip files
    for rootDir in rootFileList:
        directory = rootDir.name;

        # get list of files in directory
        zipFileListing = owncloud.get_file_listing(directory)
        # keep only zip files
        for file in zipFileListing[:]:
            if os.path.splitext(file.name)[1] != '.zip':
                zipFileListing.remove(file)

        if len(zipFileListing) == 0:
            print('No zip files in %s directory. Checking next directory.'%(directory))
            continue

        owncloud.download_dir(directory, os.path.join(paths.get('temp'), directory + '.zip'))
        utils.zip_file_extractor(os.path.join(paths.get('temp'), directory + '.zip'), paths.get('temp'))

        for zipFile in zipFileListing:
            localUploadDirectory = os.path.join(paths.get('temp'), 'result_' + os.path.splitext(zipFile.name)[0])
            os.mkdir(localUploadDirectory)
            utils.zip_file_extractor(os.path.join(paths.get('temp'), directory, zipFile.name), localUploadDirectory)
            zipFileContents = os.listdir(localUploadDirectory)

            if len(zipFileContents) != 2:
                utils.file_upload_fail(zipFile, localUploadDirectory, directory, 'Incorrect number of files')
                continue
            if not (os.path.isfile(os.path.join(localUploadDirectory, 'job.json'))):
                utils.file_upload_fail(zipFile, localUploadDirectory, directory, 'No job.json file')
                continue

            with open(os.path.join(localUploadDirectory, 'job.json')) as data_file:
                data = json.load(data_file)

            fullFilePath = os.path.join(localUploadDirectory, data.get('file_name'))
            # Verify all required CKAN fields are present
            required_items = ['resource_name', 'package_id', 'file_type']
            for item in required_items:
                if not item in data:
                    message = 'No %s in job.json'%(item)
                    print '%s. Aborting' % message
                    utils.file_upload_fail(zipFile, localUploadDirectory, directory, message)
                    continue

            # Call CKAN API
            try:
                resource_dict = {
                    'package_id': data.get('package_id'),
                    'name': data.get('resource_name'),
                    'url': '',
                    'description': data.get('resource_description'),
                    'id': data.get('resource_id'),
                    'format': data.get('file_type')
                }
                # Update resource if resource_id provided
                if data.get('resource_id'):
                    response = ckan_action.action('resource_patch', resource_dict, {'name': data.get('resource_name'), 'path': fullFilePath})
                    print(response)
                # Create new resource if only package id provided
                elif data.get('package_id'):
                    response = ckan_action.action('resource_create', resource_dict, {'name': data.get('file_name'), 'path': fullFilePath})
                    print(response)
                # Create new package and resource if neither of resource_id, package_id provided
                else:
                    dataset_dict = {
                        'title': data.get('dataset_title'),
                        'notes': data.get('dataset_notes'),
                        'owner_org': data.get('owner_org')
                    }
                    # Create new package
                    response = ckan_action.action('package_create', dataset_dict)
                    print(response)
                    resource_dict['package_id'] = response.get('result').get('name')
                    response = ckan_action.action('resource_create', resource_dict, {'name': data.get('file_name'), 'path': fullFilePath})
                    print(response)
            except:
                utils.file_upload_fail(zipFile, localUploadDirectory, directory, 'CKAN file upload failed')

            shutil.rmtree(localUploadDirectory, ignore_errors=True)
        shutil.rmtree(os.path.join(localUploadDirectory, directory), ignore_errors=True)
    shutil.rmtree(paths.get('temp'), ignore_errors=True)
