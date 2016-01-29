import bge
from mathutils import Vector
import math
from car_game_lib.logger_handler import LoggerHandler

#########################################
## Steering controller
#########################################

class SteeringController:

    def __init__(self):
        self.name = 'simpleSteeringController'
        #self.logger = LoggerHandler(appname=self.__class__.__name__)
    
    def execute(self,bgeCar):

        #vector between car and guide
        car_position = bgeCar.getPosition()
        guide_position = bgeCar.bgeGuide.getPosition()
        vec_to_guide = guide_position - car_position

        #car norm vector
        car_dir_vec = bgeCar.getVelocity()

        #in 2D
        vec_to_guide = Vector([vec_to_guide[0],vec_to_guide[1]])
        car_dir_vec = Vector([car_dir_vec[0],car_dir_vec[1]])
                
        #angle between the two
        angle = vec_to_guide.angle_signed(car_dir_vec,None)
        if angle==None:
            angleFormated = 0.0
        else:
            angleFormated = angle * 180/math.pi
        
        angle_treshold = 2.0
        
        if angleFormated > angle_treshold:
            bge.logic.sendMessage(bgeCar.carname + '_Left')
        elif angleFormated < -angle_treshold:
            bge.logic.sendMessage(bgeCar.carname + '_Right')
