#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, MySQLdb, time, cgitb, cgi
from sploshify_functions import *

cgitb.enable()

min_playlist_size = 10

def main():

    body = "<h2>Evil Override</h2>"
    body += "<p>You really thought it would be that easy? Oh dear...</p>"


    output(body=sploshify_body(body))


if __name__ == '__main__':
    main()
