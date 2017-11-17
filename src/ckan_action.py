import os
import requests

from requests_toolbelt import MultipartEncoder
from config import Config

ckanConfig = Config.get('ckan')


def action(action, resource_dict, upload=None):
    upload_obj = {}
    fields = resource_dict

    if upload:
        upload_obj = (upload.get('name'), open(os.path.abspath(upload.get('path')), 'rb'), 'application/octet-stream')
        fields = dict(resource_dict.items() + ({'upload': upload_obj}).items())

    m = MultipartEncoder(fields=fields)
    r = requests.post(
        ckanConfig.get('url') + '/api/action/' + action,
        data=m,
        headers={
            'content-type': m.content_type,
            'X-CKAN-API-Key': ckanConfig.get('api_key')
        }
    )

    print r.json()
    print "\n"
    return r
