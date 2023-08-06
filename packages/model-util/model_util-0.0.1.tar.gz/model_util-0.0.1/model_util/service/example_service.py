#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

import logging
from caijiajia.model_util.service.base_service import BaseService


class ExampleService(BaseService):
    def run_detail(self, **params):
        print 'running...'
        logging.info('running...')

    def run_history_detail(self, **params):
        print 'running history...'
        logging.info("running history...")
