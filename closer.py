import cv2
import numpy as np
import time

# Yolo 로드
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()

output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

#영상 촬영
capture = cv2.VideoCapture(cv2.CAP_DSHOW+0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
fps = capture.get(cv2.CAP_PROP_FPS)
prev_time=0
if fps==0.0:
    fps=10.0
print(fps)
while(capture.isOpened()):
    k = cv2.waitKey(1)
    if k == ord('i'):
        cv2.imwrite("test.jpg", frame) 
        break
    ret, frame = capture.read()
    current_time = time.time() - prev_time
    if (ret is True) and (current_time > 1./ fps):
        prev_time = time.time()

        img = frame
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416,416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # 정보를 화면에 표시
        class_ids = []
        confidences = []
        boxes = []
        # 3개의 array 에서 경우별 각 항목에 대해 확률이 나타남, 처음 4개는 왼쪽 위 좌표, 길이

        for out in outs:
            for detection in out:
                #print("###")
                scores = detection[5:]
                #print(len(scores))
                class_id = np.argmax(scores)
                if classes[class_id]=="cell phone":
                    scores[class_id]=0
                    class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # 좌표
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    #print([x,y,w,h],classes[class_id])

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        
        cv2.imshow("VideoFrame", frame)

capture.release()
cv2.destroyAllWindows()
