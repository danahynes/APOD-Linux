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
import os
import subprocess
import time
import urllib.request

# wait for internet to come up
# N.B. the script /etc/profile.d/apod_linux.sh forks this script, so a sleep
# here does not hang the login process
time.sleep(30)

# the hidden dir to store the wallpaper
home_dir = os.path.expanduser('~')
pic_dir = (home_dir + '/.apod_linux')

# check if dir already exists
if not os.path.exists(pic_dir):

    # if not, try to make it
    try:
        os.mkdir(pic_dir)
    except OSError as e:
        print("Could not create directory, freaking out...")
        sys.exit(1)

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

    try:

        # call gsettings to set the wallpaper
        # N.B. *** THIS PART IS GNOME SPECIFIC ***
        cmd = 'gsettings set org.gnome.desktop.background picture-uri file://' + pic_path
        cmd_array = cmd.split()
        subprocess.call(cmd_array)
    except OSError as e:
        print(str(e))

# -)
