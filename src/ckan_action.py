import os
import requests
import datetime

from requests_toolbelt import MultipartEncoder

from config import Config
ckanConfig = Config.get('ckan')


# package_create,
# package_show,
# resource_patch,
# resource_create
def action(action, resource_dict, upload = None):
  upload_obj = {}
  if upload:
    upload_obj = (upload.get('name'), open(os.path.abspath(upload.get('path')), 'rb'), 'application/octet-stream')

  m = MultipartEncoder(fields=dict(resource_dict.items() + ({ 'upload': upload_obj }).items()))
  r = requests.post(
        ckanConfig.get('url') + '/api/action/' + action,
        data = m,
        headers = {
          'content-type': m.content_type,
          'X-CKAN-API-Key': ckanConfig.get('api_key')
        }
      )

  if r.json().get('success'):
      print action + ': Success!!'
  else:
      print r.json()

  return r
