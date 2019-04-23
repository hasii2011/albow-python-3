
import sys


class MenuItem:

    keyname = ""
    keycode = None
    shift = False
    alt = False
    enabled = False

    if sys.platform.startswith('darwin') or sys.platform.startswith('mac'):
        cmd_name = "Cmd "
        option_name = "Opt "
    else:
        cmd_name = "Ctrl "
        option_name = "Alt "

    def __init__(self, text="", command=None):

        self.command = command
        if "/" in text:
            text, key = text.split("/", 1)
        else:
            key = ""
        self.text = text
        if key:
            keyname = key[-1]
            mods = key[:-1]
            self.keycode = ord(keyname.lower())
            if "^" in mods:
                self.shift = True
                keyname = "Shift " + keyname
            if "@" in mods:
                self.alt = True
                keyname = self.option_name + keyname
            self.keyname = self.cmd_name + keyname
