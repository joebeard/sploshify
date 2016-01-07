#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi

cgitb.enable()

min_playlist_size = 10

mysql_username = 'sploshify'
mysql_password = 'sploshify1'
mysql_host = 'localhost'
mysql_db = 'sploshify'

def get_current_playlist(mysql_cursor):
    mysql_cursor.execute("""SELECT * FROM playlist
            LEFT JOIN media ON playlist.media_id = media.id
            WHERE played IS NULL ORDER BY user_selected DESC, playlist.id ASC""")
    unplayed = list(mysql_cursor.fetchall())

    queue_position = 1

    table = "<table><tr><th>#</th><th>Artist</th><th>Track</th></tr>"
    for track in unplayed:
        table += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (queue_position, track[6], track[5])
        queue_position += 1
    table += "</table>"
    return table


def output_raw_text(text = None):
    print "Content-Type: text/html;charset=utf-8\n"
    print
    print text

def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    body = get_current_playlist(mysql_cursor)
    
    output_raw_text(body)


if __name__ == '__main__':
    main()
