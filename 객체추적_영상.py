# import necessary packages
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import serial
ser=serial.Serial(port='COM13',baudrate=9600,parity=serial.PARITY_NONE,\
                  stopbits=serial.STOPBITS_ONE,\
                  bytesize=serial.EIGHTBITS,\
                  )

def send_label(labels):
    for i,label in enumerate(labels):
        input_str=label+" "
        input_str=input_str.encode('utf-8')
        ser.write(input_str)

#def arduino_write(A):
#    input_str=A
#    input_str = input_str.encode('utf-8')
#    ser.write(input_str)


# open webcam (웹캠 열기)
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()
    

# loop through frames
while webcam.isOpened():

    # read frame from webcam 
    status, frame = webcam.read()

    if not status:
        #print("SDF")
        break

    # apply object detection (물체 검출)
    bbox, label, conf = cv.detect_common_objects(frame,model='yolov3')

    #print(bbox, label, conf)

    # draw bounding box over detected objects (검출된 물체 가장자리에 바운딩 박스 그리기)
    out = draw_bbox(frame, bbox, label, conf, write_conf=True)

    send_label(label)

    # display output
    cv2.imshow("Real-time object detection", out)

    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# release resources
webcam.release()
cv2.destroyAllWindows() 