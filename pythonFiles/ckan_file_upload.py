import sys
import urllib
import os
import requests
import json
import datetime

from requests_toolbelt import MultipartEncoder


def upload_resource_create(ckan_base, ckan_api_key, resource_dict, upload_file, filename):
    resource_dict['upload'] = (filename, open(os.path.abspath(upload_file), 'rb'), 'application/octet-stream')
    m = MultipartEncoder(fields=dict(resource_dict))
    r = requests.post(ckan_base + '/api/action/resource_create',
                      data=m,
                      headers={
                          'content-type': m.content_type,
                          'X-CKAN-API-Key': ckan_api_key
                      }
                      )
    if r.json().get('success'):
        print 'Created new resource!!'
        print 'Resource-id:\n' + r.json().get('result').get('id')
    else:
        print r.json()
    return r


def upload_resource_patch(ckan_base, ckan_api_key, resource_dict, upload_file, filename):
    resource_dict['last_modified'] = str(datetime.datetime.utcnow())
    resource_dict['upload'] = (filename, open(os.path.abspath(upload_file), 'rb'), 'application/octet-stream')
    m = MultipartEncoder(fields=dict(resource_dict))
    r = requests.post(ckan_base + '/api/action/resource_patch',
                      data=m,
                      headers={
                          'content-type': m.content_type,
                          'X-CKAN-API-Key': ckan_api_key
                      }
                      )
    if r.json().get('success'):
        print 'Updated resource!!'
    else:
        print r.json()
    return r


def upload_package(ckan_base, ckan_api_key, package_dict):
    m = MultipartEncoder(fields=dict(package_dict))
    r = requests.post(ckan_base + '/api/action/package_create',
                      data=m,
                      headers={
                          'content-type': m.content_type,
                          'X-CKAN-API-Key': ckan_api_key
                      }
                      )
    if r.json().get('success'):
        print 'Created package!!'
    else:
        print r.json()
    return r


def package_show(ckan_base, ckan_api_key, package_dict):
    m = MultipartEncoder(fields=dict(package_dict))
    r = requests.post(ckan_base + '/api/action/package_show',
                      data=m,
                      headers={
                          'content-type': m.content_type,
                          'X-CKAN-API-Key': ckan_api_key
                      }
                      )
    if r.json().get('success'):
        print 'Package exists!!'
    else:
        print r.json()
    return r