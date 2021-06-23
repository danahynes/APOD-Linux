#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Filename: apod_linux_config_orig.py                            /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 05/30/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# imports
import os
import subprocess
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk

# find the config file
home_dir = os.path.expanduser("~")
pic_dir = os.path.join(home_dir, ".apod_linux")
conf_file = os.path.join(pic_dir, "apod_linux.conf")

# map position codes to user strings
dict_position = {
    "TL":"Top Left",
    "TR":"Top Right",
    "BL":"Bottom Left",
    "BR":"Bottom Right",
    "C":"Center"
}

# load values from config file
def load_config():

    # check if config file exists
    if os.path.exists(conf_file):

        # open config file and get all lines
        with open(conf_file, "r") as f:
            lines = f.readlines()

            # try to find a value in the conf file
            for line in lines:

                # strip the line
                line = line.strip()

                # ignore commented or blank lines
                if line.startswith("#") or line == "":
                    continue

                # split lines at equals sign
                key_val_array = line.split("=")

                # ignore trailing comments
                key = key_val_array[0].strip().upper()
                key = key.split("#")[0].strip()
                val = key_val_array[1].strip().upper()
                val = val.split("#")[0].strip()

                # set values for keys
                if "DELAY" in key:
                    var_delay.set(val)

                if "CAPTION" in key:
                    var_caption.set(val)

                if "POSITION" in key:
                    for short_pos, long_pos in dict_position.items():
                        if val == short_pos:
                            var_position.set(long_pos)

                if "COLOR" in key:
                    colors = val.split("(")[1].split(")")[0]
                    color_vars = colors.split(",")
                    var_color_r.set(color_vars[0])
                    var_color_g.set(color_vars[1])
                    var_color_b.set(color_vars[2])
                    var_color_a.set(int(float(color_vars[3]) * 100))

                if "BACKGROUND" in key:
                    bgs = val.split("(")[1].split(")")[0]
                    bg_vars = bgs.split(",")
                    var_bg_r.set(bg_vars[0])
                    var_bg_g.set(bg_vars[1])
                    var_bg_b.set(bg_vars[2])
                    var_bg_a.set(int(float(bg_vars[3]) * 100))

                if "WIDTH" in key:
                    var_width.set(val)

                if "FONT_SIZE" in key:
                    var_font_size.set(val)

                if "CORNER_RADIUS" in key:
                    var_corner_radius.set(val)

                if "BORDER" in key:
                    var_border.set(val)

                if "TOP_PADDING" in key:
                    var_top_padding.set(val)

                if "BOTTOM_PADDING" in key:
                    var_bottom_padding.set(val)

                if "SIDE_PADDING" in key:
                    var_side_padding.set(val)

# save values to file on ok/apply
def save_config():

    # open or create config file
    with open(conf_file, "w+") as f:

        # TODO: find line for key, replace value

        f.write("# DO NOT EDIT THIS FILE BY HAND!\n\n")

        # start writing options
        f.write("DELAY=" + str(var_delay.get()) + "\n")
        f.write("CAPTION=" + str(var_caption.get()) + "\n")

        # fudge the position option from the array
        val = var_position.get()
        for short_pos, long_pos in dict_position.items():
            if val == long_pos:
                val = short_pos
        f.write("POSITION=" + val + "\n")

        # set the color alpha to a percent
        var_color_a_float = (float(var_color_a.get()) / 100)
        f.write(
            "COLOR=" +
            '\"rgba(' +
            str(var_color_r.get()) + "," +
            str(var_color_g.get()) + "," +
            str(var_color_b.get()) + "," +
            str(var_color_a_float) +
            ')\"\n'
        )

        # set the background alpha to a percent
        var_bg_a_float = (float(var_bg_a.get()) / 100)
        f.write(
            "BACKGROUND=" +
            '\"rgba(' +
            str(var_bg_r.get()) + "," +
            str(var_bg_g.get()) + "," +
            str(var_bg_b.get()) + "," +
            str(var_bg_a_float) +
            ')\"\n'
        )

        # the rest of the options should be easy
        f.write("WIDTH=" + str(var_width.get()) + "\n")
        f.write("FONT_SIZE=" + str(var_font_size.get()) + "\n")
        f.write("CORNER_RADIUS=" + str(var_corner_radius.get()) + "\n")
        f.write("BORDER=" + str(var_border.get()) + "\n")
        f.write("TOP_PADDING=" + str(var_top_padding.get()) + "\n")
        f.write("BOTTOM_PADDING=" + str(var_bottom_padding.get()) + "\n")
        f.write("SIDE_PADDING=" + str(var_side_padding.get()) + "\n")

# validate function (called whenever a character is typed/pasted in a spinbox)
def validate(input):

    # NB: we don't do any replacements in validate because that would cause
    # recursion in the validate function (it's done in focusout below)

    # if typed char is a digit or blank, it's valid
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False

# function to clean up/clamp values in spin boxes
def focusout(event):

    # get the widget that lost focus
    widget = event.widget

    # get the text of the widget
    text = widget.get()

    # strip leading zeroes and ensure valid text
    text = text.lstrip("0")
    if text == None or text == "":
        text = "0"

    # clamp the new value
    val = int(text)
    min = int(widget.config("from")[4])
    max = int(widget.config("to")[4])

    # clamp value
    if val < min:
        val = min
    elif val > max:
        val = max

    # set the new text
    widget.delete(0, END)
    widget.insert(0, val)

# enable controls based on whether we want a caption
def checkbox_cmd():
    val = var_caption.get()
    if val:
        combo_position.configure(state="readonly")
        spin_color_r.configure(state="normal")
        spin_color_g.configure(state="normal")
        spin_color_b.configure(state="normal")
        spin_color_a.configure(state="normal")
        spin_bg_r.configure(state="normal")
        spin_bg_g.configure(state="normal")
        spin_bg_b.configure(state="normal")
        spin_bg_a.configure(state="normal")
        spin_width.configure(state="normal")
        spin_font_size.configure(state="normal")
        spin_corner.configure(state="normal")
        spin_border.configure(state="normal")
        spin_top_padding.configure(state="normal")
        spin_bottom_padding.configure(state="normal")
        spin_side_padding.configure(state="normal")
    else:
        combo_position.configure(state="disabled")
        spin_color_r.configure(state="disabled")
        spin_color_g.configure(state="disabled")
        spin_color_b.configure(state="disabled")
        spin_color_a.configure(state="disabled")
        spin_bg_r.configure(state="disabled")
        spin_bg_g.configure(state="disabled")
        spin_bg_b.configure(state="disabled")
        spin_bg_a.configure(state="disabled")
        spin_width.configure(state="disabled")
        spin_font_size.configure(state="disabled")
        spin_corner.configure(state="disabled")
        spin_border.configure(state="disabled")
        spin_top_padding.configure(state="disabled")
        spin_bottom_padding.configure(state="disabled")
        spin_side_padding.configure(state="disabled")

# callback for the OK button
def button_ok_cmd():
    save_config()
    main_window.destroy()

# callback for the Cancel button
def button_cancel_cmd():
    main_window.destroy()

# callback for the Apply button
def button_apply_cmd():
    save_config()

    # only run once, no listener
    cmd = "python3 /usr/bin/apod_linux.py & disown"
    array = cmd.split()

    # non-blocking subprocess
    subprocess.Popen(array)

# create the main window (titlebar and frame)
# theme list - https://ttkthemes.readthedocs.io/en/latest/themes.html
main_window = ThemedTk(theme="equilux")
main_window.title("APOD_Linux config")
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(0, weight=1)
main_window.resizable(False, False)

# set main womdow's icon
icon = PhotoImage(
    file = "/usr/share/icons/hicolor/128x128/apps/apod_linux_icon.png")
main_window.iconphoto(False, icon)

# register the validate function with the main window (%S is the user input,
# whether typed or pasted)
validate_func = (main_window.register(validate), "%S")

# set variables/defults
# NB: needs to be done after main window creation
var_delay = IntVar()
var_delay.set(30)
var_caption = IntVar()
var_caption.set(1)
var_position = StringVar()
var_position.set("Bottom Right")
var_color_r = IntVar()
var_color_r.set(255)
var_color_g = IntVar()
var_color_g.set(255)
var_color_b = IntVar()
var_color_b.set(255)
var_color_a = IntVar()
var_color_a.set(100)
var_bg_r = IntVar()
var_bg_r.set(0)
var_bg_g = IntVar()
var_bg_g.set(0)
var_bg_b = IntVar()
var_bg_b.set(0)
var_bg_a = IntVar()
var_bg_a.set(75)
var_width = IntVar()
var_width.set(500)
var_font_size = IntVar()
var_font_size.set(15)
var_corner_radius = IntVar()
var_corner_radius.set(15)
var_border = IntVar()
var_border.set(20)
var_top_padding = IntVar()
var_top_padding.set(50)
var_bottom_padding = IntVar()
var_bottom_padding.set(10)
var_side_padding = IntVar()
var_side_padding.set(10)

# create the content view
content = Frame(main_window)
content.grid(column=0, row=0, sticky=(N, S, W, E))

# create gui
label_delay = Label(content, text="Delay (0-120):", anchor=E)
label_delay.grid(column=0, row=0, sticky=(E, W), padx=5, pady=5)

spin_delay  = Spinbox(content, from_=0, to=120, textvariable=var_delay,
    validate="all", validatecommand=validate_func)
spin_delay.grid(column=1, row=0, sticky=(E, W), padx=5, pady=5)
spin_delay.bind("<FocusOut>", focusout)

check_caption= Checkbutton(content, text="Use caption", variable=var_caption,
    command=checkbox_cmd)
check_caption.grid(column=1, row=2, sticky=(E, W), padx=5, pady=5)

label_position  = Label(content, text="Position:", anchor=E)
label_position.grid(column=0, row=3, sticky=(E, W), padx=5, pady=5)

combo_position = Combobox(content, textvariable=var_position, state="readonly",
    values=("Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center"))
combo_position.grid(column=1, row=3, sticky=(E, W), padx=5, pady=5)

frame_color = Frame(content)
frame_color.grid(column=0, row=4, columnspan=2, sticky=(E, W))
frame_color.columnconfigure(1, weight=1)

label_color = Label(frame_color, text="Text color", anchor=W)
label_color.grid(column=0, row=0, sticky=(W), padx=5, pady=5)

frame_div_color = Frame(frame_color, relief="sunken", height=2)
frame_div_color.grid(column=1, row=0, sticky=(E, W), padx=5, pady=5)

label_color_r = Label(content, text="Red (0-255):", anchor=E)
label_color_r.grid(column=0, row=5, sticky=(E, W), padx=5,pady=5)

spin_color_r = Spinbox(content, from_=0, to=255, textvariable=var_color_r,
    validate="all", validatecommand=validate_func)
spin_color_r.grid(column=1, row=5, sticky=(E, W),  padx=5,pady=5)
spin_color_r.bind("<FocusOut>", focusout)

label_color_g = Label(content, text="Green (0-255):", anchor=E)
label_color_g.grid(column=0, row=6, sticky=(E, W), padx=5,pady=5)

spin_color_g = Spinbox(content, from_=0, to=255, textvariable=var_color_g,
    validate="all", validatecommand=validate_func)
spin_color_g.grid(column=1, row=6, sticky=(E, W), padx=5,pady=5)
spin_color_g.bind("<FocusOut>", focusout)

label_color_b = Label(content, text="Blue (0-255):", anchor=E)
label_color_b.grid(column=0, row=7, sticky=(E, W), padx=5,pady=5)

spin_color_b = Spinbox(content, from_=0, to=255, textvariable=var_color_b,
    validate="all", validatecommand=validate_func)
spin_color_b.grid(column=1, row=7, sticky=(E, W), padx=5, pady=5)
spin_color_b.bind("<FocusOut>", focusout)

label_color_a = Label(content, text="Alpha (0-100):", anchor=E)
label_color_a.grid(column=0, row=8, sticky=(E), padx=5,pady=5)

spin_color_a = Spinbox(content, from_=0, to=100, textvariable=var_color_a,
    validate="all", validatecommand=validate_func)
spin_color_a.grid(column=1, row=8, sticky=(E, W), padx=5,pady=5)
spin_color_a.bind("<FocusOut>", focusout)

frame_bg = Frame(content)
frame_bg.grid(column=0, row=9, columnspan=2, sticky=(E, W))
frame_bg.columnconfigure(1, weight=1)

label_bg = Label(frame_bg, text="Background color", anchor=W)
label_bg.grid(column=0, row=0, sticky=(W), padx=5, pady=5)

frame_div_bg = Frame(frame_bg, relief="sunken", height=2)
frame_div_bg.grid(column=1, row=0, sticky=(E, W), padx=5, pady=5)

label_bg_r = Label(content, text="Red (0-255):", anchor=E)
label_bg_r.grid(column=0, row=10, sticky=(E, W), padx=5,pady=5)

spin_bg_r = Spinbox(content, from_=0, to=255, textvariable=var_bg_r,
    validate="all", validatecommand=validate_func, width=3)
spin_bg_r.grid(column=1, row=10, sticky=(E, W), padx=5,pady=5)
spin_bg_r.bind("<FocusOut>", focusout)

label_bg_g = Label(content, text="Green (0-255):", anchor=E)
label_bg_g.grid(column=0, row=11, sticky=(E, W), padx=5,pady=5)

spin_bg_g = Spinbox(content, from_=0, to=255, textvariable=var_bg_g,
    validate="all", validatecommand=validate_func, width=3)
spin_bg_g.grid(column=1, row=11, sticky=(E, W), padx=5,pady=5)
spin_bg_g.bind("<FocusOut>", focusout)

label_bg_b = Label(content, text="Blue (0-255):", anchor=E)
label_bg_b.grid(column=0, row=12, sticky=(E, W), padx=5,pady=5)

spin_bg_b = Spinbox(content, from_=0, to=255, textvariable=var_bg_b,
    validate="all", validatecommand=validate_func, width=3)
spin_bg_b.grid(column=1, row=12, sticky=(E, W), padx=5,pady=5)
spin_bg_b.bind("<FocusOut>", focusout)

label_bg_a = Label(content, text="Alpha (0-100):", anchor=E)
label_bg_a.grid(column=0, row=13, sticky=(E, W), padx=5,pady=5)

spin_bg_a = Spinbox(content, from_=0, to=100, textvariable=var_bg_a,
    validate="all", validatecommand=validate_func, width=3)
spin_bg_a.grid(column=1, row=13, sticky=(E, W), padx=5,pady=5)
spin_bg_a.bind("<FocusOut>", focusout)

frame_div_other = Frame(content, relief="sunken", height=2)
frame_div_other.grid(column=0, columnspan=2, row=14, sticky=(E, W), padx=5,
    pady=5)

label_width = Label(content, text="Width (0-2000):", anchor=E)
label_width.grid(column=0, row=15, sticky=(E, W), padx=5, pady=5)

spin_width = Spinbox(content, from_=0, to=2000, textvariable=var_width,
    validate="all", validatecommand=validate_func)
spin_width.grid(column=1, row=15, sticky=(E, W), padx=5, pady=5)
spin_width.bind("<FocusOut>", focusout)

label_font_size = Label(content, text="Font size (0-50):", anchor=E)
label_font_size.grid(column=0, row=16, sticky=(E, W), padx=5, pady=5)

spin_font_size = Spinbox(content, from_=0, to=50, textvariable=var_font_size,
    validate="all", validatecommand=validate_func)
spin_font_size.grid(column=1, row=16, sticky=(E, W), padx=5, pady=5)
spin_font_size.bind("<FocusOut>", focusout)

label_corner = Label(content, text="Corner radius (0-50):", anchor=E)
label_corner.grid(column=0, row=17, sticky=(E, W), padx=5, pady=5)

spin_corner = Spinbox(content, from_=0, to=50, textvariable=var_corner_radius,
    validate="all", validatecommand=validate_func)
spin_corner.grid(column=1, row=17, sticky=(E, W), padx=5, pady=5)
spin_corner.bind("<FocusOut>", focusout)

label_border = Label(content, text="Border (0-50):", anchor=E)
label_border.grid(column=0, row=18, sticky=(E, W), padx=5, pady=5)

spin_border = Spinbox(content, from_=0, to=50, textvariable=var_border,
    validate="all", validatecommand=validate_func)
spin_border.grid(column=1, row=18, sticky=(E, W), padx=5, pady=5)
spin_border.bind("<FocusOut>", focusout)

label_top_padding = Label(content, text="Top padding (0-50):", anchor=E)
label_top_padding.grid(column=0, row=19, sticky=(E, W), padx=5, pady=5)

spin_top_padding = Spinbox(content, from_=0, to=50,
    textvariable=var_top_padding, validate="all", validatecommand=validate_func)
spin_top_padding.grid(column=1, row=19, sticky=(E, W), padx=5, pady=5)
spin_top_padding.bind("<FocusOut>", focusout)

label_bottom_padding = Label(content, text="Bottom padding (0-50):", anchor=E)
label_bottom_padding.grid(column=0, row=20, sticky=(E, W), padx=5, pady=5)

spin_bottom_padding = Spinbox(content, from_=0, to=50,
    textvariable=var_bottom_padding, validate="all",
    validatecommand=validate_func)
spin_bottom_padding.grid(column=1, row=20, sticky=(E, W), padx=5, pady=5)
spin_bottom_padding.bind("<FocusOut>", focusout)

label_side_padding = Label(content, text="Side padding (0-50):", anchor=E)
label_side_padding.grid(column=0, row=21, sticky=(E, W), padx=5, pady=5)

spin_side_padding = Spinbox(content, from_=0, to=50,
    textvariable=var_side_padding, validate="all",
    validatecommand=validate_func)
spin_side_padding.grid(column=1, row=21, sticky=(E, W), padx=5, pady=5)
spin_side_padding.bind("<FocusOut>", focusout)

# create separator
frame_div_btn = Frame(content, relief="sunken", height=2)
frame_div_btn.grid(column=0, row=22, columnspan=2, sticky=(E, W), padx=0,
    pady=10)

# create a panel to hold the buttons
frame_buttons = Frame(content)
frame_buttons.grid(column=0, row=23, columnspan=2, sticky=(N, S, E, W))
frame_buttons.columnconfigure(0, weight=1)
frame_buttons.columnconfigure(1, weight=1)
frame_buttons.columnconfigure(2, weight=1)
frame_buttons.rowconfigure(0, weight=1)

# create buttons
btn_ok = Button(frame_buttons, text="OK", command=button_ok_cmd)
btn_ok.grid(column=0, row=0, padx=5, pady=5)

btn_cancel = Button(frame_buttons, text="Cancel", command=button_cancel_cmd)
btn_cancel.grid(column=1, row=0, padx=5, pady=5)

btn_apply = Button(frame_buttons, text="Apply", command=button_apply_cmd)
btn_apply.grid(column=2, row=0, padx=5, pady=5)

# load defaults here
load_config()

# update gui based on checkbox
checkbox_cmd()

# start the program by showing the main window
main_window.mainloop()

# -)
