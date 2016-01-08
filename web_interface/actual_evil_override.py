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
    
    if 'start' in form:
        cmd_output = subprocess.check_output('supervisorctl start sploshify_player', shell=True).replace("\n",'<br>')
        body += "<h3>%s</h3>" % cmd_output
    if 'stop' in form:
        cmd_output = subprocess.check_output('supervisorctl stop sploshify_player', shell=True).replace("\n",'<br>')
        body += "<h3>%s</h3>" % cmd_output
    if 'skip_track' in form:
        cmd_output = subprocess.check_output('supervisorctl restart sploshify_player', shell=True).replace("\n",'<br>')
        body += "<h3>%s</h3>" % cmd_output
    if 'reset_evil' in form:
        mysql_cursor.execute('DELETE FROM playlist WHERE media_id IN (SELECT id FROM media WHERE safe="evil")')
        body += "<h3>Evil has been unleashed...</h3>"
    if 'reset_goodish' in form:
        mysql_cursor.execute('DELETE FROM playlist WHERE media_id IN (SELECT id FROM media WHERE safe="goodish")')
        body += "<h3>All the goodish tracks are back!</h3>"
    if 'reclassify_id' in form:
        mysql_cursor.execute('UPDATE media SET safe = %s WHERE id = %s', (form['safe'].value, form['reclassify_id'].value) )
        body += "<h3>Track reclassified.</h3>"
        
    if 'pull_new_code' in form:
        cmd_output = subprocess.check_output('git  --work-tree=/home/pi/sploshify/ --git-dir=/home/pi/sploshify/.git pull origin master', shell=True).replace("\n",'<br>')
        body += "<h3>%s</h3>" % cmd_output
        
    mysql_cursor.execute('SELECT id, artist, title, safe FROM media ORDER BY artist, title')
    track_list = mysql_cursor.fetchall()        

    body += "<h2>Player Control</h2>"
    body += "<a href='?start=true' class='button'>Start Player</a>"
    body += "<a href='?stop=true' class='button'>Stop Player</a>"
    body += "<a href='?skip_track=true' class='button'>Skip Track</a>"
    body += "<h2>Play-List Control</h2>"
    body += "<a href='?reset_evil=true' class='button'>Unleash Evil</a><a href='?reset_goodish=true' class='button'>Reset Goodish</a><br><br>"
    body += "Re-Classify a track: <form method='post' action='?'><select name='reclassify_id'>"
    for track in track_list:
        body += "<option value='%s'>%s - %s (%s)</option>" % track
    
    body += "</select><select name='safe'><option value='good'>Good</option><option value='goodish'>Good-ish</option><option value='evil'>Evil</option><option value='dont_play'>Do Not Play</option></select><input type='submit' value='Re-Classify'></form>"
    body += "<h2>Admin</h2>"
    body += "<a href='?pull_new_code=true' class='button'>pull latest sploshify code</a>"


    output(body=sploshify_body(body))


if __name__ == '__main__':
    main()
