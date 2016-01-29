import bge
from car_game_lib import toolbox_3d as tools3d

#########################################
#
#   Powertrain.py  Blender 2.6
#
#   tutorial can be found at
#
#   www.tutorialsforblender3d.com
#
#   Released under the Creative Commons Attribution 3.0 Unported License.	
#
#   If you use this code, please include this information header.
#
##########################################

def PowerTrain():

    #get current controller
    controller = bge.logic.getCurrentController()
    
    # get vehicle constraint ID
    vehicleID = ConstraintID(controller)
	
    # brakes
    brakes = Brakes(vehicleID, controller)
            
    # gas & reverse
    Power( vehicleID, controller, brakes)
    #Power( vehicleID, controller)
            
    # steering
    Steering(vehicleID, controller)

# get vehicle constraint ID
def ConstraintID(controller):

    # get car the controller is attached to
    carObj = controller.owner
            
    # get saved vehicle Constraint ID
    vehicleID = carObj["vehicleID"]
    
    return vehicleID

def Brakes(vehicleID,controller):
    
    carObj = controller.owner
    
    # set braking amount
    # front and back brakes
    brakeAmount = carObj['brakeAmount']
    
    # get sensors
    reverse = controller.sensors['Reverse']
    brake = controller.sensors["Brake"]
    
    # brake
    if brake.positive == True and reverse.positive == False:
            
        front_Brake = brakeAmount
        back_Brake = brakeAmount
        brakes = True

    # no brakes
    else:
            
        front_Brake = 0.0
        back_Brake = 0.0
        brakes = False
    
    # brakes	
    vehicleID.applyBraking( front_Brake, 0)
    vehicleID.applyBraking( front_Brake, 1)
    vehicleID.applyBraking( back_Brake, 2)
    vehicleID.applyBraking( back_Brake, 3)

    return brakes

# gas and reverse
def Power(vehicleID,controller,brakes):	
	
    # car obj
    carObj = controller.owner

    #current car speed
    carspeed = carObj.getLinearVelocity(True)
    carspeed = carspeed.y
    
    #sensors
    slowerGround = controller.sensors['slowerGround']
    gas = controller.sensors['Gas']
    reverse = controller.sensors['Reverse']
    
    maxSpeed,gasPower = getCarMaxSpeedAndPower(carObj,reverse.positive,slowerGround.positive)
    
    # brakes
    if brakes == True:
        power = 0.0

    elif reverse.positive == True and carspeed>0:
        power = -gasPower
        
    elif gas.positive or reverse.positive:
        if carspeed > maxSpeed:
            power = gasPower
        else:
            carObj.linVelocityMax = maxSpeed
            power = -gasPower
    else:
        power = 0.0
    
    # apply power
    vehicleID.applyEngineForce(power,0)
    vehicleID.applyEngineForce(power,1)
    vehicleID.applyEngineForce(power,2)
    vehicleID.applyEngineForce(power,3)

#get max speed and reverse power based on reverse and ground flags
def getCarMaxSpeedAndPower(carObj,reverseFlag,slowerGroundFlag):
    if reverseFlag:
        if slowerGroundFlag:
            return carObj['maxSpeedReverseGrass'],-carObj['gasPowerGrass'] 
        else:
            return carObj['maxSpeedReverse'],-carObj['gasPower'] 
    else:
        if slowerGroundFlag:
            return carObj['maxSpeedGrass'],carObj['gasPowerGrass'] 
        else:
            return carObj['maxSpeed'],carObj['gasPower'] 

#steering
def SteeringMethod2(vehicleID,controller):

    
    #get current steer value
    carObj = controller.owner
    curr_steer = carObj['current_steer_value']
    
    #steer shift value
    steer_shift = 0.01

    #steer max
    max_steer = 0.4

    #get steering sensors
    steerLeft = controller.sensors['Left']
    steerRight = controller.sensors['Right']
            
    #turn left	
    if steerLeft.positive == True:
        turn = min(curr_steer + steer_shift,max_steer)
    
    #turn right	
    elif steerRight.positive == True:
        turn = max(curr_steer - steer_shift,-max_steer)
    
    #steer comes back to middle (0.0)
    else:
        #wheel is turned to the left
        if curr_steer > 0.0:
            turn = max(curr_steer - steer_shift, 0.0)
        #wheel is turned to the right
        elif curr_steer < 0.0:
            turn = min(curr_steer + steer_shift, 0.0)
        #wheel is already at the middle, keep it like that
        else:
            turn = 0.0

    #update current steering value car property
    print('turn: ' + str(turn))
    carObj['current_steer_value'] = turn
    
    #steer with front tires only
    vehicleID.setSteeringValue(turn,0)
    vehicleID.setSteeringValue(turn,1)

#steering
def Steering(vehicleID,controller):
    
    #get turn value to interpolate to
    turn = getTurn(controller)
    #turn = 0.5
    #print('turn: ' + str(turn))
    
    # get steering sensors
    steerLeft = controller.sensors['Left']
    steerRight = controller.sensors['Right']
            
    # turn left	
    if steerLeft.positive == True:
        turn = turn
    
    # turn right	
    elif steerRight.positive == True:
        turn = -turn
    
    # go straight	
    else:
        turn = 0.0
            
    # steer with front tires only
    vehicleID.setSteeringValue(turn,0)
    vehicleID.setSteeringValue(turn,1)

#compute turn value based on current speed
def getTurn(controller):
    
    # car obj
    carObj = controller.owner
    
    reverse = controller.sensors['Reverse']
    if reverse.positive == True:
        return carObj['reverseTurn']
    
    #current and max car speed
    carSpeed = carObj.getLinearVelocity(True).y
    carMaxSpeed = carObj['maxSpeed']
    
    #interpolation switch speed:
    #maxSpeed/4
    switchSpeed = carMaxSpeed/4
    
    #interpolate based on current speed
    if carSpeed < switchSpeed:
        return tools3d.linearInterpolation(
            carSpeed,
            0,carObj['minSpeedTurn'],
            switchSpeed,carObj['switchSpeedTurn'])
    else:
        return tools3d.linearInterpolation(
            carSpeed,
            switchSpeed,carObj['switchSpeedTurn'],
            carMaxSpeed,carObj['maxSpeedTurn'])	
