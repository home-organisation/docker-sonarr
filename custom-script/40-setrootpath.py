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


###########################################################
# DEFINE FUNCTION
###########################################################
def set_rootpath(database, path):
    # Create rootpath in database
    data = (path,)
    query = "INSERT INTO RootFolders (Path) VALUES( ? )"
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
        return path


def get_rootpath(database):
    query = "SELECT Path FROM RootFolders"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query)
        rows = db.fetchall()

        db.close()
        connexion.close()

        if not rows:
            raise ValueError
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    except ValueError:
        return ""
    else:
        return rows[0][0]


def update_rootpath(database, path):
    data = (path,)
    query = "UPDATE RootFolders SET Path = ?"

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
        return path


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    SONARR_ROOTPATH = os.environ.get('SONARR_ROOTPATH')
    if SONARR_ROOTPATH is None:
        logging.warning("SONARR_ROOTPATH with no value, nothing to do")
        sys.exit(0)

    logging.info("Set Root Path %s to application ..." % SONARR_ROOTPATH)
    PATH = get_rootpath(SONARR_DB)
    if PATH is None:
        sys.exit(1)

    elif PATH == "":
        PATH = set_rootpath(SONARR_DB, SONARR_ROOTPATH)
        if PATH is None:
            sys.exit(1)

    elif PATH != SONARR_ROOTPATH:
        logging.info("Root Path already exist but with an other path, update to %s ..." % SONARR_ROOTPATH)
        PATH = update_rootpath(SONARR_DB, SONARR_ROOTPATH)
        if PATH is None:
            sys.exit(1)
