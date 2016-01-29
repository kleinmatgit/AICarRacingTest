from mathutils import Vector
from car_game_lib import toolbox_3d as tools3d
from car_game_lib.logger_handler import LoggerHandler

##############################################################
## RacingLine:
## holds list of points position around a track
## also keeps points distance to each other
##############################################################

class RacingLine():

    #list of tuple (point coordinate, dist with previous point, dist with first point)
    points = []

    #length of the spline
    length = 0.0
    
    def __init__(self,points,length):
        self.points = points
        self.length = length
        #self.logger = LoggerHandler(appname=self.__class__.__name__)
        
    def __repr__(self):
        return ('RacingLine: ' \
                + '\n#points: ' + str(len(self.points)) \
                + '\nLength: ' + str(self.length))

    def printPoints(self):
        for i in range(len(self.points)):
            print('point['+str(i)+']: ' + str(self.points[i]))
    
    def getLength(self):
        return self.length

    #get next point index on the spline
    def getNextIndex(self,i):
        if i==len(self.points)-1:
            return 0
        else:
            return i+1

    #get previous point index on the spline
    def getPreviousIndex(self,i):
        if i==0:
            return len(self.points)-1
        else:
            return i-1

    #get point index coordinates
    def getCoord(self,i):
        return self.points[i][0]

    #get point index distance to previous point
    def getDistanceToPrevious(self,i):
        return self.points[i][1]
    
    #get point index distance to previous point
    def getDistanceToStart(self,i):
        return self.points[i][2]
    
    #project point to a certain distance on the spline
    #return new point and next spline point index
    def projectPointToDistance(self,point,iNext,distance):

        fun = '[projectPointToDistance]'
        
        #distance between point and next point
        iPrev = self.getPreviousIndex(iNext)
        currDist = (self.points[iNext][0]-point).length

##        self.logger.info(fun + 'distance: ' + str(distance))
##        self.logger.info(fun + 'iNext: ' + str(iNext))
##        self.logger.info(fun + 'iPrev: ' + str(iPrev))
##        self.logger.info(fun + 'currDist: ' + str(currDist))
                
        #search for target point
        bInLoop = False
        while currDist < distance:
            bInLoop = True
            iPrev = iNext
            iNext = self.getNextIndex(iNext)
            currDist += self.points[iNext][1]
##            self.logger.info(fun + 'iPrev: ' + str(iPrev))
##            self.logger.info(fun + 'iNext: ' + str(iNext))
##            self.logger.info(fun + 'currDist: ' + str(currDist))
        
        #remaining dist:
        if bInLoop:
            remaining_dist = self.points[iNext][1] - (currDist - distance)
            coord_start = self.points[iPrev][0]
        else:
            remaining_dist = distance
            coord_start = point

##        self.logger.info(fun + 'rem dist: ' + str(remaining_dist))
##        self.logger.info(fun + 'coord_start: ' + str(coord_start))

##        coord_end = self.points[iNext][0]
##        self.logger.info(fun + 'coord_end: ' + str(coord_end))
        
        #project remaining distance from previous point
        coord2D = tools3d.projectDistBetween2Points(coord_start.x,coord_start.y,
                                         self.points[iNext][0].x,self.points[iNext][0].y,remaining_dist)

##        vec_coord2D = Vector([coord2D[0],coord2D[1],point.z])
##        
##        self.logger.info(fun + 'coord2D: ' + str(coord2D))
##        self.logger.info(fun + 'vec_coord2D: ' + str(vec_coord2D))
##
##        self.logger.info(fun + 'diff (coord2D/coordStart): ' + str((vec_coord2D-coord_start).length))
        
        return Vector([coord2D[0],coord2D[1],point.z])
    
    #return closest points index on the spline given a car object position
    #note: index preceding closest point is returned in the case where object position is almost passing the closest point
    def getClosestPoint(self,position,start_index=0):

        #init variables
        min_dist = (position - self.points[start_index][0]).length
        closest_index = start_index
        last_index = self.getPreviousIndex(start_index)
        
        i = start_index + 1
        while i != start_index:
            new_dist = (position - self.points[i][0]).length
            if new_dist < min_dist:
                min_dist = new_dist
                closest_index = i
            i = self.getNextIndex(i)

        return closest_index
    
    #get relative distance between 2 points on the spline
    #by passing through all the points between the 2
    def getRelativeDistance(self,idx1,idx2):
        i = idx1
        dist = 0.0
        while i != idx2:
            i = self.getNextIndex(i)
            dist += self.points[i][1]
        return dist
    
    #project the position of a car object to a certain distance on the spline
    #it will first project the position orthogonally on the spline
    #then project to a distance which is a factor of car speed
    def projectPosition(self,bgeCar):

        fun = '[projectPosition]'

        idx_inf = bgeCar.racingLinePointInf
        idx_sup = bgeCar.racingLinePointSup
        fact = 0.4
        speed = bgeCar.getSpeed()
        dist = speed * fact
        
##        self.logger.info(fun + 'expected distance: ' + str(dist))
        
        #we project car object position orthogonally on the spline
        carobj_position_orth = tools3d.projectOrth(bgeCar.getPosition(),
                                                   self.getCoord(idx_inf),
                                                   self.getCoord(idx_sup))
        
##        self.logger.info(fun + 'distance to orth pos: ' + str((bgeCar.getPosition()-carobj_position_orth).length))

        #then we project forward on the spline
        final_position = self.projectPointToDistance(carobj_position_orth,idx_sup,dist)
        
##        self.logger.info(fun + 'actual distance: ' + str((bgeCar.getPosition()-final_position).length))
##        self.logger.info(fun + 'difference: ' + str((bgeCar.getPosition()-final_position).length-dist))
        
        return final_position
        
