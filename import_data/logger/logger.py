"""Инициализация объекта логера"""

import logging.config

from import_data.logger import logger_conf

logging.config.dictConfig(logger_conf.dict_conf)

logger = logging.getLogger('import_data_logger')
