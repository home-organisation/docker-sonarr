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


###########################################################
# DEFINE FUNCTION
###########################################################
def set_downloadclients(database, name, url, port, username, password, category):
    # Create download clients in database
    data = ("1", name, "Transmission", '{"host": "' + url + '", "port": "' + port
            + '", "useSsl": "false", "urlBase": "/transmission/", "username": "' + username + '", \
            "password": "' + password + '", "tvCategory": "' + category +'"}',
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
        return {"username": username, "password": password, "url": url, "port": port, "category": category}


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
        return {"username": "", "password": "", "url": "", "port": "", "category": ""}
    else:
        username = json.loads(rows[0][0])["username"]
        password = json.loads(rows[0][0])["password"]
        port = json.loads(rows[0][0])["port"]
        url = json.loads(rows[0][0])["host"]
        category = json.loads(rows[0][0])["tvCategory"]
        return {"username": username, "password": password, "url": url, "port": port, "category": category}


def update_downloadclients(database, name, url, port, username, password, category):
    data = ('{"host": "' + url + '", "port": "' + port + '", "useSsl": "false", "urlBase": "/transmission/", "username": "'
            + username + '", "password": "' + password + '", "tvCategory": "' + category +'"}', name)
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
        return {"username": username, "password": password, "url": url, "port": port, "category": category}


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    DOWNLOAD_NAME = os.environ.get('DOWNLOAD_NAME')
    DOWNLOAD_USER = os.environ.get('DOWNLOAD_USER')
    DOWNLOAD_PASSWORD = os.environ.get('DOWNLOAD_PASSWORD')
    DOWNLOAD_URL = os.environ.get('DOWNLOAD_URL')
    DOWNLOAD_PORT = os.environ.get('DOWNLOAD_PORT')
    DOWNLOAD_CATEGORY = os.environ.get('DOWNLOAD_TVCATEGORY')
    if DOWNLOAD_CATEGORY is None:
        DOWNLOAD_CATEGORY = ""
    if DOWNLOAD_USER is None or DOWNLOAD_PASSWORD is None or DOWNLOAD_NAME is None or DOWNLOAD_URL is None or DOWNLOAD_PORT is None:
        logging.warning("DOWNLOAD_NAME, DOWNLOAD_USER, DOWNLOAD_PASSWORD, DOWNLOAD_URL or DOWNLOAD_PORT with no value, nothing to do")
        sys.exit(0)

    logging.info("Set Download Client <%s> for downloader %s to application ..." % (DOWNLOAD_NAME, DOWNLOAD_URL))
    CLIENT = get_downloadclients(SONARR_DB, DOWNLOAD_NAME)
    if CLIENT is None:
        sys.exit(1)

    if CLIENT["username"] == "" and CLIENT["password"] == "" and CLIENT["port"] == "" and CLIENT["url"] == "" and CLIENT["category"] == "":
        CLIENT = set_downloadclients(SONARR_DB, DOWNLOAD_NAME, DOWNLOAD_URL, DOWNLOAD_PORT, DOWNLOAD_USER, DOWNLOAD_PASSWORD, DOWNLOAD_CATEGORY)
        if CLIENT is None:
            sys.exit(1)

    if CLIENT["username"] != DOWNLOAD_USER or CLIENT["password"] != DOWNLOAD_PASSWORD or CLIENT["port"] != DOWNLOAD_PORT or CLIENT["url"] != DOWNLOAD_URL or CLIENT["category"] != DOWNLOAD_CATEGORY:
        logging.info("Download Client %s for downloader %s already exist but with an other parameters, update ..." % (DOWNLOAD_NAME, DOWNLOAD_URL))
        CLIENT = update_downloadclients(SONARR_DB, DOWNLOAD_NAME, DOWNLOAD_URL, DOWNLOAD_PORT, DOWNLOAD_USER, DOWNLOAD_PASSWORD, DOWNLOAD_CATEGORY)
        if CLIENT is None:
            sys.exit(1)
