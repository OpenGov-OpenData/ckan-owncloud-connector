# CKAN OwnCloud Connector

This is a script that allows you to upload your files to CKAN via OwnCloud.  

## Getting Started

First, clone this repo to your local machine.

### Prerequisites

To run this script, you will need a working version of Python.  You should also have a running instance of OwnCloud.  Your OwnCloud directory should look like this:

```
ROOT

| ORG_1

       | SUCCESS

       | FAILURE
       
| ORG_2

       | SUCCESS

       | FAILURE
       
(etc.)
```

### Installing

To install this script, clone this repo to your local machine

## Configuring the Script

To run this script, you will need to set up the config.py file, and upload a zip file (or multiple zip files) to your OwnCloud account.

### Config.Py

Your Config.Py file (found in this repo) should look like this:

```
Config = {

    # Change this to your ownCloud's URL

    'owncloud_url': '',

    # ownCloud login

    'owncloud_login': '',

    # ownCloud password

    'owncloud_password': '',

    # this is the local path to download to

    'localDownloadDirectory': '',

}
```

Here, you should specify the URL of the owncloud instance, your login and password, as well as a local directory that the zip files will be downloaded to.  

### Job.Json

You should create a zip file with two files inside of it.  The first file is the file that will be uploaded to CKAN.  This can be a file of any type and any name.  The second is a JSON file that must be called job.json.  The job.json file should look like this:

```
{

  "etl_version": optional: version_number,

  "package_id": mandatory: name of package uploading to or creating,

  "resource_name": mandatory: resource name,

  "ckan_url": mandatory: fully qualified url of CKAN site,

  "file_name": mandatory: full name of data file including file extension,

  "ckan_api_key": mandatory: ckan API key,

  “metadata:” {  list all metadata attributes that will be set for the resource

    “description”: ... 

    }

}
```
The package ID is for updating a pre-existing resource.  You should specify the package ID of the package this resource is in.  Resource name is the name the file will have on CKAN.  CKAN URL is the base URL of the CKAN instance to upload the file to.  File name is the name of the file in the zip file.  Method is the method to update the resource (either insert or upsert.  If creating a new resource, leave blank).  Organization is the organization to upload this dataset to.  API key is the API key of your user on CKAN.  Notification emails is a list of emails that will be emailed with the results of the script.  Metadata is the information when creating a new package that will be uploaded to CKAN.

When you have correctly filled out your job.json file, create a zip file with the file to be uploaded and the job.json file in it.  Then upload this zip file to the correct orginization directory.



## Running the Script

When the Config.Py file is filled out correctly, and the zip file (or multiple zip files) have been uploaded to OwnCloud, you can run this script via the command line by running:
```
Python Main.Py
```
You can also run this script on a scheduler, and it will automatically attempt to upload all zip files in the organization directories to CKAN, and will move the zip files to the success/failure folder of its organization directory depending on the result of the CKAN file upload.

# CKAN PDF File Library

This is a script that allows you to batch upload PDF's to a "PDf Library" on your CKAN instance.  It will read the metadata of the files from a CSV, and use this information to upload the files to CKAN.  There will be a Config.Py file with the name of the base CKAN URL and the CKAN API key of your CKAN user.  From there you will fill out a CSV file with these columns:

```
{

  "package_id": mandatory: name of package uploading to or creating,

  "resource_name": mandatory:resource name,

  "file_path": mandatory: full path of file on local machine,
  
  "metadata_fields": TBD - metadata fields,

}
```

From here you will include this information for each file you want uploaded.  Each file will be one row in the CSV.  You will then run this script via the command line.
