#------------------------------------------------------------------------------#
# Filename: asus_l410m_numpad.py                                /          \  #
# Project : Asus_L410M_Numpad                                   |     ()     | #
# Date    : 02/17/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# imports
import json
import os
import subprocess
import urllib.request

# the url to load JSON from
url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'

# get the JSON and format it
response = urllib.request.urlopen(url)
byte_data = response.read()
data = json.loads(byte_data)

# the hidden dir to store the wallpaper
home_dir = os.path.expanduser('~')
pic_dir = (home_dir + '/.apod_linux')

# check it it already exists
if not os.path.exists(pic_dir):

    # if not, try to make it
    try:
        os.mkdir(pic_dir)
    except OSError as e:
        print("Could not create directory, exiting...")
        sys.exit(1)

# make sure it's an image (sometimes it's a video)
media_type = data['media_type']
if 'image' in media_type:

    # get the url to the actual image
    pic_url = data['hdurl']

    # check the file ext
    file_ext = pic_url.split('.')[-1]

    # format a new filename
    file_name = 'wallpaper.' + file_ext

    # download the full picture
    urllib.request.urlretrieve(pic_url, pic_dir + '/' + file_name)

    # call gsettings to set the wallpaper
    subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri',
        'file://' + pic_dir + '/' + file_name])

# if it's a video
else:
    print('Not an image, exiting...')
    sys.exit(1)

# -)
