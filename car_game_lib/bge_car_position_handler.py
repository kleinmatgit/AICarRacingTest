from car_game_lib import toolbox_3d as tools3d
from car_game_lib.logger_handler import LoggerHandler

#########################################
## Handle position of BGECar
#########################################

class BGECarPositionHandler:

    def __init__(self,bgeCar):
        self.bgeCar = bgeCar
        self.logger = LoggerHandler(appname=self.bgeCar.carname + self.__class__.__name__)

    #update internal state based on recent position
    def update(self):

        self.logger.info(str(self.bgeCar))

        idx_inf = self.bgeCar.racingLinePointInf
        idx_sup = self.bgeCar.racingLinePointSup
        iprev = self.bgeCar.racingLine.getPreviousIndex(idx_inf)
        inext = self.bgeCar.racingLine.getNextIndex(idx_sup)

        carobj_position = self.bgeCar.getPosition()
        vecSupInf = self.bgeCar.racingLine.getCoord(idx_sup) - self.bgeCar.racingLine.getCoord(idx_inf)
        vecSupCar = self.bgeCar.racingLine.getCoord(idx_sup) - carobj_position
        vecInfCar = self.bgeCar.racingLine.getCoord(idx_inf) - carobj_position
        vecInfSup = self.bgeCar.racingLine.getCoord(idx_inf) - self.bgeCar.racingLine.getCoord(idx_sup)
        
        #get previous/next interface point index
        next_interface_idx = self.bgeCar.next_interface_idx
        next_interface_point_idx = self.bgeCar.tiManager.getInterface(next_interface_idx).racingLinePointIdx
        prev_interface_point_idx = self.bgeCar.tiManager.getPreviousInterface(next_interface_idx).racingLinePointIdx

        #check angle at point_idx_inf (inf to car and inf to sup): if superior to 90 degree, need to increment idx
        #ie: car is moving forward as expected
        if tools3d.angleFormated(vecSupInf,vecSupCar)>90.0:

            
            #print('going forward: ' + str(vecSupInf.angle(vecSupCar)))
            self.bgeCar.racingLinePointInf = idx_sup
            self.bgeCar.racingLinePointSup = inext
            
            #check if need to increment interface (idx_sup is then the new 'point_idx_inf')
            if idx_sup==next_interface_point_idx:
                self.shiftInterfaceByOne(1)
            
            #check for new lap (idx_sup is then the new 'point_idx_inf')
            if idx_sup == 0:
                self.bgeCar.notifyEndOfLap()
                self.bgeCar.start_race = False
                #self.logger.info(str(self.bgeCar))

        #check angle at point_idx_sup (sup to car and sup to inf): if superior to 90 degree, need to decrement idx
        #ie: car is somehow moving backward for some reason
        elif tools3d.angleFormated(vecInfSup,vecInfCar)>90.0:

            #print('going backward: ' + str(vecSupInf.angle(vecInfCar)))
            self.bgeCar.racingLinePointInf = iprev
            self.bgeCar.racingLinePointSup = idx_inf
            
            #check if need to decrement interface (idx_inf is then the new 'point_idx_sup')
            if idx_inf==next_interface_point_idx:
                self.shiftInterfaceByOne(-1)

        #project car position orthogonally on the racing line
        orth_pos = self.bgeCar.getOrthPosition()
                        
        #distance to next interface
        self.bgeCar.dist_next_interface = self.getDistanceToNextInterface(orth_pos)
        
        #distance in current lap
        self.bgeCar.dist_lap = self.getDistanceLap(orth_pos)
    
    #increment/decrement car object's next interface by one
    def shiftInterfaceByOne(self,iShift):
        if iShift==1:
            self.bgeCar.next_interface_idx = self.bgeCar.tiManager.getNextInterfaceIdx(self.bgeCar.next_interface_idx)
        elif iShift==-1:
            self.bgeCar.next_interface_idx = self.bgeCar.tiManager.getPreviousInterfaceIdx(self.bgeCar.next_interface_idx)
    
    #get distance between car position (orthogonally projected on the spline)
    #and the next interface
    def getDistanceToNextInterface(self,carobj_position_orth):
        
        idx_inf = self.bgeCar.racingLinePointInf
        idx_sup = self.bgeCar.racingLinePointSup

        #distance between proj orth and next point
        dist = (carobj_position_orth - self.bgeCar.racingLine.getCoord(idx_sup)).length
        
        #remaining distance to next interface
        remaining_dist = self.bgeCar.racingLine.getRelativeDistance(
            idx_sup,self.bgeCar.tiManager.getInterfaceRLIdx(self.bgeCar.next_interface_idx))
        
        #case when AI are thrown far from the track
        #the interface count may then be screwed up
        #in that case we just need to reset next interface idx
        if dist + remaining_dist > max(self.bgeCar.tiManager.interfaceDistances):
            #TO DO
            print('issue')
        
        return dist + remaining_dist
    
    #compute distance in current lap
    #-> used by RaceManager to get ranking
    def getDistanceLap(self,carobj_position_orth):

        #special case - start of the race
        if self.bgeCar.start_race:
            return 0.0
        
        #get distance between pos orth and previous point
        dist_orth_prev = (carobj_position_orth - self.bgeCar.racingLine.getCoord(self.bgeCar.racingLinePointInf)).length

        #get distance between previous point and racing line starting point (point[0])
        dist_prev_start = self.bgeCar.racingLine.getDistanceToStart(self.bgeCar.racingLinePointInf)
        
        return dist_orth_prev + dist_prev_start
