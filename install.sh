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

# stop the unlock listener (so we don't run it twice)
pkill -f "/usr/bin/apod_linux_unlock.sh"

# set the hidden dir where we will store our junk
INSTALL_DIR="${HOME}/.apod_linux"

# make the dir to store wallpaper and log (as user)
mkdir -p "${INSTALL_DIR}"

# install the conf file (as user)
cp ./apod_linux.conf "${INSTALL_DIR}"

# install the uninstaller
cp ./uninstall.sh "${INSTALL_DIR}"

# make a log file now in case anyone needs it before the py script runs (the py
# logging system will create the file if needed, but bash scripts won't)
touch "${INSTALL_DIR}/apod_linux.log"

# copy the scripts to their locations (needs admin hence sudo)
sudo cp "./apod_linux_login.sh" "/etc/profile.d"
sudo cp "./apod_linux_unlock.sh" "/usr/bin"
sudo cp "./apod_linux.py" "/usr/bin"
sudo cp "./apod_linux_caption.sh" "/usr/bin"

# run the script now (as user) (fork and release as child)
/etc/profile.d/apod_linux_login.sh & disown

# -)
