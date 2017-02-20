#!/usr/bin/env python

import os
from subprocess import check_call
import shutil
import datetime

os.mkdir("tmp")
post_dirs = os.listdir("posts")

posts = {}
short_names = {}

with open("templates/post-top0.html") as f:
    post_top0 = f.read()
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

    short_name = "_".join(post_name.split("_")[:2])
    short_name0 = short_name
    i = 0
    while short_name0 in short_names.values():
        short_name0 = short_name + "_%d" % i
        i += 1
    short_names[date] = short_name0

    if os.path.exists("../site/blog-posts/%s.html" % short_name0) and os.path.getmtime("posts/%s/%s.ipynb" % (post_dir, post_name)) < os.path.getmtime("../site/blog-posts/%s.html" % short_name0):
        continue

    command = "jupyter nbconvert --to html --template basic posts/%s/%s.ipynb" % (post_dir, post_name)
    check_call(command.split(" "))
    shutil.move("posts/%s/%s.html" % (post_dir, post_name), "tmp/%s.html" % short_name0)

    content = post_top0
    content += title
    content += post_top
    content += "<h1>%s</h1>\n" % title
    date_str = date.strftime("%d %B %Y").lstrip("0")
    content += '<p><a href="https://twitter.com/share" class="twitter-share-button" data-via="AndrewM_Webb" data-dnt="true" data-show-count="false">Tweet</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> '
    content += "%s</p>\n" % date_str
    content += '<br>(This blog post was written as a Jupyter notebook. <a href="https://www.github.com/grey-area/website/tree/master/blog_posts/posts/%s" target="_blank">The .ipynb file of this blog post and associated files can be found here.)</a><br><br>\n' % post_dir

    with open("tmp/%s.html" % short_name0) as f:
        post_content = f.read()
        content += post_content.replace('src="./img/', 'src="../blog-images/%s/' % post_name)

    content += """

<br>
<a href="https://twitter.com/share" class="twitter-share-button" data-via="AndrewM_Webb" data-dnt="true" data-show-count="false">Tweet</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<br>
<div id="disqus_thread"></div>
<script>

/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
/*
var disqus_config = function () {
this.page.url = http://awebb.info/blog/%s;  // Replace PAGE_URL with your page's canonical URL variable
this.page.identifier = %s; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
};
*/
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = '//awebb-info.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>


""" % (short_name0, short_name0)

    content += post_bottom

    with open("../site/blog-posts/%s.html" % short_name0, "w") as f:
        f.write(content)
    shutil.copytree("posts/%s/img" % post_dir, "../site/blog-images/%s" % post_name)

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
    short_name = short_names[date]
    title = post_name.replace("_", " ")
    title = title[0].upper() + title[1:]
    date_str = date.strftime("%d/%m/%y")
    content += '%s <a href="../blog/%s">%s</a>\n' % (date_str, short_name, title)
    #content += '&nbsp;&nbsp;<a href="https://github.com/grey-area/website/tree/master/blog_posts/posts/%s" target="_blank">(.ipynb)</a>\n' % post_name
    #content += '&nbsp;<a href="../blog-posts-py/%s.ipynb">(interactive)</a>\n' % post_name
    content += "<br>"

if len(sorted_keys) == 0:
    content += "<p><b>There are currently no blog posts here.</b></p>\n"

content += list_bottom

with open("../site/blog-post-pages/blog0.html", "w") as f:
    f.write(content)
