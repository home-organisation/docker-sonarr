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
|  Parameters          | Examples values        | Functions                                                                                 |
|----------------------|------------------------|-------------------------------------------------------------------------------------------|
| SONARR_AUTHMETHOD    |  Forms                 | Authentication method for web authentication. Acceptable value is **Forms** or **Basic**  |
| SONARR_USER          |  admin                 | Username for web authentication                                                           |
| SONARR_PASSWORD      |  ****                  | Password for web authentication                                                           |
| SONARR_APIKEY        |  ****                  | Key for api authentication                                                                |
| SONARR_ROOTPATH      |  /tv/tvshows           | Local media directory                                                                     |
| SONARR_REMOTEPATH    |  /downloads/           | Remote Path Mappings - remote download directory associate to DOWNLOAD_URL                |
| SONARR_LOCALPATH     |  /tv/downloads/        | Remote Path Mappings - local download directory assosiate to DOWNLOAD_URL                 |
| DOWNLOAD_NAME        |  Transmission          | Download Client - Transmission name                                                       |
| DOWNLOAD_URL         |  localhost             | Download Client - Transmission url                                                        |
| DOWNLOAD_PORT        |  9091                  | Download Client - Transmission port                                                       |
| DOWNLOAD_USER        |  admin                 | Download Client - Transmission username                                                   |
| DOWNLOAD_PASSWORD    |  ****                  | Download Client - Transmission password                                                   |
