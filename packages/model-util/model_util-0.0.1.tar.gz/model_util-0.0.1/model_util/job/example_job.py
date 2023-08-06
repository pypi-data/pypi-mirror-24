#!/usr/bin/env python
# encoding: utf-8
# Author caijiajia.cn
# @ ALL RIGHTS RESERVED

from caijiajia.model_util.job.base_job import BaseJob
from caijiajia.model_util.utils.param_parser import InputArgument
from caijiajia.model_util.service.example_service import ExampleService


class ExampleJob(BaseJob):
    checked_args = [InputArgument.date]
    execute_class_list = (ExampleService,)


if __name__ == '__main__':
    import sys

    ExampleJob().run(sys.argv[1:], ExampleJob.checked_args, execute_class_list=ExampleJob.execute_class_list)
