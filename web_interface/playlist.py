#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi
from sploshify_functions import *

cgitb.enable()

def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    playlist = get_current_playlist(mysql_cursor)
    queue_position = 1
    
    table = "<table><tr><th>#</th><th>Artist</th><th>Track</th></tr>"
    for track in playlist:
        table += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (queue_position, track[6], track[5])
        queue_position += 1
    table += "</table>"
    
    
    output_raw_text(table)


if __name__ == '__main__':
    main()
