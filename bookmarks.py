# -*- coding: utf-8 -*-
import sqlite3
import subprocess
from collections import OrderedDict

outdir = "/Users/mark/Documents/"
dir = '/Users/mark/Library/Application Support/Firefox/Profiles/vnwxu7qq.default/'
conn = sqlite3.connect(dir + 'places.sqlite')
cursor = conn.cursor()

f = open(outdir + 'bookmarks.html','w')
f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
<title>My Bookmarks</title>
<style type="text/css">
body {background-color:#2E2E2E;}
h1 {font-family:verdana;color:white;display: inline;}
h5 {display: inline;}
li {color:white;}
a:link {font-family:verdana;color:#A4A4A4;text-decoration: none;}
a:hover {font-family:verdana;color:#555555;text-decoration: none;}
</style>
</head>
<body>
''')

sql = "select id,title from moz_bookmarks where type=2;"
cursor.execute(sql)
folders = cursor.fetchall()
folders = folders[8:-5]

f.write('<a id="Top"></a><h3>- ')

for folder in folders:
    link = '<a href="#%s">%s</a> - ' % (folder[1], folder[1])
    f.write(link)

f.write('</h3>')

bookmarks = OrderedDict()

for id in folders:
    bookmarks[id[1]] = (cursor.execute(
        "select b.title, a.url from moz_places a, moz_bookmarks b where a.id=b.fk and b.parent='%s';"
        % (id[0])).fetchall())

for key in bookmarks:
    f.write('<a id=' + '"' + key + '"' + '><h1>' + key + '</h1></a>\
                &nbsp;&nbsp;&nbsp;<h5><a href="#Top" style="color:#555555;">(top)</a></h5><ol>\n')
    #f.write('<h1>' + key + '</h1>' + '\n<ul>\n')
    for item in bookmarks[key]:
        link = ('<li><a href="%s" target="_blank">%s</a></li>' + '\n') % (item[1].encode('utf8'), item[0].encode('utf8'))
        f.write(link)
    f.write('</ol>\n')

f.write('''
</body>
</html>
''')

f.close()

try:
    subprocess.call(["scp",outdir + "bookmarks.html","usename@127.0.0.1:/var/www/bookmarks/index.html"])
except:
    print "SCP Transfer Failed"
