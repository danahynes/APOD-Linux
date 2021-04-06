#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: apod_linux_login.sh                                  /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# do the thing now (at login)
/usr/bin/apod_linux.py &

# start unlock watch script
/usr/bin/apod_linux_unlock.sh &

# -)
