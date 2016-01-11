#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi
from sploshify_functions import *

cgitb.enable()

min_playlist_size = 10

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    form = cgi.FieldStorage()

    head = """<script src="http://code.jquery.com/jquery-latest.js"></script>
<script> $(document).ready(function() { $("#currently_playing").load("currently_playing.py"); $("#playlist").load("playlist.py"); var refreshId_cp = setInterval(function() { $("#currently_playing").load('currently_playing.py'); }, 5000); var refreshId_pl = setInterval(function() { $("#playlist").load('playlist.py'); }, 10000); $.ajaxSetup({ cache: false }); }); </script>"""

    body = "<div class='two_column'>"
    body += "<h2>Currently Playing</h2><div id='currently_playing'><h3>Loading...</h3></div>"
    

    goodish_music = get_playable_selection(mysql_cursor, 'goodish')
    evil_music = get_playable_selection(mysql_cursor, 'evil')

    try: 
        if 'add_evil' in form:
            track_id = int(form['add_evil'].value)
            if track_id in [int(x[0]) for x in evil_music]:
                mysql_cursor.execute("""INSERT INTO playlist (media_id, user_selected) VALUES
                       (%s, %s)""", (track_id, 2))
                evil_music = get_playable_selection(mysql_cursor, 'evil')
        if 'add_goodish' in form:
            track_id = int(form['add_goodish'].value)
            if track_id in [int(x[0]) for x in goodish_music]:
                mysql_cursor.execute("""INSERT INTO playlist (media_id, user_selected) VALUES
                       (%s, %s)""", (track_id, 1))
                goodish_music = get_playable_selection(mysql_cursor, 'goodish')
    except:
        body += 'naughty'

    current_playlist = get_current_playlist(mysql_cursor)

    body += "<h2>Queue A Good-ish Song</h2>" 
    if len(goodish_music) > 0:
        body += "<form action='' method='post'><select name='add_goodish'>"
        for track in goodish_music:
            body += "<option value='%s'>%s - %s</option>" % (track[0], track[2], track[1])
        body += "</select><input type='submit' value='Be Goodish'></form>"
    else:
        body += "<p>Sorry no goodish music is currently available. Sad Face.</p>"

    body += "<h2>Be Evil</h2>" 
    if len(evil_music) > 0:
        body += "<form action='' method='post'><select name='add_evil'>"
        for track in evil_music:
            body += "<option value='%s'>%s - %s</option>" % (track[0], track[2], track[1])
        body += "</select><input type='submit' value='Be Evil'></form>"
    else:
        body += "<p>Sorry no evil music is currently available. Sad Face.</p>"

    body += "</div><div style='float: left; width:50px;'>&nbsp;</div><div class='two_column'><div>"
    body += "<H2>Up Next</h2><div  id='playlist'>Loading...</div></div></div>"

    output(head, sploshify_body(body))


if __name__ == '__main__':
    main()
