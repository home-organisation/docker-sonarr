# Sonarr
This docker image is a custom image of prowlarr based on lscr.io/linuxserver/sonarr.

# Parameters
Container images are configured using parameters passed at runtime has environment variable. 

The parameters below are taken from the original image [lscr.io/linuxserver/sonarr](https://hub.docker.com/r/linuxserver/sonarr) :
|  Parameters | Examples values  | Functions                                                                                                      |
|-------------|------------------|----------------------------------------------------------------------------------------------------------------|
| PUID        |  1000            | for UserID                                                                                                     |
| PGID        |  1000            | for GroupID                                                                                                    |
| TZ          |  Europe/Paris    | Specify a timezone to use, see this [List](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List). |


The extra parameters below come from this custom image :
* Sonarr parameters :

| Parameters          | Examples values | Functions                                                                                |
|---------------------|-----------------|------------------------------------------------------------------------------------------|
| AUTHMETHOD          | Forms (default) | Authentication method for web authentication. Acceptable value is **Forms** or **Basic** |
| APIKEY (optional)   | ****            | Key for api authentication                                                               |
| USER                | admin (default) | Username for web authentication                                                          |
| PASSWORD (required) | ****            | Password for web authentication                                                          |
| NAMING              | True (default)  | Enable or disable rename Tvshows function Acceptable value is **True** or **False**      |

* Database parameters (if not set, sqlite will be used) :

|  Parameters          | Examples values       | Functions                                                  |
|----------------------|-----------------------|------------------------------------------------------------|
| DBUSER               | sonarr (optional)     | Database - postgresql username                             |
| DBPASS               | **** (optional)       | Database - postgresql password                             |
| DBPORT               | 5432 (optional)       | Database - postgresql port                                 |
| DBHOST               | postgresql (optional) | Database - postgresql host                                 |

* Download client parameters :

| Parameters                   | Examples values        | Functions                                 |
|------------------------------|------------------------|-------------------------------------------|
| DOWNLOAD_NAME                | Transmission (default) | Download Client - Transmission name       |
| DOWNLOAD_URL (required)      | transmission           | Download Client - Transmission url        |
| DOWNLOAD_PORT                | 9091 (default)         | Download Client - Transmission port       |
| DOWNLOAD_USER                | admin (default)        | Download Client - Transmission username   |
| DOWNLOAD_PASSWORD (required) | ****                   | Download Client - Transmission password   |
| DOWNLOAD_CATEGORY            | tvshows (default)      | Download Client - Transmission category   |