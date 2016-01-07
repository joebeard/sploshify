#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi, subprocess
from sploshify_functions import *

cgitb.enable()

min_playlist_size = 10

def main():

    form = cgi.FieldStorage()
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()
    
    body = "<h2>The Real Evil Override</h2>"
    
    if 'skip_track' in form:
        cmd_output = subprocess.check_output('supervisorctl restart sploshify_player', shell=True).replace("\n",'<br>')
        body += "<h3>%s</h3>" % cmd_output
    if 'reset_evil' in form:
        mysql_cursor.execute('DELETE FROM playlist WHERE media_id IN (SELECT id FROM media WHERE safe="evil")')
        body += "<h3>Evil has been unleashed...</h3>"

    body += "<a href='?skip_track=true' class='button'>skip track</a>"
    body += "<a href='?reset_evil=true' class='button'>reset evil</a>"


    output(body=sploshify_body(body))


if __name__ == '__main__':
    main()
