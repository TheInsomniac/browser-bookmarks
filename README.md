Firefox Bookmarks
===

Just a simple python script that automatically exports your *nix or OSX
Firefox bookmarks into prettified HTML. This extracts the data directly
from the sqlite database so can be done while Firefox is running. 

All "Folders" are headers and the links themselves are lists beneath
each header. 

Optionally scp the file to a remote host in order to publish on your web
server for access elsewhere.

If scp is not used then a 'bookmarks.html' file is created in the directory
where the script was called from.

Add this script to your cron in order to have it update your bookmarks
when they change or perhaps further this script with linux' ionotify
so that it automatically runs when the sqlite database is modified.

Uses
---
jQuery with the stock (smoothness) theme. 
Additional themes can be downloaded and/or created at http://jqueryui.com/themeroller/ 
Optional: system provided SCP to transfer to a remote host 
Optional: Growl notification via gntp protocal.

To Use
---
Change 'firefox' string in script to the path of your Firefox profiles
directory.

Set use_scp in script to 'True' or 'False' depending on whether you want to
transfer to a remote host. If 'True' then change the 'scp_username',
'scp_host', and 'scp_filename' to suit your requirements.  

Set use_growl in script to 'True' or 'False' depending on whether you wish to
be notified by Growl when the script completes it's export. 
Optionally set 'hostname' and 'password' if sending notifications to a remote
host.
