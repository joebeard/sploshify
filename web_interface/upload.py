#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi
from sploshify_functions import *

cgitb.enable()
UPLOAD_DIR = '/sploshify_media'

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    form = cgi.FieldStorage()
    
    
    body = "<h2>Upload a file to Sploshify...</h2>"
    
    body += "<h3>%s</h3>" % save_uploaded_file (form, "mp3", UPLOAD_DIR, mysql_cursor)
    
    body += """<form action="upload.py" method="POST" enctype="multipart/form-data">
<table>
<tr><th>File name</th><td><input name="mp3" type="file"></td></tr>
<tr><th>File rating</th><td><select name='safe'>
<option value='goodish'>good-ish</option>
<option value='evil'>evil</option>
</select></td></tr>
<tr><th colspan='2' align='center'>
<input name="submit" type="submit"></th></tr>
</table>
</form>
<br>
Please note: after clicking submit the it may take a little while for the mp3 to upload and process. Please be patient :)
<br><br>
"""

    output(body=sploshify_body(body))
    
    
    
if __name__ == '__main__':
    main()
