from car_game_lib.race_ranking_manager import RaceRankingManager
from car_game_lib.race_lap_manager import RaceLapManager
from car_game_lib.logger_handler import LoggerHandler

#########################################
## RaceManager
## Handle race events:
## - ranking
## - fastest lap
## - etc
#########################################

class RaceManager:

    def __init__(self,controllers,bgeCars,racingLine,lap=2):
        self.controllers = controllers
        self.bgeCars = bgeCars
        self.registerCars()
        self.racingLine = racingLine
        self.lap = lap
        self.raceLapManager = RaceLapManager(bgeCars)
        self.raceRankingManager = RaceRankingManager(bgeCars,racingLine,self.raceLapManager)
        self.logger = LoggerHandler(appname=self.__class__.__name__)

    #observer pattern - need to register each car to race manager
    def registerCars(self):
        for bgeCar in self.bgeCars:
            bgeCar.registerRaceManager(self)
    
    #return list of carname ordered by crossed distance DESC
    def getRanking(self):
        return self.raceRankingManager.getRanking()

    #log current ranking
    def logCurrentRanking(self):
        self.logger.info(self.raceRankingManager.printCurrentRankingNicely())

    #log final ranking
    def logFinalRanking(self):
        self.logger.info(self.raceRankingManager.printFinalRankingNicely())
    
    #log best lap times
    def logBestLapTimes(self):
        self.logger.info(self.raceLapManager.printBestLapTimesNicely())

    #kind of observer pattern:
    #bgeCar will call this method and pass itself as argument
    #to notify raceManager that it has finished a lap
    #raceManager then handles all necessary action
    def notifyEndOfLap(self,bgeCar):
        
        #update list of lap time
        self.raceLapManager.notifyEndOfLap(bgeCar)

        #test race completion for given car
        if self.raceCompletedForCar(bgeCar):

            self.raceRankingManager.addToFinalRanking(bgeCar)
            
            #update controller to end of race state - if AI
            if bgeCar.carname[:3] == 'cpu':
                controller = self.controllers[bgeCar.carname]
                controller.setControl('eor')
            
            #test race completion
            if self.raceCompleted():
                self.logger.info('\n' +
                                 '############################################\n' +
                                 '######### RACE COMPLETED ###################\n' +
                                 '############################################\n')
                self.logFinalRanking()
                self.logBestLapTimes()

    #test race completion
    def raceCompleted(self):
        return self.raceLapManager.raceCompleted(self.lap)

    #test race completion
    def raceCompletedForCar(self,bgeCar):
        return self.raceLapManager.raceCompletedForCar(self.lap,bgeCar)
        
        
    

        
                        
                           
                        
