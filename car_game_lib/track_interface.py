##############################################################################
## TrackInterface object:
## holds point index to which it refers to on RacingLine
## and target speed a AI car should achieve when crossing it
##############################################################################

class TrackInterface():
    
    def __init__(self,racingLinePointIdx,targetSpeed,coord):
        self.racingLinePointIdx = racingLinePointIdx
        self.targetSpeed = targetSpeed
        self.coord = coord
        
    def __repr__(self):
        return 'TrackInterface: ' + str(self.__dict__)
