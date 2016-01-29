###########################################
## Wrap a car guide in blender game engine
###########################################

class BGEGuide:
    
    def __init__(self,scene,guidename):
        self.scene = scene
        self.guidename = guidename
        
    def __repr__(self):
        return 'BGEGuide - ' + self.guidename + ' (Position=' + str(self.getPosition()) + ')'
    
    def getPosition(self):
        return self.scene.objects[self.guidename].position

    def setPosition(self,position):
        self.scene.objects[self.guidename].position = position
