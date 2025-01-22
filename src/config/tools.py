import os
import logging
import database
import base64
import hashlib
import uuid
import pwd
import grp

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def get_env_parameter() -> dict:
    logging.info("Get environment config variables")

    # Parameter with default value
    user = os.environ.get('USER') or "admin"
    namingconfig = os.environ.get('NAMING') or "True"
    download_name = os.environ.get('DOWNLOAD_NAME') or "Transmission"
    download_user = os.environ.get('DOWNLOAD_USER') or "admin"
    download_port = os.environ.get('DOWNLOAD_PORT') or "9091"
    download_category = os.environ.get('DOWNLOAD_CATEGORY') or "tvshows"

    # Parameter without default value
    password = os.environ.get('PASSWORD')
    download_url = os.environ.get('DOWNLOAD_URL')
    download_password = os.environ.get('DOWNLOAD_PASSWORD')

    # Parameter with static value
    rootpath = "/tv/" + download_category
    remotepath = "/downloads/"
    localpath = "/tv/downloads/"


    param = {
        "user": user,
        "identifier": None,
        "salt": None,
        "password": password,
        "rootpath": rootpath,
        "namingconfig": namingconfig,
        "remotepath": remotepath,
        "localpath": localpath,
        "download" : {
            "name": download_name,
            "user": download_user,
            "password": download_password,
            "url": download_url,
            "port": download_port,
            "category": download_category
        }
    }

    return param

def get_db_parameter() -> dict:
    logging.info("Get database config variables")
    user = os.environ.get('USER') or "admin"
    download_name = os.environ.get('DOWNLOAD_NAME') or "Transmission"
    dbuser = os.environ.get('DBUSER')
    dbpass = os.environ.get('DBPASS')
    dbport = os.environ.get('DBPORT')
    dbhost = os.environ.get('DBHOST')

    if dbuser is None or dbpass is None or dbport is None or dbhost is None:
        # Connection to sqlite database
        db = database.Sqlite()
        db.connect()
    else:
        # Connection to postgresql database
        db = database.Postgres()
        db.connect(user=dbuser, password=dbpass, host=dbhost ,port=dbport)

    user, identifier, salt, password = db.get_credential(user)
    rootpath = db.get_rootpath()
    download_user, download_password, download_port, download_url, download_category, remotepath, localpath = db.get_download(download_name)
    namingconfig = db.get_namingconfig()

    db.close()

    param = {
        "user": user,
        "identifier": identifier,
        "salt": salt,
        "password": password,
        "rootpath": rootpath,
        "namingconfig": namingconfig,
        "remotepath": remotepath,
        "localpath": localpath,
        "download" : {
            "name": download_name,
            "user": download_user,
            "password": download_password,
            "url": download_url,
            "port": download_port,
            "category": download_category
        }
    }

    return param

def reconcile(desired: dict, current: dict):
    logging.info("Start to reconcile config parameter")

    # database connection
    dbuser = os.environ.get('DBUSER')
    dbpass = os.environ.get('DBPASS')
    dbport = os.environ.get('DBPORT')
    dbhost = os.environ.get('DBHOST')

    if dbuser is None or dbpass is None or dbport is None or dbhost is None:
        # Connection to sqlite database
        db = database.Sqlite()
        db.connect()
    else:
        # Connection to postgresql database
        db = database.Postgres()
        db.connect(user=dbuser, password=dbpass, host=dbhost ,port=dbport)


    # reconcile credential parameter
    if current["password"] is None:
        identifier = get_identifier()
        salt = get_salt()
    else:
        identifier = current["identifier"]
        salt = current["salt"]

    password = get_hash_password(desired["password"], salt)

    if desired["user"] != current["user"] or password != current["password"]:
        logging.info("Detection of drift for credential, reconcile the value")

        # Create new credential (current user None)
        if current["user"] is None:
            db.set_credential(username=desired["user"], identifier=identifier, salt=salt, password=password)
        # Update existing credential (current user not None)
        else:
            db.update_credential(username=desired["user"], password=password)

    # Reconcile root path parameter
    if not os.path.exists(desired["rootpath"]):
        logging.warning("rootpath directory %s doesn't exist, create the directory" % desired["rootpath"])
        os.makedirs(desired["rootpath"])
        os.chown(desired["rootpath"], pwd.getpwnam("abc").pw_uid, grp.getgrnam("abc").gr_gid)

    if current["rootpath"] != desired["rootpath"]:
        logging.info("Detection of drift for root path, reconcile the value")
        if current["rootpath"] is None:
            db.set_rootpath(desired["rootpath"])
        else:
            db.update_rootpath(desired["rootpath"])


    # Reconcile download client and remote path mapping parameter
    if current["remotepath"] != desired["remotepath"] or current["localpath"] != desired["localpath"] or current["download"] != desired["download"]:
        logging.info("Detection of drift for download client, reconcile the value")
        if current["remotepath"] is None or current["localpath"] is None or current["download"]["url"] is None:
            db.set_download(name=desired["download"]["name"], username=desired["download"]["user"], password=desired["download"]["password"], port=desired["download"]["port"], url=desired["download"]["url"], category=desired["download"]["category"], remotepath=desired["remotepath"], localpath=desired["localpath"])
        else:
            db.update_download(name=desired["download"]["name"], username=desired["download"]["user"], password=desired["download"]["password"], port=desired["download"]["port"], url=desired["download"]["url"], category=desired["download"]["category"], remotepath=desired["remotepath"], localpath=desired["localpath"])

    # Reconcile naming config parameter
    if current["namingconfig"] != desired["namingconfig"]:
        logging.info("Detection of drift for naming config, reconcile the value")
        if current["namingconfig"] is None:
            db.set_namingconfig(desired["namingconfig"])
        else:
            db.update_namingconfig(desired["namingconfig"])


    db.close()


def restart():
    logging.info("Restart application")
    os.popen('s6-svc -r /var/run/s6-rc/servicedirs/svc-sonarr/')

def get_hash_password(password: str, salt: bytes) -> bytes:
    if password is None:
        encryptpassword = None
    else:
        encryptsalt = base64.b64decode(salt)
        encryptpassword = base64.b64encode(hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), encryptsalt, 10000, 32))

    return encryptpassword

def get_salt() -> bytes:
    salt = base64.b64encode(os.urandom(16))

    return salt

def get_identifier() -> str:
    identifier = str(uuid.uuid4())

    return identifier