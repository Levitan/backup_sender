backup_sender
=============

Backup Sender - backuping your site and send to remote FTP-server.

Dependency
==========
1. Python 2.7 or later
2. Modules for Python: sys, os, ftplib, md5, cgi, zipfile
3. Avalible execution CGI on hosting

Usage
=====
1. Put file backup_sender.py in root your site
2. Change permissions to 755 (-rwxr-xr-x)
3. Add to .htaccess strings (without quotes) "Options +ExecCGI" and "AddHandler cgi-script .py"
4. Add to file backup_sender.py you access to DB and remote FTP
5. Go to url http://example.com/backup_sender.py?login=YOUR_LOGIN&pass=YOUR_PASS
