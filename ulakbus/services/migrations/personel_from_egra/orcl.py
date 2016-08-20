# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
import os
import cx_Oracle

__author__ = 'zops5'


class OrclError(Exception):
    pass


class Orcl(object):
    def __init__(self, db_user, db_pass, db_host):
        self.cursor = None
        self.DB_USER = db_user
        self.DB_PASS = db_pass
        self.DB_HOST = db_host

    def get_cursor(self):
        os.environ["NLS_LANG"] = ".AL32UTF8"

        if all([self.DB_USER, self.DB_PASS, self.DB_HOST]):
            db = cx_Oracle.connect(self.DB_USER, self.DB_PASS, self.DB_HOST)
            self.cursor = db.cursor()
        else:
            raise OrclError("Check connection string")

    def rows_as_dicts(self):
        """ returns cx_Oracle rows as dicts """
        colnames = [i[0] for i in self.cursor.description]
        for row in self.cursor:
            yield dict(zip(colnames, row))
