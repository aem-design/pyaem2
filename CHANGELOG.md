### 0.9.2-pre
* Add packagemanager#has_package
* Add FRESH_CONNECT to all requests to ensure no cached connection is used
* Add sling#is_valid_login
* Rename packagemanagersync to packagemanagerservicehtml
* Move non update/download package methods from packagemanager to packagemanagerservicejson

### 0.9.1
* Add file_path arg to webconsole#install_bundle to allow custom bundle file location
* Add response code 201 handling as webconsole#install_bundle success 
* Add response code 201 handling as webconsole#start_bundle success 
* Add response code 201 handling as pakagemanagersync#* success

### 0.9.0
* Initial version
