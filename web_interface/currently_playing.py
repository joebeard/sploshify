#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi

cgitb.enable()

min_playlist_size = 10

mysql_username = 'sploshify'
mysql_password = 'sploshify1'
mysql_host = 'localhost'
mysql_db = 'sploshify'


def get_now_playing(mysql_cursor):
    mysql_cursor.execute("""SELECT *, TIME_TO_SEC(TIMEDIFF(NOW(),played)) FROM playlist 
            LEFT JOIN media on media.id = playlist.media_id
            WHERE played IS NOT NULL ORDER BY played DESC LIMIT 1""")
    
    last_played = mysql_cursor.fetchall()

    if len(last_played) == 0:
        return "Nothing Currently Playing"
    else:
        last_played = last_played[0]

    if last_played[8] >= last_played[11]:
        return "%s - %s (~%ss remaining)" % (last_played[6], last_played[5], int(last_played[8])-int(last_played[11]))
    else:
        return "Nothing Currently Playing"

    return str(last_played)

def output_raw_text(text = None):
    print "Content-Type: text/html;charset=utf-8\n"
    print
    print text

def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    now_playing = get_now_playing(mysql_cursor)
    body  = "<h3>%s</h3>" % now_playing
    
    output_raw_text(body)


if __name__ == '__main__':
    main()
