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

def cache(timeout=False):
    def check_cache(f):
        def new_f(key):
            info = _read(key)

            if not info:
                info = f(key)

            # if request turned in nothing - do not cache it
            if info:
                _write(key, info, timeout)

            return info
        return new_f
    return check_cache


# internal functions

def _sql3():
    conn = sqlite3.connect(os.path.join(os.getcwd(), 'ukrpost.sqlite3'), 10)
    c = conn.cursor()

    c.execute('create table if not exists cache (key blob primary key, info blob, expires integer default 0)')
    conn.commit()

    return conn, c

def _read(key):
    conn, c = _sql3()

    c.execute('select key, info from cache where key = ? and (expires IS 0 or expires > ?)', (key, time.time()))

    row = c.fetchone()

    conn.close()

    if row:
        # looks like data is read from sqlite as unicode, so i have to encode
        # it to ascii, so wsgi could push data to client
        return row[1].encode('utf-8')
    
    return False

def _write(key, info, timeout):
    expires = 0

    if timeout:
        expires = int(time.time()) + timeout*60

    conn, c = _sql3()
    c.execute('replace into cache values (?, ?, ?)', (key, info, expires))
    conn.commit()

    conn.close()
