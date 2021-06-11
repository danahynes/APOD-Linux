<!----------------------------------------------------------------------------->
<!-- Filename: README.md                                       /          \  -->
<!-- Project : APOD_Linux                                     |     ()     | -->
<!-- Date    : 02/21/2019                                     |            | -->
<!-- Author  : Dana Hynes                                     |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# APOD_Linux
## "It mostly works™"

A small program that runs at every login/unlock to set your wallpaper to
NASA's Astronomy Picture of the Day.

![](screenshot.jpg)

# Installing

To install, clone the git repo:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/danahynes/APOD_Linux
foo@bar:~/Downloads$ cd APOD_Linux
```

Once you do that, you can install by:
```bash
foo@bar:~/Downloads/APOD_Linux$ ./install.sh
```
You can also download the
[latest release](http://github.com/danahynes/APOD_Linux/releases/latest), unzip
it, and run the *install.sh* file from there.

**DO NOT USE SUDO TO INSTALL!**

There is a bug in *set-wallpaper* that causes it to try and delete everything in
your current folder if run as sudo. This is because it's looking for an *env*
variable that is not set. Bad, right? WTF!!! Installing without sudo
seems to work. The install script will warn you if you use sudo, so you should
be OK.

# Uninstalling

To uninstall, go to the *~/.apod_linux* directory and run:
```bash
foo@bar:~/.apod_linux$ ./uninstall.sh
```
You can safely use sudo here, but it's not necessary.

Or you can remove the files manually:
```bash
foo@bar:~$ pkill -f "/usr/bin/apod_linux_unlock.sh"
foo@bar:~$ sudo rm -rf "~/.apod_linux"
foo@bar:~$ sudo rm -f "/etc/profile.d/apod_linux_login.sh"
foo@bar:~$ sudo rm -f "/usr/bin/apod_linux_unlock.sh"
foo@bar:~$ sudo rm -f "/usr/bin/apod_linux.py"
foo@bar:~$ sudo rm -f "/usr/bin/apod_linux_caption.sh"
```

# Update

The image can now have a caption based on the
*~/.apod_linux/apod_linux.conf* file.
If the file contains the line *CAPTION=1*, a caption will be applied to the
wallpaper. The file may also contain the line *POSITION=XX* with XX equaling
values including "TR" (top right), "BR" (bottom right), "TL" (top left), or "BL"
(bottom left). Other options include the text color and the caption bubble's
background, width of the caption, font size, border size, corner rounding, etc.

The default is to put the caption in the bottom right, with white text on a
black background with 75% opacity.

Lines can be commented out using a hash mark (#) at the beginning of the line.
White space is allowed at the beginning and end of a line, and around the equals
sign. See the *~/.apod_linux/apod_linux.conf* file for more info.


# Notes

Originally, this program tried to use *anacron* to run a script once a day. But,
I could not get the *anacron* code to work, mostly because *anacron* wants to
run as root, and  my code (mostly *set-wallpaper*) wants to run as the current
user. So I gave up and made it run when a user logs in, or unlocks the screen.
It then waits 30 seconds for an internet connection, downloads the latest APOD
picture, and sets that as the wallpaper.

The wallpaper may not change based on the following conditions:
1. You do not have an internet connection.
2. The Astronomy Picture of the Day is not a picture (sometimes it's a video,
and recently they posted an interactive GIF [fun, but won't work as wallpaper]).
3. Any of the above and you have never downloaded a working picture.

The script does try to fall back to the last working picture if any of the above
happen, however if it can't, it won't change your wallpaper so your system
settings should still apply.

You can check the log at *~/.apod_linux/apod_linux.log* to find out if
the script is working, and what it's doing.

If you're like me, and use a laptop, you probably don't log in/out very often,
but only close your laptop lid to put the system to sleep. Running the script
when a user logs in after sleep/wake was tricky, as Linux does not consider this
an actual login, only a speedbump in the current session (you're not actually
logging in, only unlocking the screen). That's one reason I wanted the script to
run every hour, but this caused problems after I set up my laptop to dual-boot
with Windows (along with other issues, so probably not the script's fault). The
script would hang the login process, even with forking.

The solution to this was to run the script after unlocking. For that, I
needed a script that monitored for an unlock event. Luckily I found some good
examples on the interwebs, and the result is *apod_linux_unlock.sh*.

One of Linux's biggest drawing points is, in my opinion, also one of it's
biggest drawbacks: modularity. There are umpteen different distros with as many
backends, configurations, and desktop environments. This app was written and
tested on elementaryOS 5 Hera, which is based on Ubuntu with the GNOME desktop.
As such, it uses a program called *set-wallpaper* to change the desktop
wallpaper. But if you're using another distro, you'll need to change the part of
the script that says "THIS PART IS ELEMENTARY SPECIFIC" to allow you to change
the wallpaper. I don't have another system installed, and I certainly don't have
the time, energy, or patience to test for every Desktop Environment out there.

I know there is code out there to test for different DEs and set the wallpaper
accordingly, but as I said I don't have any other working Linux setups right
now, so if this app doesn't work for you, feel free to fork it, change it, and
send a pull request or a DM and I'll look into it.

Here is a flowchart of what the various scripts do:

![](apod_linux_flow.jpg)

TODO:

1. Set wallpaper on non-elementaryOS desktops

# -)
