# ckan-owncloud-connector

An ETL job package is a zip file with an arbitrary name (as a best practice, we recommend something like YYYYMMDD-RESOURCE_NAME)

In the zip file are two files:

JOB.JSON
{
  "etl_version": <optional: version_number>,
  "package_id": <mandatory: name of package uploading to or creating>,
  "resource_name": <mandatory:resource name>,
  "ckan_url": <mandatory: fully qualified url of CKAN site>,
  "file_name": <mandatory: file name of data file>,
  "method": <mandatory: insert, upsert>,
  "organization": <mandatory: CKAN organization>,
  "ckan_api_key": <mandatory: ckan API key>,
  "notification_emails": <optional - comma-delimited list of emails>
  “metadata:” {  <list all metadata attributes that will be set for the resource>
      “description”: ... 
  }
}

<FILENAME>
File to be uploaded to CKAN

The schema need not be specified in the JOB.JSON file.  The data will be insert/upserted and the new CKAN Data Dictionary will allow the data curator to modify the data-types post-upload.


<ROOT>
|->ORG_1
|->ORG_2
       |
       |->SUCCESS
       |->ERROR

Once a file is processed, the ZIP file is moved to either the SUCCESS or ERROR directory.  An additional report file is added to the ZIP file.  It will be a TXT file describing the outcome of the ETL job.


The Config.Py file looks like this:

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

Here, you should specify the URL of the CKAN instance, your login and password, as well as a local directory that the zip files will be downloaded to.  
