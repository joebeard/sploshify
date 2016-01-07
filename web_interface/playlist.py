#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi
from sploshify_functions import *

cgitb.enable()

def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    body = get_current_playlist(mysql_cursor)
    
    output_raw_text(body)


if __name__ == '__main__':
    main()
