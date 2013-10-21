#!/usr/bin/env python2.7

'''
podcast.py

A basic script in python to handle conversion to a couple of different formats
'''

__author__ = "Thomas Vecchione (Seablade)"
__copyright__ = "Copyright 2013, Thomas Vecchione"
__credits__ = ""
__license__ = "GPLv2"
__version__ = "0.0.1"

import os, sys, subprocess, shutil
import argparse, tempfile
import string
import logging, logging.handlers

'''
Presets:

These are just dicts with the appropriate command line to run really,
while I am using them for ffmpeg, they literally could be used for
anything.  Appropriate Template Variables:

${ffmpeg} == full path to ffmpeg
${source} == full path to the source file
${tmp} == full path to a temporary directory
${filename} == The filename only, with no extension
${dest} == The full path to the destination folder for the file
${faststart} == The full path to the qt-faststart command
${t} == Number of threads for ffmpeg to use
'''
presets = { "mp4_high" : "${ffmpeg} -threads ${t} -i ${source} -s hd720 -vcodec libx264 -preset slow -crf 20 -acodec libfaac -ab 192k ${tmp}/${filename}.mp4 && ${faststart} ${tmp}/${filename}.mp4 ${dest}/${filename}.mp4",
            "mp4_low" : "${ffmpeg} -threads ${t} -i ${source} -s hd480 -vcodec libx264 -preset slow -crf 24 -acodec libfaac -ab 96k ${tmp}/${filename}.mp4 && ${faststart} ${tmp}/${filename}.mp4 ${dest}/${filename}.mp4",
            "webm_high" : "${ffmpeg} -threads ${t} -i ${source} -s hd720 -vcodec libvpx -g 120 -lag-in-frames 16 -deadline good -cpu-used 0 -vprofile 0 -qmax 51 -qmin 11 -slices 4 -b:v 2M -acodec libvorbis -ab 192k -f webm ${dest}/${filename}.webm",
            "ogv_high" : "${ffmpeg} -threads ${t} -i ${source} -codec:v libtheora -qscale:v 7 -codec:a libvorbis -qscale:a 6 ${dest}/${filename}.ogv",
            "aac_low" : "${ffmpeg} -threads ${t} -i ${source} -vn -acodec libfaac -ab 96k -ac 1 -ar 44100 ${dest}/${filename}.m4a",
            "snapshots" : "${ffmpeg} -i ${source} -f image2 -vf fps=fps=1/300 ${dest}/${filename}-snapshot%04d.png"
            }
'''
The following variables get converted to fill in the above templates
'''
command = "/usr/bin/env ffmpeg" # The full path to the ffmpeg command
dirtemp = tempfile.mkdtemp() # The full path to the temporary directory
qtfs = "/usr/bin/env qt-faststart" # The full path to qt-faststart command
threads = 16 # The number of threads to use in conversion

if __name__ == '__main__':
    '''
    '''

    # Necessary due to Hazel not necessarily setting the $CWD correctly, and all this is intended to be self-contained -- actually I may have changed my mind:)
    #os.chdir(os.path.dirname(os.path.realpath(__file__)))
    #curdir = os.getcwd() # Currently Unused

    logging.basicConfig(filename="podcast.log",
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(console)
    logging.getLogger('').addHandler(logging.handlers.SysLogHandler(address = ("/var/run/syslog")))
    log = logging.getLogger('Podcast')

    parser = argparse.ArgumentParser(description="Podcast Management Software for Atlee Community Church")

    # Required Arguments
    parser.add_argument("source", help="The source file to use for the podcast")
    parser.add_argument("destination", help="Where to save the encoded file to")

    # Optional Arguments
    parser.add_argument("--format", choices=presets.keys(), help="The preset format to be used, if none is defined the file will be passed through as is instead of being converted.")

    '''
    The following arguments are not yet implemented, but are intended to
    be part of the metadata of the file
    '''
    parser.add_argument("--title", help="The title of the video")
    parser.add_argument("--description", help="A short description of the video, to include the date the video was released")
    parser.add_argument("--author", help="The creator of the video")
    args = parser.parse_args()
    
    name = os.path.splitext(os.path.split(args.source)[1])[0]
    log.debug("Name: %s" % name)
    destination = os.path.realpath(args.destination)
    
    if not os.path.exists(destination):
        log.warn("Destination Directory %s doesn't exist, creating..." % destination)
        try:
            os.mkdir(destination)
        except OSError:
            log.error("Can't create destination directory %s\n\t%s" % (destination, sys.exc_info()[1]))
            sys.exit()
    
    if args.format:
        temp = string.Template(presets[args.format])
        cmd = temp.safe_substitute(ffmpeg = command, source = os.path.realpath(args.source), dest = destination, tmp = dirtemp, filename = name, faststart=qtfs, t = threads)
        log.info(cmd)
        try:
            p=subprocess.Popen(cmd, shell=True)
            p.wait()
            log.info('Conversion Completed Succesfully!')
        except:
            log.info('Conversion Failed!\n Error Code: %d' % e)
            sys.exit()
    else:
        src = os.path.realpath(args.source)
        dst = destination + "/" + os.path.basename(args.source)
        log.info("Copying %s to %s" % (src, dst))
        try:
            shutil.copyfile(src, dst)
            log.info('Source File Copy Succeeded!')
        except IOError:
            log.warn('Source File Copy Failed!\n\t%s' % sys.exc_info()[1])
            sys.exit()

