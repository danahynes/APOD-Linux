#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: apod_linux_login.sh                                  /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# start the python script and fork it to run in the background
# N.B. the py script has a 30 second delay to wait for an internet connection,
# so forking it prevents login from hanging for that 30 seconds
# also downloading the pic may take a minute or two, so don't hang for that
/usr/bin/python3 /usr/bin/apod_linux.py &

# -)
