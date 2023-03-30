#!/usr/bin/python3
import os
import sys
import logging
import xml.etree.ElementTree as ET

###########################################################
# SET STATIC CONFIG
###########################################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
CONFIG_FILE = '/config/config.xml'


###########################################################
# DEFINE FUNCTION
###########################################################
def get_apikey(file):
    # Get ApiKey from xml config files
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        apikey = root.find("ApiKey")

        if apikey is None:
            raise ValueError
    except ValueError:
        logging.error("ApiKey not found in xml file %s" % file)
        return None
    except FileNotFoundError:
        logging.error("File %s not found" % file)
        return None
    except ET.ParseError:
        logging.error("File %s is not readable by xml parser" % file)
        return None
    else:
        return apikey.text


def set_apikey(file, apikey):
    # Set ApiKey to xml config files
    try:
        tree = ET.parse(file)
        root = tree.getroot()

        root.find("ApiKey").text = apikey
        tree.write(file)
    except FileNotFoundError:
        logging.error("File %s not found" % file)
        return None
    except ET.ParseError:
        logging.error("File %s is not readable by xml parser" % file)
        return None
    else:
        return apikey


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    # Get environment variable
    SONARR_APIKEY = os.environ.get('PROWLARR_APIKEY')
    if SONARR_APIKEY is None:
        logging.warning("SONARR_APIKEY with no value, nothing to do")
        sys.exit(0)

    logging.info("Set ApiKey to application ...")
    # Get ApiKey from config file
    APIKEY = get_apikey(CONFIG_FILE)
    if APIKEY is None:
        sys.exit(1)

    if APIKEY != SONARR_APIKEY:
        message = set_apikey(CONFIG_FILE, SONARR_APIKEY)
        if message is None:
            sys.exit(1)
    else:
        logging.warning("ApiKey is already set, nothing to do")
