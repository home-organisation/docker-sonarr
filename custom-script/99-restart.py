#!/usr/bin/python3
import os
import logging

###########################################################
# SET STATIC CONFIG
###########################################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


###########################################################
# DEFINE FUNCTION
###########################################################
def restart():
    os.popen('s6-svc -r /var/run/s6-rc/servicedirs/svc-sonarr/')


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    logging.info("Restart application ...")
    restart()
