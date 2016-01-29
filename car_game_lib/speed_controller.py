import bge
from car_game_lib import toolbox_3d as tools3d
from car_game_lib.logger_handler import LoggerHandler

#########################################
## Speed controller
#########################################

class SpeedController:

    def __init__(self):
        self.name = 'simpleSpeedController'
        #self.logger = LoggerHandler(appname=self.__class__.__name__)
    
    def execute(self,bgeCar):

        carspeed = bgeCar.getSpeed()

        #if car is stopped, we send gas message and return
        if carspeed == 0:
            bge.logic.sendMessage(bgeCar.carname + '_Gas')
            return
        
        #deduce car target speed by interpolation
        target_speed = tools3d.linearInterpolation(
            bgeCar.dist_next_interface,
            0,
            bgeCar.tiManager.getInterfaceTargetSpeed(bgeCar.next_interface_idx),
            bgeCar.tiManager.getDistanceWithPreviousInterface(bgeCar.next_interface_idx),
            bgeCar.tiManager.getPreviousInterfaceTargetSpeed(bgeCar.next_interface_idx))

        if carspeed > target_speed:
            bge.logic.sendMessage(bgeCar.carname + '_Brake')
        else:
            bge.logic.sendMessage(bgeCar.carname + '_Gas')
    
