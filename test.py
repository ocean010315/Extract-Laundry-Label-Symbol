import cv2
import numpy as np

win_name = "image"
cv2.namedWindow(win_name, flags=cv2.WINDOW_KEEPRATIO)
img = cv2.imread("example.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rows, cols = img.shape[:2] # height, weight 값 구하기
draw = img.copy()
pts_cnt = 0
pts = np.zeros((4, 2), dtype=np.float32)

# ret,img_bin = cv2.threshold(img, 116, 255, cv2.THRESH_BINARY) # 임계값 175: thresh_binary, thresh_tozero. 130-170까지

# # opening = erosion -> dilation
# k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# erosion = cv2.erode(img_bin, k)
# dilation = cv2.dilate(erosion, k)

# # closing = dilation -> erosion
# d2 = cv2.dilate(dilation, k)
# e2 = cv2.erode(d2, k)

def onMouse(event, x, y, flags, params):
    global pts_cnt
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(draw, (x, y), 10, (0, 255, 0), -1) # 좌표에 초록색 동그라미
        cv2.imshow(win_name, draw)

        pts[pts_cnt] = [x, y]
        pts_cnt += 1
        if pts_cnt == 4:
            sm = pts.sum(axis=1)                 # 4쌍의 좌표 각각 x+y 계산
            diff = np.diff(pts, axis=1)       # 4쌍의 좌표 각각 x-y 계산

            topLeft = pts[np.argmin(sm)]         # x+y가 가장 작은 값이 좌상단 좌표
            bottomRight = pts[np.argmax(sm)]     # x+y가 가장 큰 값이 우하단 좌표
            topRight = pts[np.argmin(diff)]     # x-y가 가장 작은 것이 우상단 좌표
            bottomLeft = pts[np.argmax(diff)]   # x-y가 가장 큰 값이 좌하단 좌표

            # 변환 전 4개 좌표 
            pts1 = np.float32([topLeft, topRight, bottomRight , bottomLeft])

            # 변환 후 영상에 사용할 서류의 폭과 높이 계산
            w1 = abs(bottomRight[0] - bottomLeft[0])    # 상단 좌우 좌표간의 거리
            w2 = abs(topRight[0] - topLeft[0])          # 하당 좌우 좌표간의 거리
            h1 = abs(topRight[1] - bottomRight[1])      # 우측 상하 좌표간의 거리
            h2 = abs(topLeft[1] - bottomLeft[1])        # 좌측 상하 좌표간의 거리
            width = int(max([w1, w2]))                  # 두 좌우 거리간의 최대값이 서류의 폭
            height = int(max([h1, h2]))                 # 두 상하 거리간의 최대값이 서류의 높이
            
            # 변환 후 4개 좌표
            pts2 = np.float32([[0, 0], [width-1, 0], 
                                [width-1, height-1], [0, height-1]])

            # 변환 행렬 계산 
            mtrx = cv2.getPerspectiveTransform(pts1, pts2)
            # 원근 변환 적용
            result = cv2.warpPerspective(img, mtrx, (width, height))

            otsu_threshold, image_result = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            print(otsu_threshold)
            th, result = cv2.threshold(result, otsu_threshold, 255, cv2.THRESH_BINARY)

            cv2.namedWindow("scanned", cv2.WINDOW_NORMAL)
            cv2.imshow("scanned", result)



cv2.imshow(win_name, img)
cv2.setMouseCallback(win_name, onMouse) # 마우스 콜백 함수를 gui 윈도우에 등록
cv2.waitKey(0)
cv2.destroyAllWindows()