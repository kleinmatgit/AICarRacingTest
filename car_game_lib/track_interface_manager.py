from car_game_lib.track_interface import TrackInterface

################################################
## TrackInterfaceManager:
## (has-a relationship with a RacingLine)
## maintains list of TrackInterfaces
## and list of distances between each interface
################################################

class TrackInterfaceManager():

    #interfaces is a list of tuple (index on racing line, target speed)
    def __init__(self,racingLine,interfaces):
        self.racingLine = racingLine
        self.trackInterfaces = []
        self.interfaceDistances = []
        for i in range(0,len(interfaces)):
            self.trackInterfaces.append(
                TrackInterface(interfaces[i][0],interfaces[i][1],racingLine.getCoord(interfaces[i][0])))
            self.interfaceDistances.append(self.racingLine.getRelativeDistance(interfaces[i-1][0],interfaces[i][0]))
        
    def __repr__(self):
        strRes = 'TrackInterfaceManager:'
        for i in range(0,len(self.trackInterfaces)):
            strRes += '\n[' + str(i) + ']' + str(self.trackInterfaces[i]) + ', distance to previous=' + str(self.interfaceDistances[i])
        return strRes
    
    #get methods for interface object
    def getInterface(self,i):
        return self.trackInterfaces[i]

    def getNextInterface(self,i):
        if i==len(self.trackInterfaces)-1:
            return self.trackInterfaces[0]
        else:
            return self.trackInterfaces[i+1]

    def getPreviousInterface(self,i):
        return self.trackInterfaces[i-1]
    
    #get methods for interface target speed
    def getInterfaceTargetSpeed(self,i):
        return self.getInterface(i).targetSpeed

    def getNextInterfaceTargetSpeed(self,i):
        return self.getNextInterface(i).targetSpeed
    
    def getPreviousInterfaceTargetSpeed(self,i):
        return self.getPreviousInterface(i).targetSpeed
    
    #get methods for interface index
    def getNextInterfaceIdx(self,i):
        if i==len(self.trackInterfaces)-1:
            return 0
        else:
            return i+1

    def getPreviousInterfaceIdx(self,i):
        if i==0:
            return len(self.trackInterfaces)-1
        else:
            return i-1
    
    #get methods for interface racing line index
    def getInterfaceRLIdx(self,i):
        return self.trackInterfaces[i].racingLinePointIdx
    
    #get distance with previous interface for track interface of given index
    def getDistanceWithPreviousInterface(self,i):
        return self.interfaceDistances[i]

    #get coordinate of given interface
    def getInterfaceCoord(self,i):
        return self.getInterface(i).coord

    
     
    
