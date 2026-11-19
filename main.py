#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Copies the poster image (entry.png, rendered by
render_frontpage.py) to the Make.fun output directory.

Runs with no network and no input: the same bytes on every run.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576  # the competition's 1 MiB cap
MAX_SIDE = 1024      # the competition's 1024x1024 pixel cap


def png_size(path):
    """(width, height) from the PNG IHDR chunk, stdlib only."""
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def main():
    if not os.path.isfile(SOURCE):
        print(f"error: {SOURCE} missing", file=sys.stderr)
        return 1
    # Sanity-check the image before copying: PNG magic bytes, the
    # competition's 1 MiB size cap and its 1024x1024 pixel cap.
    with open(SOURCE, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG", file=sys.stderr)
        return 1
    if os.path.getsize(SOURCE) > MAX_BYTES:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    size = png_size(SOURCE)
    if size is None or size[0] > MAX_SIDE or size[1] > MAX_SIDE:
        print(f"error: entry.png size {size} breaks the pixel cap",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # Verify the copy landed byte-complete before reporting success.
    if os.path.getsize(dest) != os.path.getsize(SOURCE):
        print("error: copied entry.png is incomplete", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
