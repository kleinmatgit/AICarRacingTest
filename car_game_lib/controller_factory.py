from car_game_lib.ai_controller import AIController
from car_game_lib.human_controller import HumanController

#################################################################
## Controller factory
## Handle creation of AIController and HumanController objects
#################################################################

class ControllerFactory:

    #create controllers dictionary from list of BGECars
    def createFromCars(self,bgeCars,speedController,steeringController):
        
        #create dictionary of 'carname':'Controller'
        controllers = {}
        for bgeCar in bgeCars:
            #based on carname, we deduce if car is controlled by AI or by human
            if bgeCar.carname[:3] == 'cpu':
                controllers[bgeCar.carname] = AIController(bgeCar,speedController,steeringController)
            else:
                controllers[bgeCar.carname] = HumanController(bgeCar)
        return controllers
