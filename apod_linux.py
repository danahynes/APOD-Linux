#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Filename: apod_linux.py                                        /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/12/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# imports
import json
import logging
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

#-------------------------------------------------------------------------------
# Initialize
#-------------------------------------------------------------------------------

# NB: need pic_dir before setting up logging

# get current user's home dir
home_dir = os.path.expanduser('~')

# the hidden dir to store the wallpaper and log file
pic_dir = os.path.join(home_dir, '.apod_linux')

# get log file name`
log_name = os.path.join(pic_dir, 'apod_linux.log')

# set up logging
logging.basicConfig(filename = log_name, level = logging.DEBUG,
        format = '%(asctime)s - %(message)s')

# log start
logging.debug('---------------------------------------------------------------')
logging.debug('Starting script')

# default delay
delay = 30
key_val = []

# look for conf file
try:
    conf_name = os.path.join(pic_dir, 'apod_linux.conf')
    with open(conf_name, 'r') as f:
        lines = f.readlines()

        # try to find a delay in the conf file
        for line in lines:
            line_strip = line.strip()
            if not line_strip.startswith('#'):
                if 'DELAY' in line_strip.upper():
                    key_val = line_strip.split('=')
                    val = key_val[1].strip()
                    delay = int(val)
except Exception as e:
    logging.debug(str(e))

# wait for internet to come up
# NB: the scripts apod_linux_login.sh and apod_linux_unlock.sh fork this
# script, so a sleep here does not hang the login/unlock process
time.sleep(delay)

#-------------------------------------------------------------------------------
# Get JSON from apod.nasa.gov
#-------------------------------------------------------------------------------

# the url to load JSON from
apod_url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'

# get the JSON and format it
try:
    response = urllib.request.urlopen(apod_url)
    byte_data = response.read()
    apod_data = json.loads(byte_data)
except urllib.error.URLError as e:
    logging.debug('Could not get JSON, maybe no internet?')
    sys.exit(1)

#-------------------------------------------------------------------------------
# Get pic from apod.nasa.gov
#-------------------------------------------------------------------------------

# pic_path is pic_dir + pic_name
pic_path = None

# make sure it's an image (sometimes it's a video)
media_type = apod_data['media_type']
if 'image' in media_type:
    try:

        # get the url to the actual image
        pic_url = apod_data['hdurl']

        # create a download file path
        file_ext = pic_url.split('.')[-1]
        pic_name = 'apod_linux_wallpaper.' + file_ext
        pic_path = os.path.join(pic_dir, pic_name)

        # download the full picture
        urllib.request.urlretrieve(pic_url, pic_path)

        # log result
        logging.debug('Downloaded new file')
    except urllib.error.URLError as e:
        logging.debug('Could not get new file, maybe no internet?')
        sys.exit(1)

else:
    logging.debug('Not an image, doing nothing')
    sys.exit(0)

    # NB: this is for testing on days when the APOD is not an image
    # pic_path = os.path.join(home_dir, 'Documents/Projects/APOD_Linux/test.jpg')
    # apod_data = {'explanation':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

#-------------------------------------------------------------------------------
# Run caption script
#-------------------------------------------------------------------------------

# if we have a valid pic_path
if pic_path != None:
    try:

        # get location of caption script
        cap_path = '/usr/bin/apod_linux_caption.sh'

        # get text to send
        cap_text = apod_data['explanation']

        # call the caption script with text and pic path
        subprocess.call([cap_path, pic_path, cap_text])

    except OSError as e:
        logging.debug(str(e))
        sys.exit(1)

#-------------------------------------------------------------------------------
# THIS PART IS SPECIFIC TO ELEMENTARY OS AND MUST NOT BE CALLED USING SUDO!!!!
#-------------------------------------------------------------------------------

# if we have a valid pic_path
if pic_path != None:
    try:

        # first check for env varible
        dir = os.getenv('XDG_GREETER_DATA_DIR')
        if dir == None:
            logging.debug('No greeter dir, bailing')
            sys.exit(1)

        # get location of script
        cmd = '/usr/lib/x86_64-linux-gnu/io.elementary.contract.set-wallpaper'

        # call the script with pic path
        subprocess.call([cmd, pic_path])

        # remove file since its been copied everywhere
        # NB: this is kept with eOS specific code since we know that's how
        # set-wallpaper works. other os's may need to keep the file in place
        os.remove(pic_path)
    except OSError as e:
        logging.debug(str(e))
        sys.exit(1)

#-------------------------------------------------------------------------------
# DONE
#-------------------------------------------------------------------------------

# -)
