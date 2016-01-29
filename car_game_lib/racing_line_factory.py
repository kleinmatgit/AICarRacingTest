from mathutils.geometry import interpolate_bezier
from car_game_lib.racing_line import RacingLine
from car_game_lib import mesh_handler as mh
from mathutils import Vector

#########################################
## Builder for RacingLine object 
#########################################

class RacingLineFactory():

    file_pattern = '_racing_line_coords.txt'
    
    #create a racing line from spline bezier curve object on the scene
    def createFromSpline(self,spline,scale,divisor=1):
        raw_points = self.getSplinePoints(spline,scale)
        reduced_points = self.reducePointsList(raw_points,divisor)
        points,length = self.getSplinePointsWithDistance(reduced_points)
        return RacingLine(points,length)

    #create a racing line from list of coordinates in a file
    def createFromFile(self,path):
        positions = mh.loadSpherePositionFromFile(path)
        positions = self.convertPositionListToVector(positions)
        points,length = self.getSplinePointsWithDistance(positions)
        return RacingLine(points,length)

    #create racing lines dictionary from list of racing line file prefix
    def createFromList(self,path,items):
        racingLines = {}
        for item in items:
            racingLines[item] = self.createFromFile(path + item + self.file_pattern)
        return racingLines
    
    #get points along bezier curve given its spline
    def getSplinePoints(self,spline,scale):
        
        knots = spline.bezier_points
        
        if len(knots) < 2:
            return
     
        # verts per segment
        r = spline.resolution_u + 1
        
        # segments in spline
        segments = len(knots)
        
        if not spline.use_cyclic_u:
            segments -= 1
        
        master_point_list = []
        for i in range(segments):
            inext = (i + 1) % len(knots)
     
            knot1 = knots[i].co
            handle1 = knots[i].handle_right
            handle2 = knots[inext].handle_left
            knot2 = knots[inext].co
            
            bezier = knot1, handle1, handle2, knot2, r
            points = interpolate_bezier(*bezier)
            master_point_list.extend(points)
     
        #scaling
        for i in range(len(master_point_list)):
            p = master_point_list[i]
            p.x *= scale
            p.y *= scale
            p.z *= scale
            master_point_list[i]=p
        
        # some clean up to remove consecutive doubles, this could be smarter...
        old = master_point_list
        good = [v for i, v in enumerate(old[:-1]) if not old[i] == old[i+1]]
        good.append(old[-1])

        #remove points too close to each other (distance<treshold)
        i = 0
        while i < len(good):
            if i==len(good)-1:
                j = 0
            else:
                j = i+1
            if (good[j]-good[i]).length<0.1:
                del good[j]
            else:
                i += 1
        
        #remove last index if equal to first one
        if good[0]==good[len(good)-1]:
            good = good[:len(good)-1]
        return good
    

    #decorate list of points describing a spline
    #with distance with previous point
    #also return total length of the spline
    def getSplinePointsWithDistance(self,points):

        pointsDistance = []
        
        #first point with index=0
        pointsDistance.append((points[0],(points[0]-points[-1]).length,0.0))

        #rest of the points
        dist_to_start = 0.0
        for i in range(1,len(points)):
            dist_to_previous = (points[i]-points[i-1]).length
            dist_to_start += dist_to_previous
            pointsDistance.append((points[i],dist_to_previous,dist_to_start))

        #get length
        length = dist_to_start + pointsDistance[0][1]
        return pointsDistance,length
    
    #blender bezier curves have too many points
    #it causes performance issue when projectin AI guide on the spline
    #this method helps to reduce nbr of points
    def reducePointsList(self,points,divisor):
        new_list = []
        for i in range(0,len(points)):
            if i%divisor == 0:
                new_list.append(points[i])
        return new_list

    #take a list of positions as list of [x,y,z]
    #and convert it to list of positions as Vector([x,y,z])
    def convertPositionListToVector(self,positions):
        vec_positions = []
        for position in positions:
            vec = Vector(position)
            vec_positions.append(vec)
        return vec_positions
    
