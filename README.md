podcast
=======

Simple Python Script to Manage Podcasts.

I wrote this to handle converting podcast files into multiple formats for distribution on the web.  It essentially ends up being a preset manager for ffmpeg really, that can make it really easy to automate this process on OS X or Linux.  There is nothing specifically that won't run on Windows to my knowledge, but things like file paths etc. probably don't work as they are all set up in a 'Unix' like fashion.

Ideally this gets set up with some sort of file monitoring daemon.  On OS X I used Hazel combined with a basic Bash script to set the PATH and launch the script, on Linux thus far I like watcher.py (The .ini config file one)

Requirements
------------
ffmpeg (git)
Python 2.7

Reccomended
------------
s3cmd (git)
Hazel or watcher.py

Configuration
------------
As of right now configuration is actually done by creating presets in the python file itself.  This may be broken out to another file in the future, but is unlikely to ever be anything but plain python.  Lets face it, the presets run untrusted commands, it is a security risk anyways if someone can access the python, so no reason worrying about it to much.  Plus it makes it nice and easy to update the command line for any presets.

Operation
-----------
python podcast.py --format FORMAT SOURCE DESTINATION

Not exactly the most difficult thing.  The main thing is I am trying to keep this very short sweet and to the point.  I don't want a lot of command line options, either they go into a preset or they may just go into another file.