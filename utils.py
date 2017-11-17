import zipfile
import shutil
import os
from owncloud_methods import OwnCloudWrapper

owncloud = OwnCloudWrapper()


def zip_file_extractor(zip_file_path, destination_file_path):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(destination_file_path)
    zip_ref.close()
    os.remove(zip_file_path)


def file_upload_fail(zip_file, local_upload_directory, organization_name, error_message):
    try:
        message = '%s in %s. Upload failed' % (error_message, zip_file.names)
        print(message)
        f = open(local_upload_directory + '/result.txt', 'w')
        f.write(message)
        f.close()
        shutil.make_archive(local_upload_directory, 'zip', local_upload_directory)
        owncloud.upload_directory(organization_name + '/Failure', local_upload_directory)
        shutil.rmtree(local_upload_directory)
    except Exception as e:
        print e
        print('File re-upload failed.  Check ' + organization_name + ' Failure directory')


def file_upload_success(zip_file, local_upload_directory, organization_name):
    try:
        message = '%s successfully uploaded' % zip_file.names
        print(message)
        f = open(local_upload_directory + '/result.txt', 'w')
        f.write(message)
        f.close()
        shutil.make_archive(local_upload_directory, 'zip', local_upload_directory)
        owncloud.upload_directory(organization_name + '/Success', local_upload_directory)
        shutil.rmtree(local_upload_directory)
    except Exception as e:
        print e
        print('File re-upload failed.  Check ' + organization_name + ' Success directory')
