#!/usr/bin/python3
import sys
import os
import sqlite3
import logging

###########################################################
# SET STATIC CONFIG
###########################################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
SONARR_DB = '/config/sonarr.db'
DOWNLOAD_URL = 'localhost'


###########################################################
# DEFINE FUNCTION
###########################################################
def set_remotepath(database, url, localpath, remotepath):
    # Create rootpath in database
    data = (url, remotepath, localpath)
    query = "INSERT INTO RemotePathMappings (Host,RemotePath,LocalPath) VALUES(?, ?, ?)"
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
        return {"remotepath": remotepath, "localpath": localpath}


def get_remotepath(database, url):
    data = (url,)
    query = "SELECT RemotePath,LocalPath FROM RemotePathMappings WHERE Host = ?"

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
        return {"remotepath": "", "localpath": ""}
    else:
        return {"remotepath": rows[0][0], "localpath": rows[0][1]}


def update_remotepath(database, url, localpath, remotepath):
    data = (remotepath, localpath, url)
    query = "UPDATE RemotePathMappings SET RemotePath = ?, LocalPath = ? WHERE Host = ?"

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
        return {"remotepath": remotepath, "localpath": localpath}


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    SONARR_REMOTEPATH = os.environ.get('SONARR_REMOTEPATH')
    SONARR_LOCALPATH = os.environ.get('SONARR_LOCALPATH')
    if DOWNLOAD_URL is None or SONARR_LOCALPATH is None or SONARR_REMOTEPATH is None:
        logging.warning("DOWNLOAD_URL, SONARR_REMOTEPATH or SONARR_LOCALPATH with no value, nothing to do")
        sys.exit(0)

    logging.info("Set Remote Path Mapping for downloader %s with remote path %s and local path %s to application ..." % (DOWNLOAD_URL, SONARR_REMOTEPATH, SONARR_LOCALPATH))
    PATH = get_remotepath(SONARR_DB, DOWNLOAD_URL)
    if PATH is None:
        sys.exit(1)

    if PATH["remotepath"] == "" and PATH["localpath"] == "":
        PATH = set_remotepath(SONARR_DB, DOWNLOAD_URL, SONARR_LOCALPATH, SONARR_REMOTEPATH)
        if PATH is None:
            sys.exit(1)

    if PATH["remotepath"] != SONARR_REMOTEPATH or PATH["localpath"] != SONARR_LOCALPATH:
        logging.info("Remote Path Mapping for downloader %s already exist but with an other path, update ..." % DOWNLOAD_URL)
        PATH = update_remotepath(SONARR_DB, DOWNLOAD_URL, SONARR_LOCALPATH, SONARR_REMOTEPATH)
        if PATH is None:
            sys.exit(1)
