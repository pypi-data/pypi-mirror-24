#!/usr/bin/env python

from __future__ import print_function

from pkg_resources import get_distribution
__version__ = get_distribution('exiftimestamper').version

# from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle 

from distutils.spawn import find_executable
import subprocess
import exifread
import sys, os, re, time, functools
import argparse

def exif_timestamp ( fn ):
    TIMESTAMP_TAGS = ["EXIF DateTimeOriginal",
                      "Image DateTime"]
    with open(fn, 'rb') as fh:
        tags = exifread.process_file(fh)
        for TAG in TIMESTAMP_TAGS:
            stamp = tags.get(TAG)
            if stamp:
                break
        else:
            raise Exception("no date tag in {}: {}"
                            .format(fn, tags.keys()))

        t = time.strptime(str(stamp), '%Y:%m:%d %H:%M:%S')
        return t

def mp4_timestamp(fn):
    # mediainfo --Inform="General;%Encoded_Date%" VID_20170811_221350395-i-did-it-my-way-ryong-il-kiyul.mp4
    # UTC 2017-08-11 14:19:13

    stamp=subprocess.check_output(["mediainfo", "--Inform=General;%Encoded_Date%", fn])
    t = time.strptime(str(stamp.strip()), '%Z %Y-%m-%d %H:%M:%S')
    return t

def media_timestamp(fn):
    if re.match("(?i).*[.]jpe?g$", fn):
        return exif_timestamp(fn)
    elif re.match("(?i).*[.]mp4$", fn):
        return mp4_timestamp(fn)
    else:
        return None

def walk_top ( media_directory, quiet, recursive ):
    top=media_directory
    print ("walking over '{}'".format(top), file=sys.stderr)
    failed=0
    total=0

    for (dirpath, dirnames, filenames) in \
        (os.walk(top) if recursive else ((top, [], os.listdir(top)), )):
        for base in filenames:
            fn = os.path.join(dirpath, base)
            try:
                t=media_timestamp(fn)
                if t:
                    total+=1
                    stamp=time.strftime('%Y:%m:%d %H:%M:%S', t)
                    utime=time.mktime(t)
                    os.utime(fn, (utime,utime))
                    if not quiet:
                        print ("updated {} to {}".format(fn, stamp))
            except Exception as ex:
                failed+=1
                print ("ERROR: unable to update {}'s timestamp: {}"
                .format(fn, repr(ex)), file=sys.stderr)

        print ("{}/{} errors"
                .format(failed, total), file=sys.stderr)
                
def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("media_directory",
                        help="top-level directory containing images")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="don't report success")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="recurisve")
    parser.add_argument("--version", action="version",
                        version=__version__)

    kwargs = vars(parser.parse_args())
    if not find_executable("mediainfo"):
        print ( "WARNING: mediainfo required for mp4 timestamp extraction" )

    walk_top(**kwargs)

if __name__ == '__main__':
    main()
