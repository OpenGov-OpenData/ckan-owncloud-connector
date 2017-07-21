# ckan-owncloud-connector

This is a script that allows you to upload your files to CKAN via OwnCloud.  

To run this script, first you must add a zip file to OwnCloud.  Your OwnCloud directory should look like this:


&lt;ROOT&gt;

|-&gt;ORG_1

       |

       |-&gt;SUCCESS

       |-&gt;FAILURE
       
|-&gt;ORG_2

       |-&gt;SUCCESS

       |-&gt;FAILURE
       
etc.

The zip file should be uploaded inside of one the "Organization" directories.  From there, depending on the result of the CKAN job, it will be moved to either the success or failure directory inside of the organization directory.

The zip file should have two files inside of it.  The first file is the file that will be uploaded to CKAN.  This can be a file of any type.  The second is a JSON file that must be called job.json

The job.json file should look like this:

{

  "etl_version": &lt;optional: version_number&gt;,

  "package_id": &lt;mandatory: name of package uploading to or creating&gt;,

  "resource_name": &lt;mandatory:resource name&gt;,

  "ckan_url": &lt;mandatory: fully qualified url of CKAN site&gt;,

  "file_name": &lt;mandatory: file name of data file&gt;,

  "method": &lt;mandatory: insert, upsert&gt;,

  "organization": &lt;mandatory: CKAN organization&gt;,

  "ckan_api_key": &lt;mandatory: ckan API key&gt;,

  "notification_emails": &lt;optional - comma-delimited list of emails&gt;

  “metadata:” {  &lt;list all metadata attributes that will be set for the resource&gt;

    “description”: ... 

    }

}

The schema need not be specified in the JOB.JSON file.  The data will be insert/upserted and the new CKAN Data Dictionary will allow the data curator to modify the data-types post-upload.


Once a file is processed, the ZIP file is moved to either the SUCCESS or ERROR directory inside that organization directory.  An additional report file is added to the ZIP file.  It will be a TXT file describing the outcome of the ETL job.

Before running this script, you must also fill out the Config.Py file from this github repo.  

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

Here, you should specify the URL of the owncloud instance, your login and password, as well as a local directory that the zip files will be downloaded to.  

When the Config.Py file is uploaded, and the zip file has been uploaded to OwnCloud, you can run this script via the command line by running "Python Main.Py"
