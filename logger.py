import logging

class Logger:
    @staticmethod
    def setup():
        path_log = 'path_para_gravar_log'
        logger = logging.getLogger('bot')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(path_log)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
