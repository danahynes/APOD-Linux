<!----------------------------------------------------------------------------->
<!-- Filename: README.md                                       /          \  -->
<!-- Project : APOD_Linux                                     |     ()     | -->
<!-- Date    : 02/21/2019                                     |            | -->
<!-- Author  : Dana Hynes                                     |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# APOD_Linux

A small program that runs every day to set your wallpaper to NASA's Astronomy Picture of the Day.

![](screenshot.png)

# Installing

To install, clone the git repo:
```
foo@bar:~$ cd ~/Downloads
foo@bar:~$ git clone https://github.com/danahynes/APOD_Linux
foo@bar:~$ cd APOD_Linux
```

Once you do that, you can install by:
```
foo@bar:~$ sudo ./install.sh
```
You can also download the [latest release](http://github.com/danahynes/APOD_Linux/releases/latest), unzip it, and run the install.sh file from there.

# Uninstalling

To uninstall, go to the git directory and run:
```
foo@bar:~$ sudo ./uninstall.sh
```

# Notes

One of Linux's biggest drawing points is, in my opinion, also one of it's biggest drawbacks: modularity. There are umpteen different distros with as many backends, configurations, and desktop environments. This app was written and tested on elementaryOS 5 Hera, which is based on Ubuntu with the GNOME desktop. As such, it uses a program called gsettings to change the desktop wallpaper. If you are using a similar GNOME-based distro, it will probably work for you. But if you're using something with, say, a KDE desktop then it probably won't, and you'll need to change the part of the script that says "THIS PART IS GNOME SPECIFIC" to allow you to change the wallpaper. I don't have a KDE system installed, and I certainly don't have the time, energy, or patience to test for every Desktop Environment out there. Someday projects like freedesktop.org will give us a comman API to do common DE tasks like change the wallpaper or add icons to the desktop, but Linux is still a long way off in that regard to closed systems like Mac or Windows.

I know there is code out there to test for different DEs and set the wallpaper accordingly, but as I said I don't have any other working Linux setups right now, so if this app doesn't work for you, feel free to fork it, change it, and send a pull request or a DM and I'll look into it.

# -)
