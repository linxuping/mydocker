#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#http://www.cnblogs.com/dkblog/archive/2011/08/26/2155018.html

import logging
'''
#version.01
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(process)d %(thread)d %(filename)s:%(lineno)d[%(levelname)s] %(message)s',
                datefmt='%Y:%m:%d %H:%M:%S',
                filename='myapp.log',
                filemode='a')
#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################
'''

#version.02
import logging.config

logging.config.fileConfig("basemodules/logger.config")
#logger = logging.getLogger("filef_output")
logger = logging.getLogger("filef")



'''
#examples.
logger.debug('This is debug message')
logger.info('This is info message')
logger.warning('This is warning message')
logger.error('This is error message')
'''

