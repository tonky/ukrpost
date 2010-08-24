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
import math

conn = sqlite3.connect(os.path.join(os.getcwd(), 'ukrpost.sqlite3'))
c = conn.cursor()

c.execute('create table if not exists cache (key blob primary key, info blob, expires integer default 0)')
conn.commit()

def cache(timeout=False):
    def check_cache(f):
        def new_f(key):
            info = _read(key)

            if not info:
                info = f(key)
                _write(key, info, timeout)

            return info
        return new_f
    return check_cache


# internal functions

def _read(key):
    c.execute('select key, info from cache where key = ? and (expires IS 0 or expires > ?)', (key, time.time()))

    row = c.fetchone()

    if row:
        # looks like data is read from sqlite as unicode, so i have to encode
        # it to ascii, so wsgi could push data to client
        return row[1].encode('utf-8')
    
    return False

def _write(key, info, timeout):
    expires = 0

    if timeout:
        expires = int(time.time()) + timeout*60

    c.execute('replace into cache values (?, ?, ?)', (key, info, expires))
    conn.commit()
