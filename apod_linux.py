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
import urllib.request

# the hidden dir to store the wallpaper
home_dir = os.path.expanduser('~')
pic_dir = (home_dir + '/.apod_linux')

# set up logging
logging.basicConfig(filename=(pic_dir + '/apod_linux.log'), level=logging.DEBUG,
    format='%(asctime)s - %(message)s')

# assume no old wallpaper
pic_path = ''

# log start
logging.debug('starting script')

# wait for internet to come up
# N.B. the script /etc/profile.d/apod_linux_login.sh forks this script, so a
# sleep here does not hang the login process
time.sleep(30)

# the url to load JSON from
url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'

# get the JSON and format it
response = urllib.request.urlopen(url)
byte_data = response.read()
data = json.loads(byte_data)

# make sure it's an image (sometimes it's a video)
media_type = data['media_type']
if 'image' in media_type:

    # get the url to the actual image
    pic_url = data['hdurl']

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
    logging.debug('downloaded new file')

else:

    # see if there is an old wallpaper
    list = os.listdir(pic_dir)
    if (len(list) > 0):
        for f in list:

            # make sure it's not the log
            if ('wallpaper' in f):

                # set pic_path to old wallpaper
                pic_path = os.path.join(pic_dir, f)

                # log result
                logging.debug('using old file')
                break

# if there is a valid wallpaper somewhere
if pic_path:
    try:

        # call gsettings to set the wallpaper
        # N.B. *** THIS PART IS GNOME SPECIFIC ***
        cmd = 'gsettings set org.gnome.desktop.background picture-uri file://' + pic_path
        cmd_array = cmd.split()
        subprocess.call(cmd_array)
    except OSError as e:
        logging.debug(str(e))

else:

    # log result
    logging.debug('no new file, no old file, doing nothing')

# -)
