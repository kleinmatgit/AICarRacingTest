import math
from mathutils import Vector
  
#project point P orthographically on [AB]
#projected point is H
def projectOrth(p,a,b):
    
    #compute unit vector V from points A and B
    v = (b-a)
    v.normalize()
    
    #compute BH
    bh = (p.x-a.x)*v.x + (p.y-a.y)*v.y + (p.z-a.z)*v.z
    
    #guess H(x,y,z)
    return Vector([a.x+bh*v.x,
                   a.y+bh*v.y,
                   a.z+bh*v.z])

#vector dot product
def dotProduct(v1,v2):
    return sum(p*q for p,q in zip(v1,v2))

#linear interpolation
#return y for (x,y) interpolated betwen (x0,y0) and (x1,y1)
def linearInterpolation(x,x0,y0,x1,y1):
    return y0+(y1-y0)*(x-x0)/(x1-x0)

#take 2 points (2D) A & B, a distance
#(supposed to be inferior to dist between A and B)
#and return new point on the line projected from A towards B at this distance
def projectDistBetween2Points(xa,ya,xb,yb,dist):

    #distance between 2 points
    dist_a_b = math.sqrt(math.pow(ya - yb,2) + math.pow(xa - xb,2))
    ratio = dist/dist_a_b
    x = (1-ratio) * xa + ratio * xb
    y = (1-ratio) * ya + ratio * yb
    return (x,y)

#return abs value of angle between 2 vectors
#in XYZ Euler referenciel
def angleFormated(v1,v2):
    v1 = vec2D(v1)
    v2 = vec2D(v2)
    return abs(v1.angle_signed(v2,None) * 180/math.pi)

#convert a 3D vector to 2D vector
def vec2D(v):
    return Vector([v[0],v[1]])

#test 2 vectors are roughly equal
def roughlyEqual(v1,v2):
    return(round(v1.x - v2.x,1)==0 and
           round(v1.y - v2.y,1)==0 and
           round(v1.z - v2.z,1)==0)
