#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# delete the scripts
sudo rm -rf /usr/bin/apod_linux.py
sudo rm -rf /etc/cron.daily/apod_linux.#!/bin/sh

# N.B. we leave the hidden directory with the current wallpaper in it so the
# desktop doesn't go black

# -)
