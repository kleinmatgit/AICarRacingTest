import os
import re
from car_game_lib.bge_car import BGECar
from car_game_lib.racing_line_factory import RacingLineFactory
from car_game_lib.track_interface_factory import TrackInterfaceFactory

#########################################
## BGECar factory
#########################################

class BGECarFactory:

    file_pattern = 'cars.txt'
    
    def __init__(self,scene):
        self.scene = scene
    
    #create list of BGECars from a file containing car descriptions
    def createFromFile(self,path,racingLines,tiManagers):
        bgeCars = []
        cars = self.getCarsList(path)
        for car in cars:
            bgeCars.append(self.createCar(car[0],
                                          car[1],
                                          racingLines[car[2]],
                                          tiManagers[car[2]]))
        return bgeCars
    
    #create a BGECar from few parameters
    def createCar(self,carname,drivername,racingLine,tiManager):

        carObj_position = self.scene.objects[carname].position
    
        idx_closest = racingLine.getClosestPoint(carObj_position)
        idx_prev = racingLine.getPreviousIndex(idx_closest)
        idx_next = racingLine.getNextIndex(idx_closest)
        
        dist_car_prev = (carObj_position - racingLine.getCoord(idx_prev)).length
        dist_car_next = (carObj_position - racingLine.getCoord(idx_next)).length
        
        if dist_car_prev < dist_car_next:
            return BGECar(racingLine,tiManager,self.scene,carname,drivername,idx_prev,idx_closest)
        else:
            return BGECar(racingLine,tiManager,self.scene,carname,drivername,idx_closest,idx_next)
    
    #read a txt file describing cars and returns list of tuple:
    #(carname,drivername,race_item_key)
    def getCarsList(self,path):
        cars = []
        f = open(path + self.file_pattern,'r')
        expr = r'\((.*),(.*),(.*)\)'
        for line in f.readlines():
            matchObj = re.match(expr,line.strip())
            if matchObj:
                cars.append([matchObj.group(1),
                             matchObj.group(2),
                             matchObj.group(3)])
        f.close()
        return cars
