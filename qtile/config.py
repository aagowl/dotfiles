# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from graphical_notifications import Notifier
from colors import colors

notifier = Notifier()

#from libqtile.utils import guess_terminal

####### CONSTANTS #######

key_move_left = "h"
key_move_down = "j"
key_move_up = "k"
key_move_right = "l"


mod = "mod4"
terminal = "alacritty"

####### KEY BINDS #######
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    
    # Switch between windows
    Key([mod], key_move_left, lazy.layout.left(), desc="Move focus to left"),
    Key([mod], key_move_right, lazy.layout.right(), desc="Move focus to right"),
    Key([mod], key_move_down, lazy.layout.down(), desc="Move focus down"),
    Key([mod], key_move_up, lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to next window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], key_move_left, lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], key_move_right, lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], key_move_down, lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], key_move_up, lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], key_move_left, lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], key_move_right, lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], key_move_down, lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], key_move_up, lazy.layout.grow_up(), desc="Grow window up"),
    #growing windows for spiral layout
    Key([mod, "control"], "m", lazy.layout.grow_main(), desc="Grow main window"),
    Key([mod, "shift"], "m", lazy.layout.shrink_main(), desc="Grow main window"),
    Key([mod, "control"], "p", lazy.layout.increase_ratio(), desc="Grow spiral ratio"),
    Key([mod, "shift"], "p", lazy.layout.decrease_ratio(), desc="Shrink spiral ratio"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating mode on focused window"),

    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "s", lazy.restart(), desc="Restart Qtile"),
    
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    #launch applications
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "c", lazy.spawn("Code"), desc="Launch vscode"),
    Key([mod, "shift"], "f", lazy.spawn("firefox"), desc="Launch firefox"),
    Key([mod, "shift"], "d", lazy.spawn("discord"), desc="Launch discord"),
    Key([], "Print", lazy.spawn("spectacle"), desc="take a screenshot"),

    # graphical notifier
    Key([mod], 'grave', lazy.function(notifier.prev)),
    Key([mod, 'shift'], 'grave', lazy.function(notifier.next)),
    Key(['control'], 'space', lazy.function(notifier.close)),

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
   
]

####### GROUPS ####### 
#groups are qtiles version of workspaces
groups = [
    Group("1"),
    Group("2"),
    Group("3"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + number of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name),),

            # mod1 + shift + number of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc="Switch to & move focused window to group {}".format(i.name),),

            # mod1 + control + number of group = move focused window to group
            Key([mod, "control"], i.name, lazy.window.togroup(i.name), desc="move focused window to group {}".format(i.name)),
        ]
    )

####### LAYOUTS ####### 
layout_config = {
    'border_focus' : colors['pink'],
    'border_normal' : colors["medium"],
    'border_width' : 2,
    'margin' : 10
}

layouts = [

    layout.Spiral(**layout_config),

    layout.Max(**layout_config),

    layout.Floating(**layout_config),
    
    layout.Columns(**layout_config),
]

widget_defaults = dict(
    font= "JetBrainsMono Nerd Font",
    foreground = colors['light'],
    fontsize= 12,
    padding= 3,
    background= colors['dark'],
)
extension_defaults = widget_defaults.copy()

####### Screens ####### 
screens = [
    Screen(
        #wallpaper
        wallpaper='/home/aagowl/Downloads/PixelArt-SciFi-Landscape_WallpaperPack_2/Busy-Day_3840x2160 copy.png',
        wallpaper_mode='fill',

        #bottom bar
        bottom=bar.Bar(
            [
                widget.CurrentLayout(width=65),
                widget.Sep(foreground=colors['blue']),
                widget.GroupBox(
                    highlight_method="text",
                    active=colors['light'],
                    inactive=colors['medium'],
                    this_current_screen_border=colors['yellow'],
                    disable_drag=True,
                ),
                widget.Sep(foreground=colors['blue']),
                widget.Prompt(),
                widget.WindowName(
                    max_chars=30, 
                    width=240,
                ),
                widget.TextBox(
                    text='▓▒░',
                    # width= 25,
                    foreground=colors["dark"],
                    background=colors["lessDark"],
                    fontsize= 20,
                    padding=0
                ),
                widget.Sep(
                    foreground=colors['lessDark'],
                    background= colors['lessDark'],
                    padding=120,
                    line_width=50, 
                    size_percent=100
                ),

                widget.Systray(background=colors["lessDark"]),
                widget.BatteryIcon(update_interval=30, background=colors["lessDark"]),
                widget.Sep(
                    foreground=colors['lessDark'],
                    background= colors['lessDark'],
                    padding=5,
                    line_width=50, 
                    size_percent=100
                ),
                widget.TextBox(
                    text='\ue0b0',
                    foreground=colors["lessDark"],
                    background=colors["pink"],
                    fontsize= 18,
                    padding=0
                ),
                
                # widget.Sep(foreground=colors['pink'], background= colors['lessDark']),
                widget.TextBox(
                    text="USER:",
                    background=colors['pink'],
                    foreground=colors['dark'],
                ),
                widget.TextBox(
                    text="aagowl", 
                    name="default",
                ),

                widget.Sep(foreground=colors['yellow']),
                widget.TextBox(
                    text="UPDATES:",
                    background=colors['yellow'],
                    foreground=colors['dark']
                ),
                widget.CheckUpdates(
                    distro="Arch",
                    display_format='{updates}',
                    initial_text="Checking...",
                    no_update_string='No Updates!',
                    width=80
                ),

                widget.Sep(foreground=colors['green']),
                widget.TextBox(
                    text="CPU:",
                    background=colors['green'],
                    foreground=colors['dark'],
                ),
                widget.CPU(
                    format='{freq_current}GHz {load_percent}%',
                    width=90
                ),

                widget.Sep(foreground=colors['blue']),
                widget.TextBox(
                    text="MEMORY:",
                    background=colors['blue'],
                    foreground=colors['dark']
                ),
                widget.Memory(
                    format='{MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}'
                ),

                widget.Sep(foreground=colors['purple']),
                widget.TextBox(
                    text="TIME:",
                    background=colors['purple'],
                    foreground=colors['dark']
                ),
                widget.Clock(format="%B %d %H:%M", width=145),

                widget.TextBox(
                    text='\ue0b2',
                    foreground=colors["pink"],
                    background=colors["dark"],
                    fontsize= 18,
                    padding=0
                ),

                widget.QuickExit(
                    padding= 15,
                    default_text='\u23FB',
                    countdown_format='[{}]',
                    background=colors["pink"],
                    foreground=colors["dark"],
                    width=180
                ),
            ],
            24,
            border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            border_color=[colors['purple'], "000000", colors['blue'], "000000"]  # Borders are magenta
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button1", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
