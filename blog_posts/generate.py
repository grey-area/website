#!/usr/bin/env python

import os
from subprocess import check_call
import shutil

os.mkdir("tmp")
post_dirs = os.listdir("posts")

for post_dir in post_dirs:
    post_name = "_".join(post_dir.split("_")[3:])
    command = "jupyter nbconvert --to html --template basic posts/%s/%s.ipynb" % (post_dir, post_name)
    check_call(command.split(" "))
    shutil.move("posts/%s/%s.html" % (post_dir, post_name), "tmp/")

    command = "cat templates/post-top.html tmp/%s.html templates/post-bottom.html" % post_name
    check_call(command.split(" "))
