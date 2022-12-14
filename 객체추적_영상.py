# import necessary packages
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import serial
import math
from collections import deque

import time

COM='COM12'

dis_l=deque([])
tag=["bicycle","car","motorbike","bus","train","truck"]

KNOWN_DISTANCE = 30.0
# initialize the known object width, which in
# 
#  this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 400#13.0
# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
#image = cv2.resize(image, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
marker = 600#find_marker(image)
focalLength = (marker * KNOWN_DISTANCE) / KNOWN_WIDTH

ser=serial.Serial(port=COM,baudrate=9600,parity=serial.PARITY_NONE,\
                  stopbits=serial.STOPBITS_ONE,\
                  bytesize=serial.EIGHTBITS,\
                  )

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

def send_label(labels,box):
    global dis_l
    for i,label in enumerate(labels):
        #print(i,label)
        if label in tag:
            #print(box[i])
            dis_l.appendleft([distance_to_camera(KNOWN_WIDTH, focalLength, box[i][2])/12*30.48/2,time.time()])
            if len(dis_l)>=2 and (dis_l[0][1]-dis_l[1][1])!=0:
                #print("1_V :",dis_l[1][0])
                #print("2_V :",dis_l[0][0])
                vr=(dis_l[1][0]-dis_l[0][0])/(dis_l[0][1]-dis_l[1][1])
                #print(vr) # speed
                #A car is traveling at a speed of 2 m/s
                input_str="Car is driving at a speed of "+str(math.floor(vr))#label+" "
                input_str=input_str.encode('utf-8')
                print(input_str)
                ser.write(input_str)
            #print(distance_to_camera(KNOWN_WIDTH, focalLength, box[i][2])/12*30.48/2)
            #cv2.imwrite("save_img.jpg")

            #i,label=labels[0]
        #input_str=label+" "
        #input_str=input_str.encode('utf-8')
        #ser.write(input_str)



# open webcam (웹캠 열기)
webcam = cv2.VideoCapture(cv2.CAP_DSHOW+0)


def obt_dis(marker):
    #image = cv2.imread(imagePath)
    #image = cv2.resize(image, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
    #marker = find_marker(image) #((x,y),(length,width),degree)
    #print(marker)
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    return [inches/12]



if not webcam.isOpened():
    print("Could not open webcam")
    exit()
    

# loop through frames
while webcam.isOpened():
    # read frame from webcam 
    status, frame = webcam.read()

    #print(obt_dis(frame)*30.48)
    #print("###")

    if not status:
        #print("SDF")
        break

    # apply object detection (물체 검출)
    bbox, label, conf = cv.detect_common_objects(frame,model='yolov3')

    #print(bbox, label, conf)

    #if "person" in 

    # draw bounding box over detected objects (검출된 물체 가장자리에 바운딩 박스 그리기)
    out = draw_bbox(frame, bbox, label, conf, write_conf=True)

    send_label(label,bbox)
        #dis_l.pop(len(dis_l)-1)
    # display output
    cv2.imshow("Real-time object detection", out)

    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
# release resources
webcam.release()
cv2.destroyAllWindows() 