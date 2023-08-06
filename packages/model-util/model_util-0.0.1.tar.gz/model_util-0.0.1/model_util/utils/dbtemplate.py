#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

from decimal import *
import logging
import MySQLdb
import math


class DbTemplate(object):
    """
    Connection DB tools.
    """

    def __init__(self, ip, username, pwd, db, charset, port):
        self.conn = MySQLdb.connect(ip, username, pwd, db, charset=charset, port=port, connect_timeout=6000)
        self.conn.autocommit(1)

    def get(self, sql, value=()):
        """
        read data from table in database.
        :param sql:
        :param value: tuple, the index equals the position of placeholder in sql. eg.(1,'name')
        :return:
        """
        cur = None
        try:
            cur = self.conn.cursor()
            execute_num = cur.execute(sql, value)
            execute_detail = cur.fetchmany(execute_num)
            return execute_detail
        except Exception, e:
            logging.error('read db error!', exc_info=True)
            raise e
        finally:
            cur.close()

    def save_and_return(self, sql, value):
        """
        save one data to database and return last row id.
        :param sql:
        :param value: tuple. the index equals the position of placeholder in sql. eg.(1,'name')
        :return:
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, value)
            last_rowid = cur.lastrowid
            return last_rowid
        except Exception, e:
            logging.error('insert and return db error!', exc_info=True)
            raise e
        finally:
            if cur:
                cur.close()

    def save(self, sql, value):
        """
        save one data to database.
        :param sql:
        :param value: tuple. the index equals the position of placeholder in sql. eg.(1,'name')
        :return:
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, value)
        except Exception, e:
            logging.error('insert db error!', exc_info=True)
            raise e
        finally:
            if cur:
                cur.close()

    def update(self, sql, value):
        """
        update one data to database.
        :param sql:
        :param value: tuple. the index equals the position of placeholder in sql. eg.(1,'name')
        :return:
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, value)
        except Exception, e:
            logging.error('update db error!', exc_info=True)
            raise e
        finally:
            if cur:
                cur.close()

    def delete(self, sql, value):
        """
        update one data to database.
        :param sql:
        :param value: tuple. the index equals the position of placeholder in sql. eg.(1,'name')
        :return:
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, value)
        except Exception, e:
            logging.error('delete db error!', exc_info=True)
            raise e
        finally:
            if cur:
                cur.close()

    def update_by_patch(self, sql, values, batch_size=10000):
        """
        update multiple data to database.
        :param sql:
        :param values: list(tuple).  tuple: the index equals the position of placeholder in sql. eg.[(1,'name']
        :param batch_size: how much data save to database by once.
        :return:
        """
        i = 0
        execute_num = 0
        size = math.ceil(Decimal(values.__len__()) / Decimal(batch_size))
        while i < size:
            cur = None
            try:
                cur = self.conn.cursor()
                execute_num += cur.executemany(sql, values[int(i) * batch_size:(int(i) + 1) * batch_size])
            except Exception, e:
                logging.error('update patch error!', exc_info=True)
                raise e
            finally:
                if cur:
                    cur.close()
            i += 1

    def save_by_patch(self, sql, values, batch_size=10000):
        """
        save multiple data to database.
        :param sql:
        :param values: list(tuple).  tuple: the index equals the position of placeholder in sql. eg.[(1,'name']
        :param batch_size: how much data update to database by once.
        :return:
        """
        i = 0
        execute_num = 0
        size = math.ceil(Decimal(values.__len__()) / Decimal(batch_size))
        while i < size:
            cur = None
            try:
                cur = self.conn.cursor()
                execute_num += cur.executemany(sql, values[int(i) * batch_size:(int(i) + 1) * batch_size])
            except Exception, e:
                logging.error('insert patch error!', exc_info=True)
                raise e
            finally:
                if cur:
                    cur.close()
            i += 1

    def close_connection(self):
        """
        close database connection.
        :return:
        """
        if self.conn:
            try:
                self.conn.close()
            except Exception, e:
                logging.error('Can not close database!', exc_info=True)
            finally:
                self.conn = None
