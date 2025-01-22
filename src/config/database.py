import logging
import sqlite3
import json
import psycopg2

SQLITE_FILE='/config/sonarr.db'
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

class Database:
    def __init__(self):
        self.conn = None

    def close(self):
        try:
            self.conn.close()
        except (sqlite3.DatabaseError, Exception) as error:
            logging.error("Closing connection to sqlite database failed")
            logging.error(error)
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("Closing connection to postgresql database failed")
            logging.error(error)

    def get(self, query: str, data: tuple[str] = None):
        cur = self.conn.cursor()

        try:
            if data is None:
                cur.execute(query)
            else:
                cur.execute(query, data)
            row = cur.fetchone()

            return row
        except (sqlite3.DatabaseError, Exception) as error:
            logging.error("failed to get information on database")
            logging.error(error)
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("failed to get information on database")
            logging.error(error)
        finally:
            cur.close()

    def set(self, query: str, data: tuple = None):
        cur = self.conn.cursor()

        try:
            if data is None:
                cur.execute(query)
            else:
                cur.execute(query, data)
            self.conn.commit()

        except (sqlite3.DatabaseError, Exception) as error:
            logging.error("failed to set information on database")
            logging.error(error)
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("failed to set information on database")
            logging.error(error)
        finally:
            cur.close()

    def get_rootpath(self) -> str:
        query = 'SELECT "Path" FROM "RootFolders"'
        config = self.get(query)

        if config is not None:
            path = config[0]
        else:
            path = None

        return path

    def set_rootpath(self, path: str):
        query = 'INSERT INTO "RootFolders" ("Path") VALUES(\'' + path + '\')'

        self.set(query)

    def update_rootpath(self, path: str):
        query = 'UPDATE "RootFolders" SET "Path" = \'' + path + '\''

        self.set(query)

    def get_download(self, name: str) -> tuple[str, str, str, str, str, str, str]:
        # Set default variables
        username = None
        password = None
        port = None
        url = None
        category = None
        remotepath = None
        localpath = None

        # Get download client config
        query = 'SELECT "Settings" FROM "DownloadClients" WHERE "Name" = \'' + name + '\''
        config = self.get(query)

        if config is not None:
            username = json.loads(config[0])["username"]
            password = json.loads(config[0])["password"]
            port = str(json.loads(config[0])["port"])
            url = json.loads(config[0])["host"]
            category = json.loads(config[0])["movieCategory"]

        # Get remote path mapping associated with the download client
        if url is not None:
            query = 'SELECT "RemotePath","LocalPath" FROM "RemotePathMappings" WHERE "Host" = \'' + url + '\''
            mapping = self.get(query)

            if mapping is not None:
                remotepath = mapping[0]
                localpath = mapping[1]


        return username, password, port, url, category, remotepath, localpath

    def set_download(self, name: str, username: str, password: str, port: str, url: str, category: str, remotepath: str, localpath: str):
        query = 'INSERT INTO "DownloadClients" ("Enable", "Name", "Implementation", "Settings", "ConfigContract", "Priority", "RemoveCompletedDownloads", "RemoveFailedDownloads") VALUES(\'1\', \''+ name +'\', \'Transmission\', \'{"host": "' + url + '", "port": ' + port + ', "useSsl": false, "urlBase": "/transmission/", "username": "' + username + '", "password": "' + password + '", "tvCategory": "' + category + '"}\', \'TransmissionSettings\', \'1\', \'1\', \'1\')'
        self.set(query)

        query = 'INSERT INTO "RemotePathMappings" ("Host", "RemotePath", "LocalPath") VALUES(\'' + url + '\', \'' + remotepath + '\', \'' + localpath + '\')'
        self.set(query)

    def update_download(self, name: str, username: str, password: str, port: str, url: str, category: str, remotepath: str, localpath: str):
        query = 'UPDATE "DownloadClients" SET "Settings" = \'{"host": "' + url + '", "port": ' + port + ', "useSsl": false, "urlBase": "/transmission/", "username": "' + username + '", "password": "' + password + '", "tvCategory": "' + category + '"}\' WHERE "Name" = \'' + name + '\''
        self.set(query)

        query = 'UPDATE "RemotePathMappings" SET "RemotePath" = \'' + remotepath +'\', "LocalPath" = \'' + localpath +'\', "Host" = \'' + url +'\''
        self.set(query)

    def get_namingconfig(self) -> None | str:
        query = 'SELECT "RenameEpisodes" FROM "NamingConfig"'
        row = self.get(query)

        if row is not None:
            if row[0] == 1:
                return "True"
            else:
                return "False"
        else:
            return None

    def set_namingconfig(self, enable: str):
        if enable == "True":
            query = 'INSERT INTO "NamingConfig" ("MultiEpisodeStyle", "RenameEpisodes", "StandardEpisodeFormat", "DailyEpisodeFormat", "SeasonFolderFormat", "SeriesFolderFormat", "AnimeEpisodeFormat", "ReplaceIllegalCharacters", "SpecialsFolderFormat") VALUES(0, True, \'{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}\', \'{Series Title} - {Air-Date} - {Episode Title} {Quality Full}\', \'Season {season}\', \'{Series Title}\', \'{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}\', 1, \'Specials\')'
        else:
            query = 'INSERT INTO "NamingConfig" ("MultiEpisodeStyle", "RenameEpisodes", "StandardEpisodeFormat", "DailyEpisodeFormat", "SeasonFolderFormat", "SeriesFolderFormat", "AnimeEpisodeFormat", "ReplaceIllegalCharacters", "SpecialsFolderFormat") VALUES(0, False, \'{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}\', \'{Series Title} - {Air-Date} - {Episode Title} {Quality Full}\', \'Season {season}\', \'{Series Title}\', \'{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}\', 1, \'Specials\')'

        self.set(query)

    def update_namingconfig(self, enable: str):
        if enable == "True":
            query = 'UPDATE "NamingConfig" SET "RenameEpisodes" = True'
        else:
            query = 'UPDATE "NamingConfig" SET "RenameEpisodes" = False'

        self.set(query)


class Postgres(Database):
    def connect(self, user: str, password: str, host: str, port: str):
        # connecting to PostgreSQL database
        try:
            self.conn = psycopg2.connect(database="sonarr-main", user=user, password=password, host=host, port=port)
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("Connection to postgresql database failed")
            logging.error(error)

    def get_credential(self,username: str):
        data = (username,)
        query = 'SELECT "Identifier", "Salt", "Password" FROM "Users" WHERE "Username" = %s'

        row = self.get(query, data)
        if row is not None:
            return username, row[0], row[1].encode(), row[2].encode()
        else:
            return None, None, None, None

    def set_credential(self,username: str, identifier: str, salt: bytes, password: bytes):
        data = (identifier, username, password.decode(), salt.decode(), 10000)
        query = 'INSERT INTO "Users" ("Identifier", "Username", "Password", "Salt", "Iterations") VALUES(%s, %s, %s, %s, %s)'

        self.set(query, data)

    def update_credential(self,username: str, password: bytes):
        data = (password.decode(), username)
        query = 'UPDATE "Users" SET "Password" = %s WHERE "Username" = %s'

        self.set(query, data)


class Sqlite(Database):
    def connect(self):
        # connection to sqlite database
        try:
            self.conn = sqlite3.connect(SQLITE_FILE)
        except (sqlite3.DatabaseError, Exception) as error:
            logging.error("Connection to sqlite database failed")
            logging.error(error)

    def get_credential(self,username: str):
        data = (username,)
        query = 'SELECT "Identifier", "Salt", "Password" FROM "Users" WHERE "Username" = ?'

        row = self.get(query, data)
        if row is not None:
            return username, row[0], row[1], row[2]
        else:
            return None, None, None, None

    def set_credential(self,username: str, identifier: str, salt: bytes, password: bytes):
        data = (identifier, username, password, salt, 10000)
        query = 'INSERT INTO "Users" ("Identifier", "Username", "Password", "Salt", "Iterations") VALUES(?, ?, ?, ?, ?)'

        self.set(query, data)

    def update_credential(self,username: str, password: bytes):
        data = (password, username)
        query = 'UPDATE "Users" SET "Password" = ? WHERE "Username" = ?'

        self.set(query, data)