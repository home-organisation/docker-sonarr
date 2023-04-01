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
def set_namingconfig(database, enable):
    if enable == "True":
        naming = 1
    else:
        naming = 0
    data = (0, naming, '{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}',
            '{Series Title} - {Air-Date} - {Episode Title} {Quality Full}', 'Season {season}', '{Series Title}',
            '{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}', 1, 'Specials')
    query = "INSERT INTO NamingConfig (MultiEpisodeStyle,RenameEpisodes,StandardEpisodeFormat," \
            "DailyEpisodeFormat,SeasonFolderFormat,SeriesFolderFormat,AnimeEpisodeFormat,ReplaceIllegalCharacters," \
            "SpecialsFolderFormat) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
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
        return enable


def get_namingconfig(database):
    query = "SELECT RenameEpisodes FROM NamingConfig"

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
        if rows[0][0] == 1:
            return "True"
        else:
            return "False"


def update_namingconfig(database, enable):
    if enable == "True":
        query = "UPDATE NamingConfig SET RenameEpisodes = 1"
    else:
        query = "UPDATE NamingConfig SET RenameEpisodes = 0"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query)
        connexion.commit()

        db.close()
        connexion.close()
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    else:
        return enable


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    SONARR_NAMING = os.environ.get('SONARR_NAMING')
    if SONARR_NAMING is None or SONARR_NAMING not in ["True", "False"]:
        logging.warning("SONARR_NAMING <%s> is empty or has unaccepted value (True or False), "
                        "nothing to do" % SONARR_NAMING)
        sys.exit(0)

    logging.info("Set Naming Config to application with value %s ..." % SONARR_NAMING)
    NAMING = get_namingconfig(SONARR_DB)
    if NAMING is None:
        sys.exit(1)

    if NAMING == "":
        NAMING = set_namingconfig(SONARR_DB, SONARR_NAMING)
        if NAMING is None:
            sys.exit(1)

    if NAMING != SONARR_NAMING:
        NAMING = update_namingconfig(SONARR_DB, SONARR_NAMING)
        if NAMING is None:
            sys.exit(1)
