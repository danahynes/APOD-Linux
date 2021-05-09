#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: apod_linux_login.sh                                  /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# let the log know whats up
echo "Login" >> "${HOME}/.apod_linux/apod_linux.log"

# do the thing now (at login)
python3 /usr/bin/apod_linux.py & disown

# start listening for unlock (fork and disown to allow the login shell to exit)
# N.B. at this point any previous script(s) should be stopped,
/usr/bin/apod_linux_unlock.sh & disown

# -)
