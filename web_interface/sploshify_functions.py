#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi, os
import pydub, mutagen.id3

cgitb.enable()

min_playlist_size = 10

mysql_username = 'sploshify'
mysql_password = 'sploshify1'
mysql_host = 'localhost'
mysql_db = 'sploshify'



def seconds_to_minutes(seconds):
    try:
        minutes = int(seconds)/60
        seconds = seconds % 60
        return "%sm%ss" % (minutes, seconds)
    except:
        return "unknown"

def get_current_playlist(mysql_cursor):
    mysql_cursor.execute("""SELECT * FROM playlist 
            LEFT JOIN media ON playlist.media_id = media.id
            WHERE played IS NULL ORDER BY user_selected DESC, playlist.id ASC""")
    return mysql_cursor.fetchall()



def get_now_playing_details(mysql_cursor):
    mysql_cursor.execute("""SELECT artist, title, duration-TIME_TO_SEC(TIMEDIFF(NOW(),played)) FROM playlist 
            LEFT JOIN media on media.id = playlist.media_id
            WHERE played IS NOT NULL ORDER BY played DESC LIMIT 1""")
    
    last_played = mysql_cursor.fetchall()

    if len(last_played) == 0:
        return "Nothing Currently Playing"
    else:
        if last_played[0][2] >= 0:
            return last_played[0]
        else:
            return ("Nothing Currently Playing","NA","NA")
    
def get_playable_selection(mysql_cursor, safety = 'goodish'):
    
    min_wait_period = {'good':12, 'goodish':4, 'evil':12}
    
    mysql_cursor.execute("""SELECT * 
    FROM media AS A
    LEFT JOIN
    (SELECT media_id, max(played) as last_played
            FROM `playlist`
            GROUP BY media_id) AS B 
    ON A.id = B.media_id
    LEFT JOIN 
    (SELECT media_id, 1 as in_playlist
            FROM `playlist` 
            WHERE played is NULL) AS C
    ON C.media_id = B.media_id
    WHERE in_playlist IS NULL
        AND safe = %s
        AND (last_played <= DATE_SUB(NOW(), INTERVAL %s hour) OR last_played IS NULL)
    ORDER BY artist, title""", (safety, min_wait_period[safety]))
    
    return mysql_cursor.fetchall()



def get_full_track_list(mysql_cursor):
    table = "<table>"
    for safe in ['good','goodish','evil', 'dont_play']:
        table += "\n<tr><th colspan='5'>Tracks tagged as %s</th></tr>" % safe

        mysql_cursor.execute("""SELECT * FROM media WHERE safe = %s ORDER BY artist, title""", (safe, ))
        tracks = mysql_cursor.fetchall()

        for track in tracks:
            table += "\n<tr><td>%s</td><td>%s</td><td>(%s)</td></tr>" % (track[2], track[1], track[3])

    table += "\n</table>"
    return table




def output(head = "", body = None):
    print "Content-Type: text/html;charset=utf-8\n"
    print 
    print "<!DOCTYPE html><html><head>"
    print "<title>Sploshify</title>"
    print "<link rel='stylesheet' type='text/css' href='style.css'>"
    print head
    print "</head><body>"
    print body
    print "</body></html>"

    
    
def output_raw_text(text = None):
    print "Content-Type: text/html;charset=utf-8\n"
    print
    print text
    
    
    
def sploshify_body(text):
    return """
        <div id="wrapper">
        <div id="contentwrap">
        <div id="header">

    <h1>Sploshify</h1>
    <div id='menu'>
        <a class='button' href='/'>Player</a> 
        <a class='button' href='/track_list.py'>Track List</a> 
        <a class='button' href='/upload.py'>Make a Deposit</a>
        <a class='button' href='/evil_override.py'>Evil Override</a>
    </div>
    <br>
    </div>
    <div id="content">
    %s
    </div>
    <div class='clearer'><br><br></div>
    </div>
    """ % text

    


def save_uploaded_file (form, form_field, upload_dir, mysql_cursor):
    """This saves a file uploaded by an HTML form.
       The form_field is the name of the file input field from the form.
       For example, the following form_field would be "file_1":
           <input name="file_1" type="file">
       The upload_dir is the directory where the file will be written.
       If no file was uploaded or if the field does not exist then
       this does nothing.
    """
    if not form.has_key(form_field): return "Please upload a file."
    fileitem = form[form_field]
    
    if not form.has_key('safe'): return "Naughty!"
    safe = form['safe'].value
    
    if not fileitem.file: return "Please select a file before clicking upload."
    
    if not fileitem.filename.endswith('mp3') : return "Please upload MP3s Only"
    
    filename = os.path.join(upload_dir, fileitem.filename)
    
    if os.path.exists(filename): return "That file already exists!"
    
    fout = file (filename, 'wb')
    while 1:
        chunk = fileitem.file.read(100000)
        if not chunk: break
        fout.write (chunk)
    fout.close()
    
    try:
        s = pydub.AudioSegment.from_mp3(filename)
        id3 = mutagen.id3.ID3(filename)
        
        if id3.get('TIT2', 'Unknown') == 'Unknown' or id3.get('TPE1', 'Unknown') == 'Unknown':
            os.remove(filename)
            return "Could not read ID3 tags, please edit the file to include them: (Artist:%s - Title:%s)" % (id3.get('TPE1', 'Unknown'), id3.get('TIT2', 'Unknown'))
        
        mysql_cursor.execute("""INSERT INTO media (location, title, artist, album, duration, safe) 
            VALUES (%s, %s, %s, %s, %s, %s)""", (filename, 
            id3.get('TIT2', 'Unknown'), id3.get('TPE1', 'Unknown'), id3.get('TALB', 'Unknown'), int(s.duration_seconds), safe))

    except Exception as e:
        #remove file if something went wrong!
        os.remove(filename)
        return 'Something went wrong! %s - %s' % (file, e)
    else:
        return "Added...<br> Title: %s<br>Artist:%s<br>Album:%s<br>Duration:%s<br>Classified as:%s" % (
            id3.get('TIT2', 'Unknown'), id3.get('TPE1', 'Unknown'), 
            id3.get('TALB', 'Unknown'), int(s.duration_seconds),
            safe)        
    

if __name__ == '__main__':
    sys.exit(1)
