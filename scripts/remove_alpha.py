#!/usr/bin/env python3
from os.path import join, dirname

version_file = join(dirname(dirname(__file__)), "ovos_tts_plugin_lingva", "version.py")

with open(version_file) as f:
    lines = f.readlines()

with open(version_file, "w") as f:
    for line in lines:
        if line.startswith("VERSION_ALPHA"):
            f.write("VERSION_ALPHA = 0\n")
        else:
            f.write(line)
