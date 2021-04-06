#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# delete dirs/files from locations
sudo rm -rf "${HOME}/.apod_linux"
sudo rm -rf /etc/profile.d/apod_linux_login.sh
sudo rm -rf /usr/bin/apod_linux_unlock.sh
sudo rm -rf /usr/bin/apod_linux.py

# -)
