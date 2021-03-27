#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Filename: apod_linux.py                                        /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/17/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# imports
import json
import logging
import os
import subprocess
import time
import urllib.error
import urllib.request

# the hidden dir to store the wallpaper
home_dir = os.path.expanduser('~')
pic_dir = (home_dir + '/.apod_linux')

# set up logging
logging.basicConfig(filename = (pic_dir + '/apod_linux.log'),
        level = logging.DEBUG, format = '%(asctime)s - %(message)s')

# log start
logging.debug('---------------------------------------------------------------')
logging.debug('Starting script')

#-------------------------------------------------------------------------------
# Initialize
#-------------------------------------------------------------------------------

# assume no old wallpaper
pic_path = None

# wait for internet to come up
# N.B. the script /etc/profile.d/apod_linux_login.sh forks this script, so a
# sleep here does not hang the login/wake process
time.sleep(30)

#-------------------------------------------------------------------------------
# THIS PART IS SPECIFIC TO APOD TO GET pic_path
#-------------------------------------------------------------------------------

# the url to load JSON from
apod_url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'

# assume no JSON (but with a valid key)
apod_data = {'media_type':''}

# get the JSON and format it
try:
    response = urllib.request.urlopen(apod_url)
    byte_data = response.read()
    apod_data = json.loads(byte_data)
except urllib.error.URLError as e:
    logging.debug('Could not get JSON, maybe no internet?')

# make sure it's an image (sometimes it's a video)
media_type = apod_data['media_type']
if 'image' in media_type:
    try:

        # get the url to the actual image
        pic_url = apod_data['hdurl']

        # create a download file path
        # N.B. we use a generic filename for the downloaded file so that it
        # overwrites the old file, keeping only the newest wallpaper.
        # this may also result in more than one wallpaper if the file ext
        # is different (i.e jpg vs. png, etc.)
        file_ext = pic_url.split('.')[-1]
        pic_path = (pic_dir + '/wallpaper.' + file_ext)

        # download the full picture
        urllib.request.urlretrieve(pic_url, pic_path)

        # log result
        logging.debug('Downloaded new file')
    except urllib.error.URLError as e:
        logging.debug('Could not get picture, maybe no internet?')

#-------------------------------------------------------------------------------
# DONE
#-------------------------------------------------------------------------------

# if we don't have a valid pic_path
if pic_path == None:

    # see if there is an old wallpaper
    list = os.listdir(pic_dir)
    if (len(list) > 0):
        for f in list:

            # make sure it's not the log
            if ('wallpaper' in f):

                # set pic_path to old wallpaper
                pic_path = os.path.join(pic_dir, f)

                # log result
                logging.debug('No new file, using old file')
                break

# if there is a valid wallpaper somewhere
if pic_path != None:
    try:

#-------------------------------------------------------------------------------
# THIS PART IS SPECIFIC TO ELEMENTARY OS AND MUST NOT BE CALLED USING SUDO!!!!
#-------------------------------------------------------------------------------

        # call set-wallpaper to set the wallpaper
        cmd = '/usr/lib/x86_64-linux-gnu/io.elementary.contract.set-wallpaper '\
                + pic_path

#-------------------------------------------------------------------------------
# DONE
#-------------------------------------------------------------------------------

        cmd_array = cmd.split()
        subprocess.call(cmd_array)
    except OSError as e:
        logging.debug(str(e))

else:

    # log result
    logging.debug('No new file, no old file, doing nothing')

# -)
