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

To install this script, clone this repo to your local machine.  You will also need to pip install requests and requests_toolbelt

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

	"package_id": "",

	"resource_name": "",

	"ckan_url": "",

	"file_name": "",

	"ckan_api_key": "",

	"description": "",
	
	"file_type": ""

}
```
The package ID is for updating a pre-existing resource or creating a new package.  Resource name is the name the file will have on CKAN.  CKAN URL is the base URL of the CKAN instance to upload the file to.  File name is the name of the file in the zip file to be uploaded to CKAN.  API key is the API key of your user on CKAN.  Notification emails is a list of emails that will be emailed with the results of the script.  Metadata is the information when creating a new package that will be uploaded to CKAN.

When you have correctly filled out your job.json file, create a zip file with the file to be uploaded and the job.json file in it.  Then upload this zip file to the correct orginization directory.



## Running the Script

When the Config.Py file is filled out correctly, and the zip file (or multiple zip files) have been uploaded to OwnCloud, you can run this script via the command line by running:
```
Python Main.Py
```
You can also run this script on a scheduler, and it will automatically attempt to upload all zip files in the organization directories to CKAN, and will move the zip files to the success/failure folder of its organization directory depending on the result of the CKAN file upload.
