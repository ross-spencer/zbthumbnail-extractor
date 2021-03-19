#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import sys
import uuid


def buffer_window_read(f, buf):

    if buf != "":
        buf[0] = buf[1]
        buf[1] = buf[2]
        buf[2] = buf[3]
        buf[3] = f.read(1)
    else:
        buf = []
        buf.append(f.read(1))
        buf.append(f.read(1))
        buf.append(f.read(1))
        buf.append(f.read(1))

    return buf


def extractJpegs(tnfile):

    bFound = False

    if os.path.isfile(tnfile):

        # If we need a directory name, create it here.
        dirname = tnfile.split(".", 1)[0] + "-" + str(uuid.uuid4())

        f = open(tnfile, "rb")

        tncount = 0

        buf = ""

        file_len = os.path.getsize(f.name)

        JPGHead = "\xFF\xD8"
        JPGTail = "\xFF\xD9"

        while f.tell() < file_len:
            buf = buffer_window_read(f, buf)
            fbytes = b"".join(buf[0:2])
            if fbytes == JPGHead:

                # Create a folder to store jpegs
                if bFound is False:
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                        bFound = True

                tncount += 1
                file = []
                file = buf
                buf = ""
                eofJPG = False
                while eofJPG is False:
                    buf = buffer_window_read(f, buf)
                    fbytes = b"".join(buf[0:2])
                    if fbytes == JPGTail:
                        file.append(buf[0])
                        file.append(buf[1])
                        eofJPG = True
                        buf = ""
                        image_name = "image-{}.jpg".format(str(tncount).zfill(4))
                        file_to_open = os.path.join(dirname, image_name)
                        jpg = open(file_to_open, "wb")
                        jpg.write(b"".join(file[0:]))
                        jpg.close()
                    else:
                        file.append(buf[0])

        f.close()
        print("{} JPEGs discovered.".format(tncount))
    else:
        print("Warning: Filename provided does not point to a file.", file=sys.stderr)


def main():

    # Usage:  --info [ZbThumbnail.info]

    # Handle command line arguments for the script
    parser = argparse.ArgumentParser(
        description="Extract JPG from ZbThumbnail.info files. NOTE: May also be applicable to Thumbs.db at users own risk."
    )
    parser.add_argument(
        "--info", help="Optional: Single zbthumbnail.info file to read.", default=False
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if args.info:
        extractJpegs(args.info)

    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
