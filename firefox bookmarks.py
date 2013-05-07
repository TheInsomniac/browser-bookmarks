#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from collections import OrderedDict
import tempfile

use_growl = False
use_scp = False

firefox = '/Users/me/Firefox/Profiles/abcdefg23.default/'

if use_scp is True:
    import subprocess
    scp_username = "www"
    scp_host = "192.168.1.1"
    scp_filename = "/var/www/bookmarks/index.html"

if use_growl is True:
    import gntp.notifier
    growl = gntp.notifier.GrowlNotifier(
        applicationName = "Firefox Bookmarks Export",
        notifications = ["New Updates","New Messages"],
        defaultNotifications = ["New Messages"],
        # hostname = "computer.example.com", # Defaults to localhost
        # password = "abc123" # Defaults to a blank password
        )
    growl.register()

conn = sqlite3.connect(firefox + 'places.sqlite')
cursor = conn.cursor()

f = tempfile.NamedTemporaryFile(mode='w+b')

f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="utf-8" />
 <title>My Bookmarks</title>
 <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
 <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
 <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
 <link rel="stylesheet" href="/resources/demos/style.css" />
 <script>
 $(function() {
   $( "#accordion" ).accordion({
    collapsible: true,
    heightStyle: "content",
    active: false
   });
 });
 </script>
</head>
<body>
''')

sql = "select id,title from moz_bookmarks where type=2;"
cursor.execute(sql)
folders = cursor.fetchall()

# Remove built in folders such as Unsorted and hide the parent (extraneous) folders for the Menubar and the main Bookmarks.
folders = folders[8:-5]

# f.write('<a id="Top"></a><h3>- ')

# for folder in folders:
#     link = '<a href="#%s">%s</a> - ' % (folder[1], folder[1])
#     f.write(link)

# f.write('</h3>')

f.write('<div id="accordion">\n')

bookmarks = OrderedDict()

for id in folders:
    bookmarks[id[1]] = (cursor.execute(
        "select b.title, a.url from moz_places a, moz_bookmarks b where a.id=b.fk and b.parent='%s';"
        % (id[0])).fetchall())

for key in bookmarks:
    f.write('<h3>' + key + '</h3>\n' + '<div id="' + key + '">\n' + '<ol>\n')
    for item in bookmarks[key]:
        link = ('<li><a href="%s" target="_blank">%s</a></li>\n') % (item[1].encode('utf8'), item[0].encode('utf8'))
        f.write(link)
    f.write('</ol>' + '</div>\n')

f.write('''
</div>
</body>
</html>
''')

f.seek(0)

if use_scp is True:
    subprocess.call(["scp", f.name, scp_username + "@" + scp_host +\
            ":" + scp_filename])
elif use_scp is False:
    outfile = open('bookmarks.html', 'w')
    outfile.write(f.read())
    outfile.close()

f.close()

if use_growl is True:
    growl.notify(
        noteType = "New Messages",
        title = "Firefox Bookmarks Export Completed",
        description = "The Firefox bookmarks export script has completed..",
        sticky = False,
        priority = 1,
        )
