import time

#convert a float to time as string
#ie: 75.06 seconds -> '01:15:06'
def convertFloatToTimeStr(f):
    str_millis = str(int(round(f - int(f),2) * 100))
    if len(str_millis) == 1:
        str_millis = '0' + str_millis
    return time.strftime('%M:%S',time.gmtime(f)) + ':' + str_millis

#return position as a nice string
def positionAsString(i):
    if i == 1:
        return '1st'
    elif i == 2:
        return '2nd'
    elif i == 3:
        return '3rd'
    else:
        return str(i) + 'th'
