import re
from car_game_lib.track_interface_manager import TrackInterfaceManager


#########################################
## Factory for TrackInterface
#########################################

class TrackInterfaceFactory():

    file_pattern = '_track_interfaces.txt'
    
    #create TrackInterfaceManager from list of tuple(index on racing line, target speed)
    def create(self,racingLine,interfaces):
        return TrackInterfaceManager(racingLine,interfaces)
    
    #create TrackInterfaceManager from file containing list of tuple..
    def createFromFile(self,racingLine,file_full_path):
        return TrackInterfaceManager(racingLine,self.readInterfacesFromFile(file_full_path))
    
    #create TrackInterfaceManagers dictionary from list of items
    #and racing lines dictionary
    def createFromList(self,path,items,racingLines):
        tiManagers = {}
        for item in items:
            tiManagers[item] = self.createFromFile(racingLines[item],path + item + self.file_pattern)
        return tiManagers
        
    #read a list of track interface from file
    def readInterfacesFromFile(self,file_full_path):
        interfaces = []
        f = open(file_full_path,'r')
        expr = r'^.*\(([0-9]+),([0-9]+\.[0-9]+)\)'
        for line in f.readlines():
            matchObj = re.match(expr,line.strip())
            if matchObj:
                interfaces.append((int(matchObj.group(1)),float(matchObj.group(2))))
        f.close()
        return interfaces
            
    
