#!/usr/bin/python3
import logging
import sys
import xml.etree.ElementTree as ET

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
        tree = ET.parse(file)
        root = tree.getroot()

        root.find("AuthenticationMethod").text = method
        root.find("AuthenticationRequired").text = "Enabled"
        tree.write(file)
    except FileNotFoundError:
        logging.warning("File %s not found" % file)
        return None
    except ET.ParseError:
        logging.warning("File %s is not readable by xml parser" % file)
        return None
    else:
        return method


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    logging.info("Set authentication method <Forms> to application ...")
    message = set_authenticationmethod(CONFIG_FILE, "Forms")
    if message is None:
        sys.exit(1)
