#!/usr/bin/env python

import os
import sys
import datetime
import shutil

now = datetime.datetime.now()

dir_start = "%d_%d_%d_" % (now.year, now.month, now.day)
if len(sys.argv) > 1:
    title = sys.argv[1]
    dir_name = "%s%s" % (dir_start, title)
else:
    print "Supply a name"
    sys.exit(1)

post_dir = "posts/%s" % dir_name
os.mkdir(post_dir)

shutil.copy("templates/requirements.txt", post_dir)
shutil.copy("templates/no_publish", post_dir)
shutil.copy("templates/template.ipynb", "%s/%s.ipynb" % (post_dir, title))

os.mkdir("%s/img" % post_dir)

title.replace("_", " ")
title = title[0].upper() + title[1:]
with open("%s/README.md" % post_dir, "w") as f:
    f.write("# %s\n" % title)
