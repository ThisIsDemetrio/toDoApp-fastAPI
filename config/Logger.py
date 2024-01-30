from logging.config import dictConfig
import logging

from utils import APP_NAME, LOG_LEVELS_DICT

class Logger():
    def __init__(self, log_level='INFO'):
        log_level_num = LOG_LEVELS_DICT.get(log_level, -1)
        if log_level_num == -1:
            print(f'{log_level} is not a valid log level. Defaulting to "INFO".')
            log_level_num = 20
            
        logConfig =  {
			"version": 1,
			"disable_existing_loggers": False,
			"formatters": {
				"default": {
					"()": "uvicorn.logging.DefaultFormatter",
					"fmt": "%(levelprefix)s %(asctime)s %(message)s",
					"datefmt": "%Y-%m-%d %H:%M:%S",
				},
			},
			"handlers": {
				"default": {
					"formatter": "default",
					"class": "logging.StreamHandler",
					"stream": "ext://sys.stderr",
				},
			},
			"loggers": {
				'toDoApp': {"handlers": ["default"], "level": log_level_num},
			},
		}
        
        dictConfig(logConfig)
        
    def get_logger(self):
        return logging.getLogger(APP_NAME)
