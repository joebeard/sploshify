#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi
from sploshify_functions import *

cgitb.enable()


def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    now_playing = get_now_playing(mysql_cursor)
    body  = "<h3>%s</h3>" % now_playing
    
    output_raw_text(body)


if __name__ == '__main__':
    main()
