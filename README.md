# ckan-owncloud-connector

An ETL job package is a zip file with an arbitrary name (as a best practice, we recommend something like YYYYMMDD-RESOURCE_NAME)

In the zip file are two files:

JOB.JSON

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

&lt;FILENAME&gt;

File to be uploaded to CKAN

The schema need not be specified in the JOB.JSON file.  The data will be insert/upserted and the new CKAN Data Dictionary will allow the data curator to modify the data-types post-upload.

&lt;ROOT&gt;

|-&gt;ORG_1

|-&gt;ORG_2

       |

       |-&gt;SUCCESS

       |-&gt;ERROR

Once a file is processed, the ZIP file is moved to either the SUCCESS or ERROR directory.  An additional report file is added to the ZIP file.  It will be a TXT file describing the outcome of the ETL job.

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
