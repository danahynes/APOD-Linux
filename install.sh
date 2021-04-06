#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: install.sh                                           /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# make sure we are installing as user (not root or sudo)
USER=$(whoami)
if [ "${USER}" == "root" ]
then
  echo "Do not run as root or with sudo"
  exit 1
fi

# make the dir to store wallpaper and log
mkdir -p "${HOME}/.apod_linux"

# copy the scripts to their locations
sudo cp ./apod_linux_login.sh /etc/profile.d/
sudo cp ./apod_linux_unlock.sh /usr/bin
sudo cp ./apod_linux.py /usr/bin

# run the script now (runs as current user)
/etc/profile.d/apod_linux_login.sh

# -)
