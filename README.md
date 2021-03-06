<!----------------------------------------------------------------------------->
<!-- Filename: README.md                                       /          \  -->
<!-- Project : APOD_Linux                                     |     ()     | -->
<!-- Date    : 02/21/2019                                     |            | -->
<!-- Author  : Dana Hynes                                     |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# APOD_Linux
## "It mostly works™"

A small program that runs at every login to set your wallpaper to NASA's Astronomy Picture of the Day.

![](screenshot.png)

# Installing

To install, clone the git repo:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/danahynes/APOD_Linux
foo@bar:~/Downloads$ cd APOD_Linux
```

Once you do that, you can install by:
```bash
foo@bar:~/Downloads/APOD_Linux$ sudo ./install.sh
```
You can also download the [latest release](http://github.com/danahynes/APOD_Linux/releases/latest), unzip it, and run the install.sh file from there.

You need to log out and log back in to start the script.
I haven't figured out a reliable way to start the script from the install file. -(

# Uninstalling

To uninstall, go to the git directory and run:
```bash
foo@bar:~/Downloads/APOD_Linux$ sudo ./uninstall.sh
```
Or you can remove the files manually:
```bash
foo@bar:~$ sudo rm /usr/bin/apod_linux.py
foo@bar:~$ sudo rm /etc/profile.d/apod_linux.sh
```

# Notes

Originally, this program tried to use *anacron* to run a script once a day. But, I could not get the *anacron* code to work, mostly because *anacron* wants to run as root, and all my code (mostly *gsettings*) wants to run as the current user. So I gave up and made it run when a user logs in. It then waits 30 seconds for an internet connection, downloads the latest APOD picture, and sets that as the wallpaper.

One of Linux's biggest drawing points is, in my opinion, also one of it's biggest drawbacks: modularity. There are umpteen different distros with as many backends, configurations, and desktop environments. This app was written and tested on elementaryOS 5 Hera, which is based on Ubuntu with the GNOME desktop. As such, it uses a program called *gsettings* to change the desktop wallpaper. If you are using a similar GNOME-based distro, it will probably work for you. But if you're using something with, say, a KDE desktop then it probably won't, and you'll need to change the part of the script that says "THIS PART IS GNOME SPECIFIC" to allow you to change the wallpaper. I don't have a KDE system installed, and I certainly don't have the time, energy, or patience to test for every Desktop Environment out there.

I know there is code out there to test for different DEs and set the wallpaper accordingly, but as I said I don't have any other working Linux setups right now, so if this app doesn't work for you, feel free to fork it, change it, and send a pull request or a DM and I'll look into it.

# -)
