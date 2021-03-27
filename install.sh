#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: install.sh                                           /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# get name of current user for wake script
# N.B. don't run as root - set-wallpaper has an issue!!!
user=$(whoami)
if [ "${user}" == "root" ]
then

  # DO NOT RUN AS ROOT!!! set-wallpaper will try to delete your hard drive!!!
  echo 'Do not run install.sh as root, it breaks set-wallpaper!'
  exit 1
fi

# make the dir to store wallpaper
mkdir -p "/home/${user}/.apod_linux"

# put current user into a copy of wake script
touch ./apod_linux_wake2.sh
sed "s/REPLACE_USER/${user}/g" ./apod_linux_wake.sh > ./apod_linux_wake2.sh
sudo chmod +x ./apod_linux_wake2.sh
sudo chown root:root ./apod_linux_wake2.sh

# copy the scripts to their locations
sudo cp ./apod_linux_login.sh /etc/profile.d/
sudo mv ./apod_linux_wake2.sh /lib/systemd/system-sleep/apod_linux_wake.sh
sudo cp ./apod_linux.py /usr/bin/

# run the script now (runs as current user)
/etc/profile.d/apod_linux_login.sh

# -)
