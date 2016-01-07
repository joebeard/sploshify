#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, logging, MySQLdb, mutagen.id3, sys, time, pygame


mysql_username = 'sploshify'
mysql_password = 'sploshify1'
mysql_host = 'localhost'
mysql_db = 'sploshify'



def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()

    pygame.mixer.init()
    while True:
        #Get Next Song
        mysql_cursor.execute("""SELECT media.id, artist, title, location, playlist.id
                FROM `playlist` 
                LEFT JOIN media ON media.id = playlist.media_id
                WHERE played is NULL 
                ORDER BY user_selected DESC, playlist.id ASC
                LIMIT 1""")
        next_song = mysql_cursor.fetchall()

        if len(next_song) == 0:
            logging.warning('Playlist was empty!')
            time.sleep(10)
        else:
            try:
                logging.info('Playing %s - %s' % (next_song[0][1], next_song[0][2]))
                pygame.mixer.music.load(next_song[0][3])
                pygame.mixer.music.play()
            except pygame.error as e:
                logging.error('Failed to play %s' % e)
            finally:
                mysql_cursor.execute("""UPDATE playlist SET played = NOW() WHERE id = %s""", (next_song[0][4],))
    
                while pygame.mixer.music.get_busy() == True:
                    time.sleep(0.1)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    main()
