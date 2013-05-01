# -*- coding: utf-8 -*-
import sqlite3
import subprocess
from collections import OrderedDict

outdir = "/Users/mark/Projects/Firefox Bookmarks/"
dir = '/Users/mark/Library/Application Support/Firefox/Profiles/vnwxu7qq.default/'
conn = sqlite3.connect(dir + 'places.sqlite')
cursor = conn.cursor()

f = open(outdir + 'bookmarks.html','w')
f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="utf-8" />
 <title>My Bookmarks</title>
 <link rel="stylesheet" href="./themes/insomniac/jquery-ui-1.10.2.custom.css" />
 <script src="./js/jquery-1.9.1.js"></script>
 <script src="./js/ui/jquery-ui-1.10.2.custom.js"></script>
 <!-- <link rel="stylesheet" href="/resources/demos/style.css" /> -->
 <script>
 $(function() {
   $( "#accordion" ).accordion({
    collapsible: true,
    heightStyle: "fill"
   });
 });
 </script>
</head>
<body>
''')

sql = "select id,title from moz_bookmarks where type=2;"
cursor.execute(sql)
folders = cursor.fetchall()
folders = folders[8:-5]

#f.write('<a id="Top"></a><h3>- ')

#for folder in folders:
#    link = '<a href="#%s">%s</a> - ' % (folder[1], folder[1])
#    f.write(link)

#f.write('</h3>')

f.write('<div id="accordion">\n')

bookmarks = OrderedDict()

for id in folders:
    bookmarks[id[1]] = (cursor.execute(
        "select b.title, a.url from moz_places a, moz_bookmarks b where a.id=b.fk and b.parent='%s';"
        % (id[0])).fetchall())

for key in bookmarks:
    f.write('<h3>' + key + '</h3>\n' + '<div>\n' + '<ol>\n')
    for item in bookmarks[key]:
        link = ('<li><a href="%s" target="_blank">%s</a></li>\n') % (item[1].encode('utf8'), item[0].encode('utf8'))
        f.write(link)
    f.write('</ol>' + '</div>\n')

f.write('''
</div>
</body>
</html>
''')

f.close()

try:
    subprocess.call(["scp",outdir + "bookmarks.html","root@192.168.10.101:/var/www/bookmarks/index.html"])
except:
    print "SCP Transfer Failed"
