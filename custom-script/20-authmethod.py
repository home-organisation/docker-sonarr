#!/usr/bin/python3
import logging
import sys
import os
from defusedxml.ElementTree import parse

###########################################################
# SET STATIC CONFIG
###########################################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
CONFIG_FILE = '/config/config.xml'


###########################################################
# DEFINE FUNCTION
###########################################################
def set_authenticationmethod(file, method):
    # Set Authentication method to xml config files
    try:
        tree = parse(file)
        root = tree.getroot()

        root.find("AuthenticationMethod").text = method
        tree.write(file)
    except FileNotFoundError:
        logging.warning("File %s not found" % file)
        return None
    except parse.ParseError:
        logging.warning("File %s is not readable by xml parser" % file)
        return None
    else:
        return method


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    SONARR_AUTHMETHOD = os.environ.get('SONARR_AUTHMETHOD')
    if SONARR_AUTHMETHOD is None or SONARR_AUTHMETHOD not in ["Forms", "Basic"] :
        logging.warning("SONARR_AUTHMETHOD <%s> is empty or has unaccepted value (Forms or Basic), nothing to do" % SONARR_AUTHMETHOD)
        sys.exit(0)
    logging.info("Set authentication method <%s> to application ..." % SONARR_AUTHMETHOD)
    message = set_authenticationmethod(CONFIG_FILE, SONARR_AUTHMETHOD)
    if message is None:
        sys.exit(1)
