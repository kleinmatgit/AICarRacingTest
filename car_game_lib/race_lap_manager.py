from car_game_lib.logger_handler import LoggerHandler
from car_game_lib import toolbox as tools
from operator import itemgetter
import time

#########################################
## RaceLapManager
## Handle race lap events
#########################################

class RaceLapManager:

    #maintains dictionary of lap times for each car
    lap_times = {}

    #maintains current lap starting time for each car
    start_times = {}
    
    def __init__(self,bgeCars):
        self.bgeCars = bgeCars
        for bgeCar in bgeCars:
            self.lap_times[bgeCar.carname] = []
            self.start_times[bgeCar.carname] = time.time()
        #self.logger = LoggerHandler(appname=self.__class__.__name__)

    #return current lap # for given car (first lap is lap #1)
    def getCurrentLap(self,bgeCar):
        return len(self.lap_times[bgeCar.carname]) + 1
    
    #return completed lap # for given car
    def getCompletedLaps(self,bgeCar):
        return len(self.lap_times[bgeCar.carname])

    #handle end of lap for given car
    def notifyEndOfLap(self,bgeCar):

        #at start of race we don't want to record any best time
        if bgeCar.start_race:
            return
        
        #get end of lap time
        time_end = time.time()
        
        #compute lap time
        lap_time_secs = time_end - self.start_times[bgeCar.carname]
        
        #add lap time to list of lap times
        self.lap_times[bgeCar.carname].append(lap_time_secs)

        #reset starting time
        self.start_times[bgeCar.carname] = time_end

    #test race completion
    def raceCompleted(self,lap):
        for bgeCar in self.bgeCars:
            if not self.raceCompletedForCar(lap,bgeCar):
                return False
        return True
    
    #test race completion
    def raceCompletedForCar(self,lap,bgeCar):
        return self.getCompletedLaps(bgeCar) == lap

    #return best lap for given car
    def getBestLap(self,bgeCar):
        return min(self.lap_times[bgeCar.carname])
    
    #get sorted list of driver from fastest to slowest
    def getSortedBestTimes(self):

        #convert dic of best times to list of tuple (driver,lap_time)
        driver_time = []

        for bgeCar in self.bgeCars:
            for t in self.lap_times[bgeCar.carname]:
                driver_time.append((bgeCar.drivername,t))
        
        if len(driver_time) > 0:
            #convert to sorted list of tuple (drivername,best_time)
            #ordered from fastest to slowest
            return sorted(driver_time,key=itemgetter(1))
        else:
            return []

    #get sorted list of driver from fastest to slowest
    def getSortedBestTimesOld(self):

        #dic of best time for each car
        best_times = {}
        for bgeCar in self.bgeCars:
            if len(self.lap_times[bgeCar.carname]) > 0:
                best_times[bgeCar.drivername] = self.getBestLap(bgeCar)

        if len(best_times) > 0:
            #convert to sorted list of tuple (drivername,best_time)
            #ordered from fastest to slowest
            return sorted(best_times.items(),key=itemgetter(1))
        else:
            return []

    #print nicely list of best lap times, from fastest to longest
    def printBestLapTimesNicely(self):

        best_time_tuples = self.getSortedBestTimes()
        s = '\nBest laps:\n'
        if len(best_time_tuples) > 0:
            i = 1
            for t in best_time_tuples:
                s += (tools.positionAsString(i)
                      + ': ' + t[0] + ' - '
                      + tools.convertFloatToTimeStr(t[1]) + '\n')
                i += 1
        else:
            s += 'No lap time available yet\n'
        return s
