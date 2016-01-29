import bge
from car_game_lib.logger_handler import LoggerHandler

#########################################
## AIController
#########################################

class AIController:
    
    def __init__(self,bgeCar,
                 speedController,steeringController):
        self.bgeCar = bgeCar
        self.speedController = speedController
        self.steeringController = steeringController
        self.control = self.standardControl
        #self.logger = LoggerHandler(appname=self.__class__.__name__)
    
    def __repr__(self):
        return ('AIController - ' + self.bgeCar.carname)

    #execute algorithm        
    def execute(self):
        self.control()

    #change type of control: 'eor' or 'standard'
    def setControl(self,control):
        if control == 'eor':
            self.control = self.endOfRaceControl
        else:
            self.control = self.standardControl
    
    #used during the race as a standard way of steering/speeding
    def standardControl(self):
        self.speedController.execute(self.bgeCar)
        self.steeringController.execute(self.bgeCar)
        self.bgeCar.projectGuide()
        self.bgeCar.update()
        #self.logger.info(str(self.bgeCar))

    #used at end of race to stop AI car
    def endOfRaceControl(self):
        bge.logic.sendMessage(self.bgeCar.carname + '_Brake')
        
