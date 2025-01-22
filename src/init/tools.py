import os
import pwd
import grp
import logging
from xml.etree.ElementTree import Element
from defusedxml import ElementTree

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def get_env_parameter() -> dict:
    logging.info("Get environment init variables")

    apikey = os.environ.get('APIKEY')
    authmethod = os.environ.get('AUTHMETHOD') or "Forms"
    dbuser = os.environ.get('DBUSER')
    dbpass = os.environ.get('DBPASS')
    dbport = os.environ.get('DBPORT')
    dbhost = os.environ.get('DBHOST')

    if dbuser is None or dbpass is None or dbport is None or dbhost is None:
        logging.warning("One of environment variables is not set (DBUSER, DBPASS, DBPORT or DBHOST), don't configure postgresql")
        dbuser = None
        dbpass = None
        dbport = None
        dbhost = None

    env = {
        "ApiKey": apikey,
        "AuthenticationMethod": authmethod,
        "PostgresUser": dbuser,
        "PostgresPassword": dbpass,
        "PostgresPort": dbport,
        "PostgresHost": dbhost
    }

    return env

def reconcile(env: dict, path: str):
    logging.info("Start to reconcile init parameter")

    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        logging.warning("Config directory %s doesn't exist, create the directory" % dirname)
        os.makedirs(dirname)

    if not os.path.isfile(path):
        logging.warning("Config file %s doesn't exist, create the file" % path)
        with open(path, 'w') as file:
            file.write("<Config>\n")
            file.write("</Config>")
        os.chown(path, pwd.getpwnam("abc").pw_uid, grp.getgrnam("abc").gr_gid)

    try:
        tree = ElementTree.parse(path)
        root = tree.getroot()

        for key in env:
            elmt = root.find(key)
            if elmt is not None:
                value = elmt.text
            else:
                value = None

            # Element have to be created
            if value is None and env[key] is not None:
                root.append(Element(key))
                value = ""

            # Element have to be deleted
            if value is not None and env[key] is None:
                logging.info("Detection of drift for %s, reconcile the value" % key)
                root.remove(root.find(key))

            # Element have to be updated
            if value != env[key] and value is not None and env[key] is not None:
                logging.info("Detection of drift for %s, reconcile the value" % key)
                root.find(key).text = env[key]

        tree.write(path)


    except ElementTree.ParseError:
        logging.error("File %s is not readable by xml parser" % path)