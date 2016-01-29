from car_game_lib.logger_handler import LoggerHandler
from car_game_lib import toolbox as tools
from operator import itemgetter

#########################################
## RaceRankingManager
## Handle race ranking events
#########################################

class RaceRankingManager:

    final_ranking = []
    
    def __init__(self,bgeCars,racingLine,raceLapManager):
        self.bgeCars = bgeCars
        self.racingLine = racingLine
        self.raceLapManager = raceLapManager
        #self.logger = LoggerHandler(appname=self.__class__.__name__)
    
    #return list of drivername ordered by crossed distance DESC
    def getRanking(self):
        ranking = []
        for bgeCar in self.bgeCars:
            ranking.append((bgeCar.drivername,self.getCrossedDistance(bgeCar)))            
        return sorted(ranking,key=itemgetter(1),reverse=True)

    #return current ranking as a nice string:
    def printCurrentRankingNicely(self):
        i = 1
        s = '\nRanking:\n'
        for t in self.getRanking():
            s += tools.positionAsString(i) + ': ' + t[0] + '\n'
            i += 1
        return s

    #return final ranking as a nice string:
    def printFinalRankingNicely(self):
        i = 1
        s = '\nFinal Ranking:\n'
        for t in self.final_ranking:
            s += tools.positionAsString(i) + ': ' + t + '\n'
            i += 1
        return s

    #add driver name to final ranking list
    def addToFinalRanking(self,bgeCar):
        self.final_ranking.append(bgeCar.drivername)
    
    #get total distance that a car has crossed so far
    def getCrossedDistance(self,bgeCar):
        if self.raceLapManager.getCurrentLap(bgeCar) == 0:
            return 0.0
        else:
            return bgeCar.dist_lap + (self.raceLapManager.getCurrentLap(bgeCar)-1) * self.racingLine.length
    

        
                        
                           
                        
