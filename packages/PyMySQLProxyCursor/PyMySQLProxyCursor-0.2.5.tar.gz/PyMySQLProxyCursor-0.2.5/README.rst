.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/PyMySQL/PyMySQL/blob/master/LICENSE


PyMySQLProxyCursor
==================


A simple cursor wrapper to support before/after processing using PyMySQL.


Installation
------------

The last stable release is available on PyPI and can be installed with ``pip``::

    $ pip install PyMySQLProxyCursor

Example
-------

.. code:: python

    from __future__ import print_function

    import pymysql
    import proxycursor

    class SimpleProxy(object):
        def __init__(self):
            self.tblname = 'user'

        def after_insert(self, **kwargs):
            cur = kwargs['cursor']
            cur.execute('SELECT LAST_INSERT_ID()')

        def after_update(self, **kwargs):
            cur = kwargs['cursor']
            cur.execute('SELECT * FROM user ORDER BY updated_at desc LIMIT 1')


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='mysql')

    cur = conn.cursor()
    cur = proxycursor.wrap(cur, handlers=[SimpleProxy()])
    cur.execute("SELECT Host,User FROM user")

    print(cur.description)

    print()

    for row in cur:
        print(row)

    cur.close()
    conn.close()

License
-------

PyMySQLProxyCursor is released under the MIT License. See LICENSE for more information.
