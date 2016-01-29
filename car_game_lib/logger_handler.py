import logging
import datetime
import os

class LoggerHandler():

    logger = None
    hdlr = None
    
    def __init__(self,
                 appname,
                 log_path = 'C:/Program Files/Blender Foundation/Blender/2.70/python/lib/site-packages/car_game_lib/log/',
                 log_file_ext = '.log',
                 log_formatter = '%(asctime)s %(levelname)s %(message)s',
                 log_level = logging.DEBUG):

        try:
            #print('path:' + os.getcwd())
            os.makedirs(log_path)
        except OSError as exception:
            if os.path.exists(log_path):
                pass
            else:
                raise
        
        self.logger = logging.getLogger(appname)
        self.hdlr = logging.FileHandler(log_path + appname + '_' + str(os.getpid()) + log_file_ext)
        self.hdlr.setFormatter(logging.Formatter(log_formatter))
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(log_level)
        
    def info(self,msg,bPrint=False,bReturnStr=False):
        self.logger.info(msg)
        if bPrint: print(msg)
        if bReturnStr: return msg

    def warning(self,msg,bPrint=False):
        self.logger.warning(msg)
        if bPrint: print(msg)
    
    def fatal(self,msg,bPrint=False):
        self.logger.fatal(msg)
        if bPrint: print(msg)

    def close(self):
        self.hdlr.close()
        self.logger.removeHandler(self.hdlr)

if __name__ == "__main__":
    appname = 'test_logger'
    logger = LoggerHandler(appname)
    logger.info('test info')
    logger.warning('test warning')
    logger.fatal('test fatal')
    logger.close()
    
