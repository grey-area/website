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
    post_fields = post_dir.split("_")

    year = int(post_fields[0])
    month = int(post_fields[1])
    day = int(post_fields[2])
    date = datetime.datetime(year, month, day)

    post_name = "_".join(post_fields[3:])
    command = "jupyter nbconvert --to html --template basic posts/%s/%s.ipynb" % (post_dir, post_name)
    check_call(command.split(" "))
    shutil.move("posts/%s/%s.html" % (post_dir, post_name), "tmp/")

    content = post_top
    content += "<br><a href=http://awebb.info/blog-posts-py/%s.ipynb>Download the .ipynb file of this blog post here.</a><br><br>\n" % post_name
    with open("tmp/%s.html" % post_name) as f:
        content += f.read()
    content += post_bottom

    with open("../site/blog-posts/%s.html" % post_name, "w") as f:
        f.write(content)
    shutil.copy("posts/%s/%s.ipynb" % (post_dir, post_name), "../site/blog-posts-py/")

    posts[date] = post_name

shutil.rmtree("tmp")

with open("templates/list-top.html") as f:
    list_top = f.read()
with open("templates/list-bottom.html") as f:
    list_bottom = f.read()
content = list_top

sorted_keys = sorted(posts.keys(), reverse=True)
month_year_str = ""
for date in sorted_keys:
    new_month_year_str = "\n<br><b>%s</b><br>\n" % date.strftime("%B %Y")
    if new_month_year_str != month_year_str:
        content += new_month_year_str
        month_year_str = new_month_year_str
    post_name = posts[date]
    title = post_name.replace("_", " ")
    title = title[0].upper() + title[1:]
    date_str = date.strftime("%d/%m/%y")
    content += '%s <a href="../blog/%s">%s</a>\n' % (date_str, post_name, title)
    content += ' <a href="../blog-posts-py/%s.ipynb"><img src="../misc/jupyter.png", style="border:0;", height="20", width="20"></a><br>\n' % post_name

content += list_bottom

with open("../site/blog-post-pages/blog0.html", "w") as f:
    f.write(content)
