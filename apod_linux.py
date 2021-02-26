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
import urllib.request

# the hidden dir to store the wallpaper
home_dir = os.path.expanduser('~')
pic_dir = (home_dir + '/.apod_linux')

# check it it already exists
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
if not 'image' in media_type:
    print('Not an image, freaking out...')
    sys.exit(1)

# get the url to the actual image
pic_url = data['hdurl']

# check the file ext
file_ext = pic_url.split('.')[-1]

# format a new filename
file_name = ('wallpaper.' + file_ext)
pic_path = (pic_dir + '/' + file_name)

# download the full picture
urllib.request.urlretrieve(pic_url, pic_path)

# call gsettings to set the wallpaper
# N.B. THIS PART IS GNOME SPECIFIC
cmd = 'gsettings set org.gnome.desktop.background picture-uri file://' + pic_path
cmd = cmd.split()
subprocess.call(cmd)

# -)
