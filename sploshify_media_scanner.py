#!/usr/bin/python
# -*- coding: utf-8 -*-

import pydub, os, logging, MySQLdb, mutagen.id3

media_directory = '/sploshify_media'

mysql_username = 'sploshify'
mysql_password = 'sploshify1'
mysql_host = 'localhost'
mysql_db = 'sploshify'


def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_cursor = mysql_connect_object.cursor()

    found_media = os.listdir(media_directory)

    for file in found_media:
        filename = '%s%s' % (media_directory, file)

        mysql_cursor.execute("""SELECT id FROM media WHERE location = %s""", (filename,) )
        if len(mysql_cursor.fetchall()) == 0:
    	    try:
    	        s = pydub.AudioSegment.from_mp3(filename)
                id3 = mutagen.id3.ID3(filename)
                mysql_cursor.execute("""INSERT INTO media (location, title, artist, album, duration, safe) 
                    VALUES (%s, %s, %s, %s, %s, %s)""", (filename, 
                    id3.get('TIT2', 'Unknown'), id3.get('TPE1', 'Unknown'), id3.get('TALB', 'Unknown'), int(s.duration_seconds), 'goodish'))
                mysql_connect_object.commit()
            
                logging.info("Added: %s, %s, %s, %s, %s" % (filename, 
                    id3.get('TIT2', 'Unknown'), id3.get('TPE1', 'Unknown'), id3.get('TALB', 'Unknown'), int(s.duration_seconds)))

    	    except Exception as e:
    	        logging.info('Something couldnt load %s - %s' % (file, e))
                
            else:
                pass

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    main()
