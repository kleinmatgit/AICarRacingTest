from car_game_lib import toolbox_3d as tools3d
from car_game_lib.racing_line_factory import RacingLineFactory
from car_game_lib.track_interface_factory import TrackInterfaceFactory
from car_game_lib.bge_car_factory import BGECarFactory
from car_game_lib.race_manager import RaceManager
from car_game_lib.speed_controller import SpeedController
from car_game_lib.steering_controller import SteeringController
from car_game_lib.controller_factory import ControllerFactory
from car_game_lib.human_controller import HumanController
from mathutils import Vector

##############################################################
## Unit test for all objects
##############################################################

class UnitTest:
    
    test_total = 0
    test_success = 0

    #function wrapper to display test result
    def printMethodResult(self,myType,descr,bResult):
        msg = "Testing " + myType.__name__ + " - "
        if bResult:
            print(msg + descr + ": OK")
            self.test_success += 1
        else:
            print(msg + descr + ": Test failed")
        self.test_total += 1

    #test generic function which takes a list of args (can be only 1 arg)
    #and return a value
    def testFunGeneric(self,myType,fun,args,expected):
        self.printMethodResult(myType,fun.__name__,fun(*args) == expected)

    #test generic function which takes a list of args (can be only 1 arg)
    #and return a value
    def testFunGenericWithRound(self,myType,fun,args,expected,digit):
        self.printMethodResult(myType,fun.__name__,round(fun(*args) - expected,digit) == 0)

    #test function which return 2D coordinates
    #we introduce specificity because of necessary rounding
    def testFun2DCoords(self,myType,fun,args,expected_2d_coord):
        coord = fun(*args)
        bResult = (round(coord[0]-expected_2d_coord[0],0) == 0 and
                   round(coord[1]-expected_2d_coord[1],0) == 0)
        self.printMethodResult(myType,fun.__name__,bResult)

    #test 2 values are equal
    def testValGeneric(self,myType,descr,v,expected):
        self.printMethodResult(myType,descr,v == expected)

    #test 2 values are different
    def testValGenericDiff(self,myType,descr,v,expected):
        self.printMethodResult(myType,descr,v != expected)

    #test function which return a vector against another vector
    #each coordinates must be roughly equal
    def testFunVectorWithRound(self,myType,fun,args,expected_vec,digit):
        vec = fun(*args)
        bResult = (round(vec.x - expected_vec.x,digit) == 0 and
                   round(vec.y - expected_vec.y,digit) == 0 and
                   round(vec.z - expected_vec.z,digit) == 0)
        self.printMethodResult(myType,fun.__name__,bResult)

    #test a vector against another vector
    #each coordinates must be roughly equal
    def testVectorWithRound(self,myType,descr,vec,expected_vec,digit):
        bResult = (round(vec.x - expected_vec.x,digit) == 0 and
                   round(vec.y - expected_vec.y,digit) == 0 and
                   round(vec.z - expected_vec.z,digit) == 0)
        self.printMethodResult(myType,descr,bResult)
                   
    def printSeparator(self):
        print('----------------------------------------------------')
    
    #main function to run all unit tests
    def run(self,scene,spline,scale,divisor,race_items_path,race_items):

        #toolbox3D
        myType = type(tools3d)
        self.testFun2DCoords(myType,tools3d.projectDistBetween2Points,[1,2,5,2,1.0],(2.0,2.0))
        self.testFun2DCoords(myType,tools3d.projectDistBetween2Points,[5,2,1,2,1.0],(4.0,2.0))
        self.testFun2DCoords(myType,tools3d.projectDistBetween2Points,[1,5,1,1,1.0],(1.0,4.0))
        self.testFun2DCoords(myType,tools3d.projectDistBetween2Points,[1,1,1,5,1.0],(1.0,2.0))
        self.testFun2DCoords(myType,tools3d.projectDistBetween2Points,[360.0,8.0,379.0,-27.0,2.78],(361.32,5.55))
        self.printSeparator()
        
        #racing line
        racingLineFactory = RacingLineFactory()
        racingLineFromSpline = racingLineFactory.createFromSpline(spline,scale,divisor)
        #racingLineFromSpline.printPoints()
        myType = type(racingLineFromSpline)
        self.testValGeneric(myType,'createFromSpline',len(racingLineFromSpline.points),36)
        racingLines = racingLineFactory.createFromList(race_items_path,race_items)
        racingLineBezier = racingLines['BEZIER']
        self.testValGeneric(myType,'createFromList',len(racingLineBezier.points),36)
        self.testFunGeneric(myType,racingLineBezier.getNextIndex,[0],1)
        self.testFunGeneric(myType,racingLineBezier.getPreviousIndex,[1],0)
        self.testFunGeneric(myType,racingLineBezier.getNextIndex,[35],0)
        self.testFunGeneric(myType,racingLineBezier.getPreviousIndex,[0],35)
        self.testFunGeneric(myType,racingLineBezier.getDistanceToPrevious,[1],120.0)
        self.testFunGeneric(myType,racingLineBezier.getDistanceToPrevious,[2],120.0)
        self.testFunGeneric(myType,racingLineBezier.getDistanceToStart,[1],120.0)
        self.testFunGeneric(myType,racingLineBezier.getDistanceToStart,[2],240.0)
        self.testFunGeneric(myType,racingLineBezier.getDistanceToStart,[0],0.0)
        self.testFunGeneric(myType,racingLineBezier.getDistanceToStart,
                            [35],racingLineBezier.getLength() - racingLineBezier.getDistanceToPrevious(0))
        self.testFunGeneric(myType,racingLineBezier.getClosestPoint,[Vector([-14.0,27.0,0.0])],0)
        self.testFunGeneric(myType,racingLineBezier.getClosestPoint,[Vector([-4.0,27.0,0.0])],0)
        self.testFunGeneric(myType,racingLineBezier.getClosestPoint,[Vector([80.0,27.0,0.0])],1)
        self.testFunGeneric(myType,racingLineBezier.getClosestPoint,[Vector([70.0,27.0,0.0])],1)
        self.testFunGeneric(myType,racingLineBezier.getClosestPoint,[Vector([-80.0,27.0,0.0])],35)
        self.testFunGeneric(myType,racingLineBezier.getClosestPoint,[Vector([-70.0,27.0,0.0])],35)
        self.testFunGeneric(myType,racingLineBezier.projectPointToDistance,[Vector([-25.0,24.0,0.0]),0,10.0],Vector([-15.0,24.0,0.0]))
        self.testFunGeneric(myType,racingLineBezier.projectPointToDistance,[Vector([-15.0,24.0,0.0]),0,30.0],Vector([15.0,24.0,0.0]))
        self.testFunGeneric(myType,racingLineBezier.projectPointToDistance,[Vector([-20.0,24.0,0.0]),0,200.0],Vector([180.0,24.0,0.0]))
        self.testFunGeneric(myType,racingLineBezier.projectPointToDistance,[Vector([-10.0,24.0,0.0]),1,30.0],Vector([20.0,24.0,0.0]))
        self.testFunGeneric(myType,racingLineBezier.projectPointToDistance,[Vector([-10.0,24.0,0.0]),1,120.0],Vector([110.0,24.0,0.0]))
        self.testFunGeneric(myType,racingLineBezier.projectPointToDistance,[Vector([-10.0,24.0,0.0]),1,150.0],Vector([140.0,24.0,0.0]))
        self.testFunGenericWithRound(myType,racingLineBezier.getRelativeDistance,[0,2],240,1)
        self.printSeparator()

        #track interface manager
        tiManagers = TrackInterfaceFactory().createFromList(race_items_path,race_items,racingLines)
        tiManager = tiManagers['BEZIER']
        myType = type(tiManager)
        self.testValGeneric(myType,'createFromList',len(tiManager.trackInterfaces),16)
        self.testFunGeneric(myType,tiManager.getInterfaceTargetSpeed,[0],100.0)
        self.testFunGeneric(myType,tiManager.getInterfaceTargetSpeed,[13],45.0)
        self.testFunGeneric(myType,tiManager.getNextInterfaceTargetSpeed,[5],30.0)
        self.testFunGeneric(myType,tiManager.getPreviousInterfaceTargetSpeed,[4],60.0)
        self.testFunGeneric(myType,tiManager.getInterfaceCoord,[0],Vector([-10.0,24.0,0.0]))
        self.testFunGeneric(myType,tiManager.getNextInterfaceIdx,[0],1)
        self.testFunGeneric(myType,tiManager.getPreviousInterfaceIdx,[0],15)
        self.printSeparator()
        
        #BGECar
        bgeCars = BGECarFactory(scene).createFromFile(race_items_path,racingLines,tiManagers)
        bgeCar = bgeCars[0]
        myType = type(bgeCar)
        self.testValGeneric(myType,'bgeCar.dist_lap',bgeCar.dist_lap,0.0)
        self.testValGeneric(myType,'bgeCar.next_interface_idx',bgeCar.next_interface_idx,0)
        self.testFunVectorWithRound(myType,bgeCar.getLinearVelocity,[],Vector([0.0,0.0,0.0]),0)
        self.testFunGenericWithRound(myType,bgeCar.getSpeed,[],0.0,0)
        self.testFunVectorWithRound(myType,bgeCar.getPosition,[],Vector([-14.42,27.28,0.37]),0)
        self.testFunVectorWithRound(myType,bgeCar.getOrthPosition,[],Vector([-14.42,24.0,0.0]),0)
        self.testFunGeneric(myType,bgeCar.getGuideName,[],bgeCar.carname + '_Guide')
        bgeCar.projectGuide()
        self.testVectorWithRound(myType,'projectGuide',bgeCar.bgeGuide.getPosition(),Vector([-14.42893,24.0,0.0]),0)
        self.printSeparator()
        
        #BGECarPositionHandler
        bgeCarPosHandler = bgeCar.bgeCarPositionHandler
        myType = type(bgeCarPosHandler)
        self.testFunGenericWithRound(myType,bgeCarPosHandler.getDistanceToNextInterface,[bgeCar.getOrthPosition()],4.42,1)
        self.testFunGeneric(myType,bgeCarPosHandler.getDistanceLap,[bgeCar.getOrthPosition()],0.0)
        bgeCarPosHandler.shiftInterfaceByOne(1)
        self.testValGeneric(myType,'shiftInterfaceByOne',bgeCar.next_interface_idx,1)
        bgeCarPosHandler.shiftInterfaceByOne(-1)
        self.testValGeneric(myType,'shiftInterfaceByOne',bgeCar.next_interface_idx,0)
        bgeCarPosHandler.shiftInterfaceByOne(-1)
        self.testValGeneric(myType,'shiftInterfaceByOne',bgeCar.next_interface_idx,15)
        #make sure last call to shiftInterface set car next interface to idx=0:
        bgeCarPosHandler.shiftInterfaceByOne(1)
        self.testValGeneric(myType,'shiftInterfaceByOne',bgeCar.next_interface_idx,0)
        #BGECar.update(): better to run after BGECarPositionHandler
        bgeCar.update()
        self.testVectorWithRound(myType,'update',bgeCar.getPosition(),Vector([-14.42,27.28,0.37]),0)
        self.printSeparator()

        #Controller
        controllers = ControllerFactory().createFromCars(bgeCars,SpeedController(),SteeringController())
        controller = controllers['cpu1']
        myType = type(controller)
        self.testValGeneric(myType,'creation',len(controllers.keys()),3)
        self.testValGenericDiff(myType,'type',type(controllers['car']),type(controllers['cpu1']))
        self.testValGeneric(myType,'type',type(controllers['cpu1']),type(controllers['cpu2']))
        self.printSeparator()
        
        #RaceManager
        raceManager = RaceManager(controllers,bgeCars,racingLineBezier)
        myType = type(raceManager)
        self.testValGeneric(myType,'creation',len(raceManager.bgeCars),3)
        self.testFunGeneric(myType,raceManager.raceRankingManager.getCrossedDistance,[bgeCar],0.0)
        self.testValGeneric(myType,'getRanking',len(raceManager.getRanking()),3)
        self.printSeparator()

        print('Test success rate: ' + str(self.test_success) + '/' + str(self.test_total))

        

