import sys, os

from config import Config

import src.owncloud as owncloud

owncloudConfig = Config.get('owncloud')


class OwnCloudWrapper(object):
    def __init__(self):
        try:
            self.client = owncloud.Client(owncloudConfig.get('url'), dav_endpoint_version=0)
            self.client.login(owncloudConfig.get('username'), owncloudConfig.get('password'))
            self.root = owncloudConfig.get('root')
        except:
            print('Problems with owncloud connection. Process aborting')
            sys.exit(0)

    def upload_directory(self, ownclouddirectory, localdirectory):
        self.client.put_directory(os.path.join(self.root, ownclouddirectory), localdirectory)


    def download_dir(self, ownclouddirectory, localdirectory):
        self.client.get_directory_as_zip(os.path.join(self.root, ownclouddirectory), localdirectory)

    def delete_file(self, ownclouddirectory, filename):
        self.client.delete(os.path.join(self.root, ownclouddirectory, filename))

    def get_file_listing(self, ownclouddirectory):
        return self.client.list(os.path.join(self.root, ownclouddirectory))