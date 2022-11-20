import cv2
import numpy as np

# 초기값 설정

# 객체 선택시 포함될 영역에 대한 값
col, width, row, height = -1,-1,-1,-1

# 비디오 영상이 출력되는 이미지
frame = None

# 원본이미지
frame2 = None

# 객체영역 선택 활성화 변수
inputmode = False

# 그리기 활성화
rectangle = False

# 선택영역
trackWindow = None

# 잘린 이미지영역값
roi_hist = None

def onMouse(event, x, y, flags, param):
    global col, width, row, height, frame, frame2, inputmode
    global rectangle, roi_hist, trackWindow

    # 객체영역을 설정할 때, 'i' 키보드를 누르면 활성화됨 inputmode
    if inputmode:

        # 마우스클릭 이벤트
        if event == cv2.EVENT_LBUTTONDOWN:
            # 그리기 활성화
            rectangle = True
            col, row = x,y

        # 마우스 이동시 ( 클릭된 상태 )
        elif event == cv2.EVENT_MOUSEMOVE:

            if rectangle:
                # 깔끔한 새 이미지 출력
                frame = frame2.copy()
                # 마우스 이동경로에 맞게 초록색 사각형범위 생성
                cv2.rectangle(frame,(col, row), (x,y),(0,255,0),2)
                cv2.imshow('frame',frame)

        # 마우스 클릭 해제시
        elif event == cv2.EVENT_LBUTTONUP:
            # 객체영역선택 비활성화
            inputmode = False

            # 그리기 비활성화
            rectangle = False

            # 선택된 영역에 대한 표시 ( 초록 사각형 )
            cv2.rectangle(frame,(col,row),(x,y),(0,255,0),2)

            # 높이와 폭을 영역의 크기만큼 지정 abs() 함수는 절대값 반환
            height, width = abs(row-y),abs(col-x)

            # 추적 영역을 설정함
            trackWindow = (col, row, width, height)

            # 선택된 영역 분할
            roi = frame[row:row+height, col:col+width]

            # 잘라낸 이미지에 대한 HSV 색공간 변환
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # 2D이미지 히스토그램을 추출, 여기선 Hue 색상값만 사용 0~179
            roi_hist = cv2.calcHist([roi],[0], None, [180],[0,180])

            # 히스토그램을 정규화 시킴 0~179의 값을 0~255 의 값으로
            cv2.normalize(roi_hist, roi_hist, 0 , 255, cv2.NORM_MINMAX)
    return

def CamShift():
    global frame, frame2, inputmode, trackWindow, roi_hist

    # 영상호출 단계
    try:
        cap = cv2.VideoCapture(cv2.CAP_DSHOW+0)

    # 오류내용 출력
    except Exception as e:
        print(e)
        return

    # frame 값에 현재 출력중인 이미지 삽입
    ret, frame = cap.read()
    cv2.namedWindow('frame')
    # frame, frame2 에 대한 마우스 액션에 대한 작업
    cv2.setMouseCallback('frame',onMouse,param=(frame,frame2))

    # meanShift 알고리즘 동작에 대한 정보
    # meanshift의 반복횟수를 10회 또는 현재 객체에 대한 무게중심의 위치까지 이동할 때 까지
    # 알고리즘을 구동
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


    while True:
        ret, frame = cap.read()
        # 영상 출력이 제대로 되지않을 경우 해당 프로그램 종료
        if not ret:
            break

        # 객체선택을 하지 않았을경우
        if trackWindow is not None:
            # 현재 출력화면에 대한 HSV 색공간 변환
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            # 히스토그램의 역 투영을 계산
            # HSV 색공간 변환이 된 이미지에서 객체가 포함된 영역을 찾아줌.
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            cv2.imshow('dst',dst)
            # (역투영이미지, 초기검색창, 알고리즘 기준)
            ret, trackWindow = cv2.CamShift(dst, trackWindow, termination)
            # box의 포인트좌표를 배열로 정리
            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            # 배열로된 네꼭지점을 선으로 이음 True 값은 닫힘여부
            cv2.polylines(frame,[pts],True,(0,255,0),2)

        cv2.imshow('frame',frame)

        # esc 클릭시 프로그램 창종료
        k = cv2.waitKey(1)
        if k == 27:
            break

        # 'i' 버튼 클릭시 객체선택 활성화
        if k == ord('i'):
            print("select Area for CamShift and Enter a Key")
            inputmode = True
            # 기존에 선택되었던 객체영역에 대한 값 초기화
            frame2 = frame.copy()

            while inputmode:
                cv2.imshow('frame',frame)
                cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()

CamShift()