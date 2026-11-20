#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 round 2 poster.

Copies the rendered broadsheet (entry.png, drawn by
render_frontpage.py in this directory) into the output directory
Make.fun provides. Pure standard library, no network, no input:
two runs always write the same bytes.
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"
SIZE_LIMIT = 1_048_576        # competition cap: 1 MiB
SIDE_LIMIT = 1024             # competition cap: 1024x1024 px
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def read_dimensions(path):
    """Width and height from the PNG IHDR chunk, or None."""
    with path.open("rb") as handle:
        head = handle.read(24)
    if head[:8] != PNG_MAGIC or head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def sha256_of(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not IMAGE.is_file():
        return fail(f"{IMAGE} is missing")
    if IMAGE.stat().st_size > SIZE_LIMIT:
        return fail("entry.png is over the 1 MiB cap")
    with IMAGE.open("rb") as handle:
        if handle.read(8) != PNG_MAGIC:
            return fail("entry.png is not a PNG file")
    dims = read_dimensions(IMAGE)
    if dims is None:
        return fail("entry.png has no readable IHDR chunk")
    if dims[0] > SIDE_LIMIT or dims[1] > SIDE_LIMIT:
        return fail(f"entry.png is {dims}, over the 1024x1024 cap")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(IMAGE, target)
    if target.stat().st_size != IMAGE.stat().st_size:
        return fail("copied entry.png came out incomplete")
    if sha256_of(target) != sha256_of(IMAGE):
        return fail("copied entry.png does not match the source bytes")
    print(f"wrote {target} ({target.stat().st_size} bytes, "
          f"sha256 {sha256_of(target)[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
