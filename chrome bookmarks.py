#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import cgi
import os
import codecs

import tempfile

use_growl = False
use_scp = True

# get name of current logged in user for OS X in orde to help determine the proper
# Chrome/Chromium path.
user = os.getlogin()

#For Google Chrome use:
#input_filename = "/Users/%s/Library/Application Support/Google/Chrome/Default/Bookmarks" % user

#For Chromium use:
input_filename = "/Users/%s/Library/Application Support/Chromium/Default/Bookmarks" % user

# Destination filename/folder
# This will be deleted afterwards if sent via SCP (use_scp is True)
output_filename = "/Users/%s/Desktop/chrome-bookmarks.html" % user

if use_scp is True:
	import subprocess
	scp_username = "root"
	scp_host = "192.168.10.101"
	scp_filename = "/var/www/bookmarks/index.html"

if use_growl is True:
	import gntp.notifier
	growl = gntp.notifier.GrowlNotifier(
		applicationName = "Chrome Bookmarks Export",
		notifications = ["New Updates","New Messages"],
		defaultNotifications = ["New Messages"],
		# hostname = "computer.example.com", # Defaults to localhost
		# password = "abc123" # Defaults to a blank password
		)
	growl.register()

input_file = codecs.open(input_filename, encoding='utf-8')
bookmark_data = json.load(input_file)
output_file = codecs.open(output_filename, 'w', encoding='utf-8')

def print_bookmarks(bookmarks):
	for entry in bookmarks:
		if entry['type'] == 'folder':
			if not len(entry['children']) == 0:
				output_file.write(u'<h3>' + entry['name'] + '</h3>\n' + '<div id="' + entry['name'] + '">\n' + '<ol>\n')
				next_folder = entry['children']
				print_bookmarks(next_folder)
				output_file.write('</ol>' + '</div>\n')
		else:
			link = ('<li><a href="%s" target="_blank">%s</a></li>\n') % (cgi.escape(entry['url']), entry['name'])
			output_file.write(link)

output_file.write('''
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="utf-8" />
 <title>My Bookmarks</title>
 <!-- link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" / -->
 <link rel="stylesheet" href="http://bootswatch.com/simplex/bootstrap.css" />
 <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
 <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
 <!-- link rel="stylesheet" href="/resources/demos/style.css" / -->
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
<div id="accordion">\n
''')


# Extracts all folders/urls from the last bookmark in roots which is typically
# 'other_bookmarks', 'other', or 'Bookmarks'
# Basically, this should be all your bookmarks besides your bookmarks menu bar
roots = bookmark_data['roots']['bookmark_bar']['children'][-1]

# Extract a specific folder from the Bookmarks menu bar. In my case it's the first
# in the list (first in the menu bar).
readlater = bookmark_data['roots']['bookmark_bar']['children'][0]

#Enable IPython debug to shell
#from IPython import embed
#embed()

for entry in roots:
	try:
		print_bookmarks(roots[entry])
	except:
		pass

# Create a specific header and id for my folder extracted from the bookmarks menu as we won't be iterating through to get the folder name.
output_file.write(u'<h3> Read Later </h3>\n' + '<div id="Read Later">\n' + '<ol>\n')

for entry in readlater:
	try:
		print_bookmarks(readlater[entry])
	except:
		pass

output_file.write('''
</div>
</body>
</html>
''')

if use_scp is True:
		output_file.close()
		subprocess.call(["scp", output_filename, scp_username + "@" + scp_host + \
                        ":" + scp_filename])
		os.remove(output_filename)
elif use_scp is False:
		output_file.close()

if use_growl is True:
	growl.notify(
		noteType = "New Messages",
		title = "Chrome Bookmarks Export Completed",
		description = "The Chrome bookmarks export script has completed..",
		sticky = False,
		priority = 1,
	)
