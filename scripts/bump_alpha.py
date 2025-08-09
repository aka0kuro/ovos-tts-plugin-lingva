#!/usr/bin/env python3
from os.path import join, dirname

version_file = join(dirname(dirname(__file__)), "ovos_tts_plugin_lingva", "version.py")

with open(version_file) as f:
    lines = f.readlines()

with open(version_file, "w") as f:
    for line in lines:
        if line.startswith("VERSION_ALPHA"):
            current = int(line.split("=")[1])
            f.write(f"VERSION_ALPHA = {current + 1}\n")
        else:
            f.write(line)
