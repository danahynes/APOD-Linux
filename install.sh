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

# show some progress
# NB: first call with sudo to ask for password on its own line (aesthetics)
sudo echo "Installing APOD_Linux..."
echo "For license info see the LICENSE.txt file in this directory"

# stop the unlock listener (so we don't run it twice)
echo -n "Stopping unlock listener... "
sudo pkill -f "/usr/bin/apod_linux_unlock.sh"
echo "Done"

# set the hidden dir where we will store our junk
INSTALL_DIR="${HOME}/.apod_linux"

# make the dir to store wallpaper and log (as user)
echo -n "Creating install directory... "
mkdir -p "${INSTALL_DIR}"
echo "Done"

# install the conf file (as user)
echo -n "Copying config file... "
cp "./apod_linux.conf" "${INSTALL_DIR}"
echo "Done"

# install the uninstaller
echo -n "Copying uninstaller... "
cp "./uninstall.sh" "${INSTALL_DIR}"
echo "Done"

# make a log file now in case anyone needs it before the py script runs (the py
# logging system will create the file if needed, but bash scripts won't)
echo -n "Creating log file... "
touch "${INSTALL_DIR}/apod_linux.log"
echo "Done"

# copy the scripts to their locations (needs admin hence sudo)
echo -n "Copying scripts to their locations... "
sudo cp "./apod_linux_caption.sh" "/usr/bin"
sudo cp "./apod_linux_unlock.sh" "/usr/bin"
sudo cp "./apod_linux.py" "/usr/bin"
sudo cp "./apod_linux_login.sh" "/etc/profile.d"
echo "Done"

# install ttk gui and themes
echo "Installing GUI "
sudo cp "./gui/apod_linux_config.py" "/usr/bin"
sudo cp "./gui/apod_linux_icon.png" "/usr/share/icons/hicolor/128x128/apps"
cp "./gui/apod_linux.desktop" "${HOME}/.local/share/applications"
echo "Done"

# run the script now (as user) (fork and release as child)
echo -n "Running APOD_Linux now... "
/usr/bin/apod_linux_login.sh
echo "Done"

# show that we are done
echo "APOD_Linux installed"

# -)
