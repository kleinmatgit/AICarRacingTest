from car_game_lib.bge_guide import BGEGuide
from car_game_lib.bge_car_position_handler import BGECarPositionHandler
from car_game_lib import toolbox_3d as tools3d

#########################################
## Wrap a car in blender game engine
#########################################

class BGECar:
    
    def __init__(self,racingLine,tiManager,scene,carname,drivername,
                 racingLinePointInf,racingLinePointSup,
                 lap=0,dist_lap=0.0,next_interface_idx=0,dist_next_interface=0.0):

        self.racingLine = racingLine
        self.tiManager = tiManager
        self.scene = scene
        self.carname = carname
        self.drivername = drivername
        self.racingLinePointInf = racingLinePointInf
        self.racingLinePointSup = racingLinePointSup
        self.dist_lap = dist_lap
        self.next_interface_idx = next_interface_idx
        self.dist_next_interface = dist_next_interface
        self.bgeGuide = BGEGuide(scene,self.getGuideName())
        self.bgeCarPositionHandler = BGECarPositionHandler(self)
        self.start_race = True
    
    def __repr__(self):
        return ('BGECar - ' + self.carname
                + ' - RLInf/Sup: ' + str(self.racingLinePointInf)
                + '/' + str(self.racingLinePointSup)
                + ' - dist_lap: ' + str(self.dist_lap)
                + ' - nxt_intrf_idx: ' + str(self.next_interface_idx)
                + ' - dist_nxt_intrf: ' + str(self.dist_next_interface)
                + ' - ' + str(self.bgeGuide)
                + ' - dist_guide: ' + str(self.getDistToGuide()))

    #observer pattern - need to register each car to race manager
    def registerRaceManager(self,raceManager):
        self.raceManager = raceManager
    
    #notify race manager of end of lap event
    def notifyEndOfLap(self):
        self.raceManager.notifyEndOfLap(self)
        
    def getLinearVelocity(self):
        return self.scene.objects[self.carname].getLinearVelocity(True)

    def getVelocity(self):
        return self.scene.objects[self.carname].getVelocity()

    def getSpeed(self):
        return self.getLinearVelocity().y
    
    def getPosition(self):
        return self.scene.objects[self.carname].position

    #get guide name from car name
    def getGuideName(self):
        return self.carname + '_Guide'

    #distance to guide - usefull for debug
    def getDistToGuide(self):
        return (self.getPosition() - self.bgeGuide.getPosition()).length
    
    #project AI guide forward on the spline
    #at a distance computed as a product of velocity
    def projectGuide(self):
        self.bgeGuide.setPosition(self.racingLine.projectPosition(self))
    
    #update car own variables - this method is called by AIController all the time
    #delegate the update to a BGECarHandler object
    def update(self):
        self.bgeCarPositionHandler.update()
    
    #compute car position projected orthogonally on the racing line
    def getOrthPosition(self):
        return tools3d.projectOrth(self.getPosition(),
                                   self.racingLine.getCoord(self.racingLinePointInf),
                                   self.racingLine.getCoord(self.racingLinePointSup))
