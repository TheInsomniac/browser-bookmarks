Firefox Bookmarks
===

Just a simple python script that automatically exports your *nix or OSX
Firefox bookmarks. This extracts the data directly from the sqlite database
so can be done while Firefox is running. 

All "Folders" are headers and the links themselves are lists beneath
each header. 

Optionally scp the file to a remote host in order to publish on your web
server for access elsewhere.

Add this script to your cron in order to have it update your bookmarks
when they change or perhaps further this script with linux' ionotify
so that it automatically runs when the sqlite database is modified.

Added:
---
jquery version as an option to the plain html version.
Requires the 'js' and 'themes' folder. Additional themes can be downloaded and/or created at
http://jqueryui.com/themeroller/
