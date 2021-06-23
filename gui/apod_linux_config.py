#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Filename: apod_linux_config.py                                 /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 06/23/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os
import subprocess

# find the config file
home_dir = os.path.expanduser("~")
pic_dir = os.path.join(home_dir, ".apod_linux")
conf_file = os.path.join(pic_dir, "apod_linux.conf")

class MyWindow(Gtk.Window):

    position_map = {
        "TL" : "Top Left",
        "TR" : "Top Right",
        "BL" : "Bottom Left",
        "BR" : "Bottom Right",
        "C"  : "Center"
    }

    def_enabled = 1
    def_delay = 30
    def_use_caption = 1

    def_text_r = 255
    def_text_g = 255
    def_text_b = 255
    def_text_a = 100
    def_bg_r = 0
    def_bg_g = 0
    def_bg_b = 0
    def_bg_a = 75

    def_position = "BR"
    def_width = 500
    def_font_size = 15
    def_corner = 15
    def_border = 20
    def_top_pad = 50
    def_bottom_pad = 10
    def_side_pad = 10

    def __init__(self):
        Gtk.Window.__init__(self, title="APOD_Linux")

        # the padding between the window edge and the content
        self.set_border_width(12)

        # set new width and default (fit) height
        self.set_default_size(400, -1)
        self.set_resizable(False)

        # create the stach and set props
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.NONE)

        # create the switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        # create a box for the switcher that keeps it centered horizontally
        hbox_switcher = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_switcher.pack_start(stack_switcher, True, False, 0)

        # the first tab

        # create a grid with inter-spacig
        grid_general = Gtk.Grid()
        grid_general.set_row_spacing(20)
        grid_general.set_column_spacing(20)

        # add a checkbox
        self.check_enabled = Gtk.CheckButton(label="Enable APOD")
        self.check_enabled.connect("clicked", self.check_enabled_clicked)
        grid_general.attach(self.check_enabled, 1, 0, 1, 1)

        # add a label
        label_delay = Gtk.Label(label="Delay (0-60):")
        grid_general.attach(label_delay, 0, 1, 1, 1)

        # add a spinbox that grows horisontally
        adj_delay = Gtk.Adjustment(
                0.0,
                0.0,
                60.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_delay = Gtk.SpinButton(adjustment=adj_delay, hexpand=True)
        self.spin_delay.set_numeric(True)
        grid_general.attach(self.spin_delay, 1, 1, 1, 1)

        # add another checkbox
        self.check_caption = Gtk.CheckButton(label="Use caption")
        self.check_caption.connect("clicked", self.check_caption_clicked)
        grid_general.attach(self.check_caption, 1, 2, 1, 1)

        # add the grid to the stack with a name and a title
        stack.add_titled(grid_general, "general", "General")

        # the second tab

        # create a grid with inter-spacig
        grid_colors = Gtk.Grid()
        grid_colors.set_row_spacing(20)
        grid_colors.set_column_spacing(20)

        label_text = Gtk.Label()
        label_text.set_markup("<b>Text</b>")

        sep_text = Gtk.HSeparator()

        vbox_sep_text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox_sep_text.pack_start(sep_text, True, False, 0)

        hbox_text = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox_text.pack_start(label_text, False, False, 0)
        hbox_text.pack_start(vbox_sep_text, True, True, 0)
        grid_colors.attach(hbox_text, 0, 0, 2, 1)

        label_text_r = Gtk.Label(label="Red (0-255):")
        label_text_r.set_alignment(1, 0)
        grid_colors.attach(label_text_r, 0, 1, 1, 1)

        adj_text_r = Gtk.Adjustment(
                0.0,
                0.0,
                255.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_text_r = Gtk.SpinButton(adjustment=adj_text_r, hexpand=True)
        self.spin_text_r.set_numeric(True)
        grid_colors.attach(self.spin_text_r, 1, 1, 1, 1)

        label_text_g = Gtk.Label(label="Green (0-255):")
        label_text_g.set_alignment(1, 0)
        grid_colors.attach(label_text_g, 0, 2, 1, 1)

        adj_text_g = Gtk.Adjustment(
                0.0,
                0.0,
                255.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_text_g = Gtk.SpinButton(adjustment=adj_text_g, hexpand=True)
        self.spin_text_g.set_numeric(True)
        grid_colors.attach(self.spin_text_g, 1, 2, 1, 1)

        label_text_b = Gtk.Label(label="Blue (0-255):")
        label_text_b.set_alignment(1, 0)
        grid_colors.attach(label_text_b, 0, 3, 1, 1)

        adj_text_b = Gtk.Adjustment(
                0.0,
                0.0,
                255.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_text_b = Gtk.SpinButton(adjustment=adj_text_b, hexpand=True)
        self.spin_text_b.set_numeric(True)
        grid_colors.attach(self.spin_text_b, 1, 3, 1, 1)

        label_text_a = Gtk.Label(label="Alpah % (0-100):")
        label_text_a.set_alignment(1, 0)
        grid_colors.attach(label_text_a, 0, 4, 1, 1)

        adj_text_a = Gtk.Adjustment(
                0.0,
                0.0,
                100.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_text_a = Gtk.SpinButton(adjustment=adj_text_a, hexpand=True)
        self.spin_text_a.set_numeric(True)
        grid_colors.attach(self.spin_text_a, 1, 4, 1, 1)

        label_bg = Gtk.Label()
        label_bg.set_markup("<b>Background</b>")

        sep_bg = Gtk.HSeparator()

        vbox_sep_bg = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox_sep_bg.pack_start(sep_bg, True, False, 0)

        hbox_bg = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox_bg.pack_start(label_bg, False, False, 0)
        hbox_bg.pack_start(vbox_sep_bg, True, True, 0)
        grid_colors.attach(hbox_bg, 0, 5, 2, 1)

        label_bg_r = Gtk.Label(label="Red (0-255):")
        label_bg_r.set_alignment(1, 0)
        grid_colors.attach(label_bg_r, 0, 6, 1, 1)

        adj_bg_r = Gtk.Adjustment(
                0.0,
                0.0,
                255.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_bg_r = Gtk.SpinButton(adjustment=adj_bg_r, hexpand=True)
        self.spin_bg_r.set_numeric(True)
        grid_colors.attach(self.spin_bg_r, 1, 6, 1, 1)

        label_bg_g = Gtk.Label(label="Green (0-255):")
        label_bg_g.set_alignment(1, 0)
        grid_colors.attach(label_bg_g, 0, 7, 1, 1)

        adj_bg_g = Gtk.Adjustment(
                0.0,
                0.0,
                255.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_bg_g = Gtk.SpinButton(adjustment=adj_bg_g, hexpand=True)
        self.spin_bg_g.set_numeric(True)
        grid_colors.attach(self.spin_bg_g, 1, 7, 1, 1)

        label_bg_b = Gtk.Label(label="Blue (0-255):")
        label_bg_b.set_alignment(1, 0)
        grid_colors.attach(label_bg_b, 0, 8, 1, 1)

        adj_bg_b = Gtk.Adjustment(
                0.0,
                0.0,
                255.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_bg_b = Gtk.SpinButton(adjustment=adj_bg_b, hexpand=True)
        self.spin_bg_b.set_numeric(True)
        grid_colors.attach(self.spin_bg_b, 1, 8, 1, 1)

        label_bg_a = Gtk.Label(label="Alpha % (0-100):")
        label_bg_a.set_alignment(1, 0)
        grid_colors.attach(label_bg_a, 0, 9, 1, 1)

        adj_bg_a = Gtk.Adjustment(
                0.0,
                0.0,
                100.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_bg_a = Gtk.SpinButton(adjustment=adj_bg_a, hexpand=True)
        self.spin_bg_a.set_numeric(True)
        grid_colors.attach(self.spin_bg_a, 1, 9, 1, 1)

        # add the grid to the stack with a name and a title
        stack.add_titled(grid_colors, "colors", "Colors")

        # the third tab

        # create a grid with inter-spacig
        grid_other = Gtk.Grid()
        grid_other.set_row_spacing(20)
        grid_other.set_column_spacing(20)

        label_position = Gtk.Label(label="Position:")
        label_position.set_alignment(1, 0)
        grid_other.attach(label_position, 0, 0, 1, 1)

        self.combo_position = Gtk.ComboBoxText()
        grid_other.attach(self.combo_position, 1, 0, 1, 1)
        for key, val in self.position_map.items():
            self.combo_position.append(key, val)

        label_width = Gtk.Label(label="Width (0-1000):")
        label_width.set_alignment(1, 0)
        grid_other.attach(label_width, 0, 1, 1, 1)

        adj_width = Gtk.Adjustment(
                0.0,
                0.0,
                1000.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_width = Gtk.SpinButton(adjustment=adj_width, hexpand=True)
        self.spin_width.set_numeric(True)
        grid_other.attach(self.spin_width, 1, 1, 1, 1)

        label_font_size = Gtk.Label(label="Font size (0-50):")
        label_font_size.set_alignment(1, 0)
        grid_other.attach(label_font_size, 0, 2, 1, 1)

        adj_font_size = Gtk.Adjustment(
                0.0,
                0.0,
                50.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_font_size = Gtk.SpinButton(adjustment=adj_font_size,
                hexpand=True)
        self.spin_font_size.set_numeric(True)
        grid_other.attach(self.spin_font_size, 1, 2, 1, 1)

        label_corner = Gtk.Label(label="Corner radius (0-50):")
        label_corner.set_alignment(1, 0)
        grid_other.attach(label_corner, 0, 3, 1, 1)

        adj_corner = Gtk.Adjustment(
                0.0,
                0.0,
                50.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_corner = Gtk.SpinButton(adjustment=adj_corner, hexpand=True)
        self.spin_corner.set_numeric(True)
        grid_other.attach(self.spin_corner, 1, 3, 1, 1)

        label_border = Gtk.Label(label="Border (0-50):")
        label_border.set_alignment(1, 0)
        grid_other.attach(label_border, 0, 4, 1, 1)

        adj_border = Gtk.Adjustment(
                0.0,
                0.0,
                50.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_border = Gtk.SpinButton(adjustment=adj_border, hexpand=True)
        self.spin_border.set_numeric(True)
        grid_other.attach(self.spin_border, 1, 4, 1, 1)

        label_top_pad = Gtk.Label(label="Top padding (0-100):")
        label_top_pad.set_alignment(1, 0)
        grid_other.attach(label_top_pad, 0, 5, 1, 1)

        adj_top_pad = Gtk.Adjustment(
                0.0,
                0.0,
                100.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_top_pad = Gtk.SpinButton(adjustment=adj_top_pad, hexpand=True)
        self.spin_top_pad.set_numeric(True)
        grid_other.attach(self.spin_top_pad, 1, 5, 1, 1)

        label_bottom_pad = Gtk.Label(label="Bottom padding (0-100):")
        label_bottom_pad.set_alignment(1, 0)
        grid_other.attach(label_bottom_pad, 0, 6, 1, 1)

        adj_bottom_pad = Gtk.Adjustment(
                0.0,
                0.0,
                100.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_bottom_pad = Gtk.SpinButton(adjustment=adj_bottom_pad,
                hexpand=True)
        self.spin_bottom_pad.set_numeric(True)
        grid_other.attach(self.spin_bottom_pad, 1, 6, 1, 1)

        label_side_pad = Gtk.Label(label="Side padding (0-100):")
        label_side_pad.set_alignment(1, 0)
        grid_other.attach(label_side_pad, 0, 7, 1, 1)

        adj_side_pad = Gtk.Adjustment(
                0.0,
                0.0,
                100.0,
                1.0,
                5.0,
                0.0
        )
        self.spin_side_pad = Gtk.SpinButton(adjustment=adj_side_pad,
                hexpand=True)
        self.spin_side_pad.set_numeric(True)
        grid_other.attach(self.spin_side_pad, 1, 7, 1, 1)

        # add the grid to the stack with a name and a title
        stack.add_titled(grid_other, "other", "Other")

        # create a box for the buttons
        hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                spacing=20)

        # create the buttons
        button_ok = Gtk.Button(label="OK")
        button_ok.connect("clicked", self.button_ok_clicked)
        hbox_buttons.pack_start(button_ok, True, True, 0)

        button_cancel = Gtk.Button(label="Cancel")
        button_cancel.connect("clicked", self.button_cancel_clicked)
        hbox_buttons.pack_start(button_cancel, True, True, 0)

        button_apply = Gtk.Button(label="Apply")
        button_apply.connect("clicked", self.button_apply_clicked)
        hbox_buttons.pack_start(button_apply, True, True, 0)

        # create a box for the switcher and the stack and add it as main
        # window's content
        vbox_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        self.add(vbox_content)

        # add the switcher's box and the stack as content
        # do not resize switcher's box (horizontal fill is implicit)
        # fully resize stack
        vbox_content.pack_start(hbox_switcher, False, False, 0)
        vbox_content.pack_start(stack, True, True, 0)
        vbox_content.pack_start(hbox_buttons, False, False, 0)

        self.load_config()

    # load values from config file
    def load_config(self):

        # set defaults
        self.check_enabled.set_active(int(self.def_enabled))
        self.spin_delay.set_value(int(self.def_delay))
        self.check_caption.set_active(int(self.def_use_caption))

        self.spin_text_r.set_value(int(self.def_text_r))
        self.spin_text_g.set_value(int(self.def_text_g))
        self.spin_text_b.set_value(int(self.def_text_b))
        self.spin_text_a.set_value(int(self.def_text_a))
        self.spin_bg_r.set_value(int(self.def_bg_r))
        self.spin_bg_g.set_value(int(self.def_bg_g))
        self.spin_bg_b.set_value(int(self.def_bg_b))
        self.spin_bg_a.set_value(int(self.def_bg_a))

        for short_pos, long_pos in self.position_map.items():
            if self.def_position == short_pos:
                self.combo_position.set_active_id(short_pos)
        self.spin_width.set_value(int(self.def_width))
        self.spin_font_size.set_value(int(self.def_font_size))
        self.spin_corner.set_value(int(self.def_corner))
        self.spin_border.set_value(int(self.def_border))
        self.spin_top_pad.set_value(int(self.def_top_pad))
        self.spin_bottom_pad.set_value(int(self.def_bottom_pad))
        self.spin_side_pad.set_value(int(self.def_side_pad))

        # check if config file exists
        if os.path.exists(conf_file):

            # open config file and get all lines
            with open(conf_file, "r") as f:
                lines = f.readlines()

                # try to find a value in the conf file
                for line in lines:
                    line_clean = line.strip().upper()

                    # ignore comment lines
                    if line_clean.startswith("#") or line_clean == "":
                        continue

                    # split key off at equals
                    key_val = line_clean.split("=")
                    key = key_val[0].strip()

                    # split val off ignoring trailing comments
                    val_array = key_val[1].split("#")
                    val = val_array[0].strip()

                    # set values for keys

                    if "ENABLED" in key:
                        self.check_enabled.set_active(int(val))

                    if "DELAY" in key:
                        self.spin_delay.set_value(int(val))

                    if "CAPTION" in key:
                        self.check_caption.set_active(int(val))

                    if "COLOR" in key:
                        colors = val.split("(")[1].split(")")[0]
                        color_vars = colors.split(",")
                        self.spin_text_r.set_value(int(color_vars[0]))
                        self.spin_text_g.set_value(int(color_vars[1]))
                        self.spin_text_b.set_value(int(color_vars[2]))
                        self.spin_text_a.set_value(
                                int(float(color_vars[3]) * 100))

                    if "BACKGROUND" in key:
                        bgs = val.split("(")[1].split(")")[0]
                        bg_vars = bgs.split(",")
                        self.spin_bg_r.set_value(int(bg_vars[0]))
                        self.spin_bg_g.set_value(int(bg_vars[1]))
                        self.spin_bg_b.set_value(int(bg_vars[2]))
                        self.spin_bg_a.set_value(int(float(bg_vars[3]) * 100))

                    if "POSITION" in key:
                        for short_pos, long_pos in self.position_map.items():
                            if val == short_pos:
                                self.combo_position.set_active_id(short_pos)

                    if "WIDTH" in key:
                        self.spin_width.set_value(int(val))

                    if "FONT_SIZE" in key:
                        self.spin_font_size.set_value(int(val))

                    if "CORNER_RADIUS" in key:
                        self.spin_corner.set_value(int(val))

                    if "BORDER" in key:
                        self.spin_border.set_value(int(val))

                    if "TOP_PADDING" in key:
                        self.spin_top_pad.set_value(int(val))

                    if "BOTTOM_PADDING" in key:
                        self.spin_bottom_pad.set_value(int(val))

                    if "SIDE_PADDING" in key:
                        self.spin_side_pad.set_value(int(val))

    def save_config(self):

        # open or create config file
        with open(conf_file, "w+") as f:

            # TODO: find line for key, replace value instead of overwriting
            # whole file

            f.write("# DO NOT EDIT THIS FILE BY HAND!\n\n")

            # start writing options
            f.write("ENABLED=" + str(int(self.check_enabled.get_active())) +
                    "\n")
            f.write("DELAY=" + str(int(self.spin_delay.get_value())) + "\n")
            f.write("CAPTION=" + str(int(self.check_caption.get_active())) +
                    "\n")

            # set the color alpha to a percent
            f.write(
                "COLOR=" +
                '\"rgba(' +
                str(int(self.spin_text_r.get_value())) + "," +
                str(int(self.spin_text_g.get_value())) + "," +
                str(int(self.spin_text_b.get_value())) + "," +
                str(float(self.spin_text_a.get_value()) / 100) +
                ')\"\n'
            )

            # set the background alpha to a percent
            f.write(
                "BACKGROUND=" +
                '\"rgba(' +
                str(int(self.spin_bg_r.get_value())) + "," +
                str(int(self.spin_bg_g.get_value())) + "," +
                str(int(self.spin_bg_b.get_value())) + "," +
                str(float(self.spin_bg_a.get_value()) / 100) +
                ')\"\n'
            )

            # fudge the position option from the array
            val = self.combo_position.get_active_text()
            for short_pos, long_pos in self.position_map.items():
                if val == long_pos:
                    f.write("POSITION=" + short_pos + "\n")

            f.write("WIDTH=" + str(int(self.spin_width.get_value())) + "\n")
            f.write("FONT_SIZE=" + str(int(self.spin_font_size.get_value())) +
                    "\n")
            f.write("CORNER_RADIUS=" + str(int(self.spin_corner.get_value())) +
                    "\n")
            f.write("BORDER=" + str(int(self.spin_border.get_value())) + "\n")
            f.write("TOP_PADDING=" + str(int(self.spin_top_pad.get_value())) +
                    "\n")
            f.write("BOTTOM_PADDING=" +
                    str(int(self.spin_bottom_pad.get_value())) + "\n")
            f.write("SIDE_PADDING=" + str(int(self.spin_side_pad.get_value())) +
                    "\n")

    def run_prog(self):

        # only run once, no listener
        cmd = "python3 /usr/bin/apod_linux.py & disown"
        array = cmd.split()

        # non-blocking subprocess
        subprocess.Popen(array)

    def check_enabled_clicked(self, widget):
        if widget.get_active():
            self.spin_delay.set_sensitive(True)
            self.check_caption.set_sensitive(True)
            self.check_caption_clicked(self.check_caption)
        else:
            self.spin_delay.set_sensitive(False)
            self.check_caption.set_sensitive(False)
            self.spin_text_r.set_sensitive(False)
            self.spin_text_g.set_sensitive(False)
            self.spin_text_b.set_sensitive(False)
            self.spin_text_a.set_sensitive(False)
            self.spin_bg_r.set_sensitive(False)
            self.spin_bg_g.set_sensitive(False)
            self.spin_bg_b.set_sensitive(False)
            self.spin_bg_a.set_sensitive(False)
            self.combo_position.set_sensitive(False)
            self.spin_width.set_sensitive(False)
            self.spin_font_size.set_sensitive(False)
            self.spin_corner.set_sensitive(False)
            self.spin_border.set_sensitive(False)
            self.spin_top_pad.set_sensitive(False)
            self.spin_bottom_pad.set_sensitive(False)
            self.spin_side_pad.set_sensitive(False)

    def check_caption_clicked(self, widget):
        if widget.get_active():
            self.spin_text_r.set_sensitive(True)
            self.spin_text_g.set_sensitive(True)
            self.spin_text_b.set_sensitive(True)
            self.spin_text_a.set_sensitive(True)
            self.spin_bg_r.set_sensitive(True)
            self.spin_bg_g.set_sensitive(True)
            self.spin_bg_b.set_sensitive(True)
            self.spin_bg_a.set_sensitive(True)
            self.combo_position.set_sensitive(True)
            self.spin_width.set_sensitive(True)
            self.spin_font_size.set_sensitive(True)
            self.spin_corner.set_sensitive(True)
            self.spin_border.set_sensitive(True)
            self.spin_top_pad.set_sensitive(True)
            self.spin_bottom_pad.set_sensitive(True)
            self.spin_side_pad.set_sensitive(True)
        else:
            self.spin_text_r.set_sensitive(False)
            self.spin_text_g.set_sensitive(False)
            self.spin_text_b.set_sensitive(False)
            self.spin_text_a.set_sensitive(False)
            self.spin_bg_r.set_sensitive(False)
            self.spin_bg_g.set_sensitive(False)
            self.spin_bg_b.set_sensitive(False)
            self.spin_bg_a.set_sensitive(False)
            self.combo_position.set_sensitive(False)
            self.spin_width.set_sensitive(False)
            self.spin_font_size.set_sensitive(False)
            self.spin_corner.set_sensitive(False)
            self.spin_border.set_sensitive(False)
            self.spin_top_pad.set_sensitive(False)
            self.spin_bottom_pad.set_sensitive(False)
            self.spin_side_pad.set_sensitive(False)

    def button_ok_clicked(self, widget):
        self.save_config()
        self.run_prog()
        self.destroy()

    def button_cancel_clicked(self, widget):
        self.destroy()

    def button_apply_clicked(self, widget):
        self.save_config()
        self.run_prog()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()

# -)