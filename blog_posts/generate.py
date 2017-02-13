#!/usr/bin/env python

import os
from subprocess import check_call
import shutil
import datetime

os.mkdir("tmp")
post_dirs = os.listdir("posts")

posts = {}

with open("templates/post-top.html") as f:
    post_top = f.read()
with open("templates/post-bottom.html") as f:
    post_bottom = f.read()

for post_dir in post_dirs:

    if "no_publish" in os.listdir("posts/%s" % post_dir):
        continue

    post_fields = post_dir.split("_")

    year = int(post_fields[0])
    month = int(post_fields[1])
    day = int(post_fields[2])
    date = datetime.datetime(year, month, day)

    post_name = "_".join(post_fields[3:])
    title = post_name.replace("_", " ")
    title = title[0].upper() + title[1:]
    posts[date] = post_name

    if os.path.exists("../site/blog-posts/%s.html" % post_name) and os.path.getmtime("posts/%s/%s.ipynb" % (post_dir, post_name)) < os.path.getmtime("../site/blog-posts/%s.html" % post_name):
        continue

    command = "jupyter nbconvert --to html --template basic posts/%s/%s.ipynb" % (post_dir, post_name)
    check_call(command.split(" "))
    shutil.move("posts/%s/%s.html" % (post_dir, post_name), "tmp/")

    content = post_top
    content += "<h1>%s</h1>\n" % title
    date_str = date.strftime("%d %B %Y").lstrip("0")
    content += "<p>%s</p>\n" % date_str
    content += '<br><a href="../blog-posts-py/%s.ipynb" download target="_blank">Download the .ipynb file of this blog post here.</a><br><br>\n' % post_name
    with open("tmp/%s.html" % post_name) as f:
        content += f.read()
    content += post_bottom

    with open("../site/blog-posts/%s.html" % post_name, "w") as f:
        f.write(content)
    shutil.copy("posts/%s/%s.ipynb" % (post_dir, post_name), "../site/blog-posts-py/")

shutil.rmtree("tmp")

with open("templates/list-top.html") as f:
    list_top = f.read()
with open("templates/list-bottom.html") as f:
    list_bottom = f.read()
content = list_top

sorted_keys = sorted(posts.keys(), reverse=True)
month_year_str = ""
for date in sorted_keys:
    new_month_year_str = "\n<b>%s</b><br>\n" % date.strftime("%B %Y")
    if new_month_year_str != month_year_str:
        content += "<br>"
        content += new_month_year_str
        month_year_str = new_month_year_str
    post_name = posts[date]
    title = post_name.replace("_", " ")
    title = title[0].upper() + title[1:]
    date_str = date.strftime("%d/%m/%y")
    content += '%s <a href="../blog/%s">%s</a>\n' % (date_str, post_name, title)
    content += '&nbsp;&nbsp;<a href="../blog-posts-py/%s.ipynb" download target="_blank">(.ipynb file)</a>\n' % post_name
    #content += '&nbsp;<a href="../blog-posts-py/%s.ipynb">(interactive)</a>\n' % post_name
    content += "<br>"

if len(sorted_keys) == 0:
    content += "<p><b>There are currently no blog posts here.</b></p>\n"

content += list_bottom

with open("../site/blog-post-pages/blog0.html", "w") as f:
    f.write(content)
