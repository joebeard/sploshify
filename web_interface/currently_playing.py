#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi
from sploshify_functions import *

cgitb.enable()


def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    now_playing = get_now_playing_details(mysql_cursor)
    body = """<table class='player'>
    <tr><th>Artist:</th><td>%s</td></tr>
    <tr><th>Title:</th><td>%s</td></tr>
    <tr><th>Time Left:</th><td>%s</td></tr>
    </table>""" % (now_playing[0], now_playing[1], seconds_to_minutes(now_playing[2]))
        
    output_raw_text(body)


if __name__ == '__main__':
    main()
