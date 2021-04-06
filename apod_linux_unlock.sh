#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: apod_linux_unlock.sh                                 /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# watch dbus for unlock event
# TODO: find out more about -y and -d switches
# -d is probably for --dest which is for where the messages go (to the login
# manager)
# TODO: shorten this to a grep -q statement
gdbus monitor -y -d org.freedesktop.login1 |
while read LINE
do

    # if we have an unlock event
    RES=$(echo "${LINE}" | grep -c "Session.Unlock")
    if [ "${RES}" == "1" ]
    then

      # do the thing now (at unlock)
      /usr/bin/apod_linux.py &
    fi
done

# -)
