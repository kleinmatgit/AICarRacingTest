import bpy
from mathutils import Vector
import math
from math import radians
import re
import shutil
import datetime
import os

#create a mesh
#rotation expressed in angle (ie: [90.0,180.0,250.0])
def createMesh(meshType='plane',name='plane_toto',
               location=[.0,.0,.0],
               scale=[1.0,1.0,1.0],
               rotation=[.0,.0,.0]):

    location_vector = Vector(location)
    
    if meshType=='plane':
        bpy.ops.mesh.primitive_plane_add(location=location_vector)
    elif meshType=='sphere':
        bpy.ops.mesh.primitive_uv_sphere_add(location=location_vector)
    ob = bpy.context.object
    ob.name = name
    ob.scale = Vector(scale)
    rotateMesh(ob,rotation)
    
#create a UV sphere
def createSphere(i,co,scale=0.1):
    if i<10:
        idx = '000' + str(i)
    elif i<100:
        idx = '00' + str(i)
    elif i<1000:
        idx = '0' + str(i)
    sphereName = 'sphereBezier_' + idx
    bpy.ops.mesh.primitive_uv_sphere_add(location=co)
    ob = bpy.context.object
    ob.name = sphereName
    ob.scale = (scale,scale,scale)
    
    #set object to Actor/Ghost/Invisible
    ob.game.use_actor = True
    ob.game.use_ghost = True
    ob.hide_render = False

#delete mesh which name start match pattern 'name'
def deleteMeshPattern(name):
    for ob in bpy.context.scene.objects:
        ob.select = ob.type == 'MESH' and ob.name.startswith(name)
    bpy.ops.object.delete()

#save sphere object position into a txt file
def saveSpherePositions(sphere_name_pattern,path,backup=False):

    #save a backup of existing path
    if backup and os.path.exists(path):
        shutil.copyfile(path,path
                        + '.'
                        + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                        + '.txt')
    
    idx_and_positions = []

    for ob in bpy.context.scene.objects:
        if ob.name.startswith(sphere_name_pattern):
            #get sphere idx
            idx = int(ob.name[-4:])
            idx_and_positions.append((idx,ob.location))

    #sort by idx asc
    idx_and_positions.sort()
    
    #keep only positions
    positions = []
    for t in idx_and_positions:
        positions.append(t[1])
    
    #write list to file
    with open(path, 'w') as file_to_write:
        for position in positions:
            file_to_write.write("{}\n".format('(' + str(position[0]) + ','
                                              + str(position[1]) + ','
                                              + str(position[2]) + ')'))

#read a list of track interface from file
def loadSpherePositionFromFile(file_full_path):
    positions = []
    f = open(file_full_path,'r')
    expr = r'\((\-*[0-9]+\.[0-9]+),(\-*[0-9]+\.[0-9]+),(\-*[0-9]+\.[0-9]+)\)'
    for line in f.readlines():
        matchObj = re.match(expr,line.strip())
        if matchObj:
            positions.append([float(matchObj.group(1)),
                              float(matchObj.group(2)),
                              float(matchObj.group(3))])
    f.close()
    return positions

def createSpheresFromFile(file_full_path):
    positions = loadSpherePositionFromFile(file_full_path)
    

#rotate a mesh object
def rotateMesh(ob,rotation):
##    rot_factor = math.pi/180
##    ob.rotation_euler = (rotation[0]*rot_factor,
##                         rotation[1]*rot_factor,
##                         rotation[2]*rot_factor)
    ob.rotation_euler = (radians(rotation[0]),
                         radians(rotation[1]),
                         radians(rotation[2]))

#return normal vector of plane
def getPlaneNormal(plane):
    return plane.matrix_world * plane.data.polygons[0].normal - plane.location

#return index as a string    
def getIdxAsString(idx,length=4):
    s_idx = ''
    for i in range(0,length - len(str(idx))):
        s_idx += '0'
    s_idx += str(idx)
    return s_idx

#return index as a string    
def getIdxAsStringOld(idx):
    if idx<10:
        return '000' + str(idx)
    elif idx<100:
        return '00' + str(idx)
    elif idx<1000:
        return '0' + str(idx)
    

