#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Filename: apod_linux.py                                        /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/12/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# imports
import fcntl
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

str_prog_name = "apod_linux"

# NB: need pic_dir before setting up logging

# get current user's home dir
home_dir = os.path.expanduser("~")

# the hidden dir to store the wallpaper and log file
pic_dir = os.path.join(home_dir, "." + str_prog_name)

# look for conf file
conf_file = os.path.join(pic_dir, str_prog_name + ".conf")

# get location of caption script
cap_path = "/usr/bin/" + str_prog_name + "_caption.sh"

# get log file name
log_file = os.path.join(pic_dir, str_prog_name + ".log")

# set up logging
logging.basicConfig(filename = log_file, level = logging.DEBUG,
        format = "%(asctime)s - %(message)s")

#-------------------------------------------------------------------------------
# Prevent more than one instance running at a time (to avoid file collisions)
#-------------------------------------------------------------------------------

# get lock file (write-only, create if necessary)
lock_file = os.open(f"/tmp/" + str_prog_name + ".lock",
        os.O_WRONLY | os.O_CREAT)

# check for existance of lock file
try:
    fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    already_running = False
except IOError:
    already_running = True

# a nother instance is running, log and exit normally
if already_running:
    logging.debug("Already running")
    sys.exit(0)

# log start
logging.debug("---------------------------------------------------------------")
logging.debug("Starting script")

# defaults
enabled = True
delay = 30
caption = True

# NB: clean lines as such:
# # this is a comment, ignored
# FOO=BAR # split at equals, FOO is key, split val at #, BAR is val

try:

    if os.path.exists(conf_file):
        with open(conf_file, "r") as f:
            lines = f.readlines()

            # read key/value pairs from conf file
            for line in lines:
                line_clean = line.strip().upper()

                # ignore comment lines or blanks or lines with no values
                if line_clean.startswith("#") or line_clean == "":
                    continue

                # split key off at equals
                key_val = line_clean.split("=")
                key = key_val[0].strip()

                # split val off ignoring trailing comments
                val = ""
                if (len(key_val) > 1):
                    val_array = key_val[1].split("#")
                    val = val_array[0].strip()

                # check if we are enabled
                if key == "ENABLED":
                    if val != "":
                        enabled = int(val)

                # get delay
                if key == "DELAY":
                    if val != "":
                        delay = int(val)

                # get caption
                if key == "CAPTION":
                    if val != "":
                        caption = int(val)

except Exception as e:
    logging.debug(str(e))

if not enabled:
    logging.debug("Not enabled")
    sys.exit(0)

# wait for internet to come up
# NB: the scripts apod_linux_login.sh and apod_linux_unlock.sh fork this
# script, so a sleep here does not hang the login/unlock process
time.sleep(delay)

#-------------------------------------------------------------------------------
# Get JSON from apod.nasa.gov
#-------------------------------------------------------------------------------

# the url to load JSON from
apod_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

# get the JSON and format it
try:
    response = urllib.request.urlopen(apod_url)
    byte_data = response.read()
    apod_data = json.loads(byte_data)
except urllib.error.URLError as e:
    logging.debug("Could not get JSON, maybe no internet?")
    sys.exit(1)

#-------------------------------------------------------------------------------
# Get pic from apod.nasa.gov
#-------------------------------------------------------------------------------

# pic_path is pic_dir + pic_name
pic_path = None

# make sure it's an image (sometimes it's a video)
media_type = apod_data["media_type"]
if "image" in media_type:
    try:

        # get the url to the actual image
        pic_url = apod_data["hdurl"]

        # create a download file path
        file_ext = pic_url.split(".")[-1]
        pic_name = "apod_linux_wallpaper." + file_ext
        pic_path = os.path.join(pic_dir, pic_name)

        # download the full picture
        urllib.request.urlretrieve(pic_url, pic_path)

        # log result
        logging.debug("Downloaded new file")
    except urllib.error.URLError as e:
        logging.debug("Could not get new file, maybe no internet?")
        sys.exit(1)

else:
    logging.debug("Not an image, doing nothing")
    sys.exit(0)

    # NB: this is for testing on days when the APOD is not an image
    # pic_path = os.path.join(home_dir, 'Documents/Projects/APOD_Linux/test.jpg')
    # apod_data = {'explanation':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

#-------------------------------------------------------------------------------
# Run caption script
#-------------------------------------------------------------------------------

# if we have a valid pic_path
if pic_path != None and caption:
    try:

        # get text to send
        cap_text = apod_data["explanation"]

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
        dir = os.getenv("XDG_GREETER_DATA_DIR")
        if dir == None:
            logging.debug("No greeter dir, bailing")
            sys.exit(1)

        # get location of script
        cmd = "/usr/lib/x86_64-linux-gnu/io.elementary.contract.set-wallpaper"

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
