#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# N.B. we leave the hidden directory with the current wallpaper in it so the
# desktop doesn't go black

# delete files from locations
sudo rm /usr/bin/apod_linux.py
sudo rm /etc/profile.d/apod_linux.sh

# -)
