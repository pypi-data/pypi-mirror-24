#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

from caijiajia.model_util.utils.dbtemplate import DbTemplate


class BaseDao(object):
    def __init__(self, host, port, username, pwd, db, charset, db_type):
        real_db = BaseDao._get_real_database(db, db_type)
        self.db_template = DbTemplate(host, username, pwd, real_db, charset, port)

    def _read(self, sql, params=()):
        return self.db_template.get(sql, params)

    def _update(self, sql, params):
        self.db_template.update(sql, params)

    def _save(self, sql, params):
        self.db_template.save(sql, params)

    def _save_and_return(self, sql, params):
        return self.db_template.save_and_return(sql, params)

    def _update_by_patch(self, sql, params):
        self.db_template.update_by_patch(sql, params)

    def _save_by_patch(self, sql, params):
        self.db_template.save_by_patch(sql, params)

    def _delete(self, sql, params):
        self.db_template.delete(sql, params)

    def close(self):
        self.db_template.close_connection()

    @staticmethod
    def _get_real_database(db, db_type):
        if db_type == 'test':
            return '%s_test' % db
        elif db_type == 'auto_test':
            return '%s_test' % db.split('_')[-1]
        else:
            return db
