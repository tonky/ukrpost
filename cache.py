#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Provides caching mechanism with persistent storage for function calls.
Implemented as decorator, with timeout argument, in minutes.
"""

import inspect
import os
import sqlite3
import time

conn = sqlite3.connect(os.path.join(os.getcwd(), 'ukrpost.sqlite3'))
c = conn.cursor()

c.execute('create table if not exists address (postcode integer, address blob)')
c.execute('create table if not exists track (number integer, info blob, expires integer)')
conn.commit()

def cache(timeout=False):
    def check_cache(f):
        def new_f(key):
            table = f.__name__

            if table == 'index':
                info = _read_index(key)

            if table == 'track':
                info = _read_track(key)

            if not info:
                info = f(key)

                if table == 'index':
                    _write_index(key, info)

                if table == 'track':
                    _write_track(key, info, timeout)


            return info
        return new_f
    return check_cache


# internal functions

def _read_index(key):
    c.execute('select postcode, address from address where postcode = ?', (key,))

    row = c.fetchone()

    if row:
        # looks like data is read from sqlite as unicode, so i have to encode
        # it to ascii, so wsgi could push data to client
        return row[1].encode('utf-8')
    
    return False

def _read_track(key):
    c.execute('select number, info from track where number = ? and expires > ?', (key, time.time()))

    row = c.fetchone()

    if row:
        # looks like data is read from sqlite as unicode, so i have to encode
        # it to ascii, so wsgi could push data to client
        return row[1].encode('utf-8')
    
    return False

def _write_index(key, info):
    c.execute('replace into address values (?, ?)', (key, info))
    conn.commit()

def _write_track(key, info, timeout):
    expires = time.time() + timeout*60

    c.execute('replace into track values (?, ?, ?)', (key, info, expires))
    conn.commit()
