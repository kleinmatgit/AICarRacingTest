import bge

def Speed():
    
    # get the current controller
    controller = bge.logic.getCurrentController()
    
    # car obj
    carObj = controller.owner
    
    # set car speed
    setSpeedIndicator(carObj)
    
#set speed indicator 
def setSpeedIndicator(carObj):
    # get velocity vector
    carObj["speed_indicator"] = getCarSpeed(carObj)

#get car speed 
def getCarSpeed(carObj):
    # get velocity vector
    velocity = carObj.getLinearVelocity(True)
    # speed is y coordinates since we pass true to getLinearVelocity
    return velocity.y
