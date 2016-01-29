from car_game_lib.logger_handler import LoggerHandler

#########################################
## HumanController
#########################################

class HumanController:
    
    def __init__(self,bgeCar):
        self.bgeCar = bgeCar
        #self.logger = LoggerHandler(appname=self.__class__.__name__)
    
    def __repr__(self):
        return ('HumanController - ' + self.bgeCar.carname)
            
    def execute(self):
        self.bgeCar.update()
        #self.logger.info(str(self.bgeCar))
    
