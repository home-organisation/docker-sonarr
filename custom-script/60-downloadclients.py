#!/usr/bin/python3
import sys
import os
import sqlite3
import logging
import json

###########################################################
# SET STATIC CONFIG
###########################################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
SONARR_DB = '/config/sonarr.db'
DOWNLOAD_URL = 'localhost'
DOWNLOAD_PORT = '9091'
DOWNLOAD_NAME = 'Transmission'


###########################################################
# DEFINE FUNCTION
###########################################################
def set_downloadclients(database, name, url, port, username, password):
    # Create download clients in database
    data = ("1", name, "Transmission", '{"host": "' + url + '", "port": "' + port
            + '", "useSsl": "false", "urlBase": "/transmission/", "username": "' + username + '", "password": "' + password + '"}',
            "TransmissionSettings", "1", "1", "1")
    query = "INSERT INTO DownloadClients (Enable,Name,Implementation,Settings,ConfigContract,Priority," \
            "RemoveCompletedDownloads,RemoveFailedDownloads) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query, data)
        connexion.commit()

        db.close()
        connexion.close()
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    else:
        return {"username": username, "password": password}


def get_downloadclients(database, name):
    data = (name,)
    query = "SELECT Settings FROM DownloadClients WHERE Name = ?"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query, data)
        rows = db.fetchall()

        db.close()
        connexion.close()

        if not rows:
            raise ValueError
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    except ValueError:
        return {"username": "", "password": ""}
    else:
        username = json.loads(rows[0][0])["username"]
        password = json.loads(rows[0][0])["password"]
        return {"username": username, "password": password}


def update_downloadclients(database, name, url, port, username, password):
    data = ('{"host": "' + url + '", "port": "' + port + '", "useSsl": "false", "urlBase": "/transmission/", "username": "'
            + username + '", "password": "' + password + '"}', name)
    query = "UPDATE DownloadClients SET Settings = ? WHERE Name = ?"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query, data)
        connexion.commit()

        db.close()
        connexion.close()
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    else:
        return {"username": username, "password": password}


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    DOWNLOAD_USER = os.environ.get('DOWNLOAD_USER')
    DOWNLOAD_PASSWORD = os.environ.get('DOWNLOAD_PASSWORD')
    if DOWNLOAD_USER is None or DOWNLOAD_PASSWORD is None:
        logging.warning("DOWNLOAD_USER or DOWNLOAD_PASSWORD with no value, nothing to do")
        sys.exit(0)

    logging.info("Set Download Client <%s> for downloader %s to application ..." % (DOWNLOAD_NAME, DOWNLOAD_URL))
    CLIENT = get_downloadclients(SONARR_DB, DOWNLOAD_NAME)
    if CLIENT is None:
        sys.exit(1)

    if CLIENT["username"] == "" and CLIENT["password"] == "":
        CLIENT = set_downloadclients(SONARR_DB, DOWNLOAD_NAME, DOWNLOAD_URL, DOWNLOAD_PORT, DOWNLOAD_USER, DOWNLOAD_PASSWORD)
        if CLIENT is None:
            sys.exit(1)

    if CLIENT["username"] != DOWNLOAD_USER or CLIENT["password"] != DOWNLOAD_PASSWORD:
        logging.info("Download Client %s for downloader %s already exist but with an other parameters, update ..." % (DOWNLOAD_NAME, DOWNLOAD_URL))
        CLIENT = update_downloadclients(SONARR_DB, DOWNLOAD_NAME, DOWNLOAD_URL, DOWNLOAD_PORT, DOWNLOAD_USER, DOWNLOAD_PASSWORD)
        if CLIENT is None:
            sys.exit(1)
