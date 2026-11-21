"""DRIFTWICK poster entry: copy the pre-rendered poster to /output/entry.png.

The poster itself is drawn by tools/render.py (Pillow) and committed as
assets/entry.png, so both harness runs write identical bytes. This program
needs no network, no fonts and no Pillow at run time — plain stdlib only.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, "/output/entry.png")


if __name__ == "__main__":
    main()
