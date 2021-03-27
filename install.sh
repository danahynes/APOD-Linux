#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: install.sh                                           /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# get name of current user for wake script
user=$(whoami)
if [ "${user}" == "root" ]
then

  # DO NOT RUN AS ROOT!!! set-wallpaper will try to delete your hard drive!!!
  echo 'Do not run as root, it breaks set-wallpaper!'
  exit 1
fi

# make the dir to store wallpaper
mkdir -p "/home/${user}/.apod_linux"
sudo chown ${user}:${user} "/home/${user}/.apod_linux"

# put current user into a copy of wake script
touch ./apod_linux_wake2.sh
sed "s/REPLACE_USER/${user}/g" ./apod_linux_wake.sh > ./apod_linux_wake2.sh

# copy the script for login
if [ -d "/etc/profile.d" ]
then
  sudo cp ./apod_linux_login.sh /etc/profile.d/
else
  echo "/etc/profile.d does not exist, freaking out..."
  exit 1
fi

# change permissions and owner of apod_linux_wake
sudo chmod +x ./apod_linux_wake2.sh
sudo chown root:root ./apod_linux_wake2.sh

# move the script copy for wake
if [ -d "/lib/systemd/system-sleep" ]
then
  sudo mv ./apod_linux_wake2.sh /lib/systemd/system-sleep/apod_linux_wake.sh
else
  echo "/lib/systemd/system-sleep does not exist, freaking out..."
  exit 1
fi

# copy the script for changing the wallpaper
if [ -d "/usr/bin" ]
then
  sudo cp ./apod_linux.py /usr/bin/
else
  echo "/usr/bin does not exist, freaking out..."
  exit 1
fi

# run the script now (runs as current user)
#su -s $(/usr/bin/env bash) -c /etc/profile.d/apod_linux_login.sh ${user}
su -s /bin/bash -c /etc/profile.d/apod_linux_login.sh ${user}

# -)
