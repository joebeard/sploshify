#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time

media_directory = '/home/joeb/pyjuke/media/'

min_playlist_size = 10

mysql_username = 'sploshify'
mysql_password = 'sploshify1'
mysql_host = 'localhost'
mysql_db = 'sploshify'


def main():
    mysql_connect_object = MySQLdb.connect(host=mysql_host, user=mysql_username, passwd=mysql_password, db=mysql_db)
    mysql_connect_object.autocommit(True)
    mysql_cursor = mysql_connect_object.cursor()
    while True:
        try:
            mysql_cursor.execute("SELECT count(*) FROM `playlist` WHERE played IS NULL")
            count = mysql_cursor.fetchall()[0][0]
            if count < min_playlist_size: 
                required = min_playlist_size - count
                logging.info('Not enough auto-added songs, adding %s more' % (required))

                mysql_cursor.execute("""SELECT id, last_played FROM
                    (SELECT media.`id`, max(played) AS last_played FROM `media` 
                    LEFT JOIN `playlist` on media.id = playlist.media_id
                    WHERE safe = 1
                    GROUP BY media.id
                    ORDER BY max(played) ASC LIMIT 50) AS T
                    ORDER BY RAND()
                    LIMIT %s """,(required,))

                for new_track in mysql_cursor.fetchall():
                    mysql_cursor.execute("INSERT INTO `playlist` (media_id, user_selected) VALUES (%s, %s) ", (new_track[0], 0))
            else:
                logging.info('Playlist has %s unplayed songs, sleeping' % min_playlist_size)
        except Exception as e:
            logging.error('Something went wrong! - %s' % e)
        time.sleep(60)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    main()
