import cv2
# import matplotlib as mlp
import numpy as np
import os

# 이미지 전처리
def preprocess(gray):
    # Canny Edge Detection - thresh value를 지정해줘야 하는 번거로움
    canny = cv2.Canny(gray, 50, 200)
    # cv2.namedWindow("Canny Edge", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Canny Edge.jpg", canny)

    # Threshold
    t1, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret, thresh = cv2.threshold(gray, t1, 255, cv2.THRESH_BINARY)
    # cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Thresh.jpg", thresh)

    # Find Contour
    img2 = gray.copy()
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img2, contours, -1, (255, 0, 0), 1)
    # cv2.namedWindow("Contour", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Contour.jpg", img2)

    # Highboost Filtering
    gaussian = cv2.GaussianBlur(gray, (0, 0), 4)
    edge = cv2.subtract(gray, gaussian)
    highboost = cv2.add(gray, edge)
    # cv2.namedWindow("Highboost", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Highboost.jpg", highboost)

    # 또 뭐가 있을까

    return canny, thresh, img2, gaussian, highboost

# 이미지, template 불러와서 각각 gray scale로 변환
img = cv2.imread("label15.jpg")
# O: label1, label3, label5, label9, label11, label12 확인 / label3 처럼 표백 설명 여부 없을 때는??? / X: label2-2, label5-3, label11-1, label13-1/3
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
draw = gray.copy()

win_name = "gray origin"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
pts_cnt = 0
pts = np.zeros((4, 2), dtype=np.float32)
def onMouse(event, x, y, flags, parmas):
    global pts_cnt
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(draw, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow(win_name, draw)

        pts[pts_cnt] = [x, y]
        pts_cnt += 1
        if pts_cnt == 4:
            sm = pts.sum(axis=1)
            diff = np.diff(pts, axis=1)

            topLeft = pts[np.argmin(sm)]
            bottomRight = pts[np.argmax(sm)]
            topRight = pts[np.argmin(diff)]
            bottomLeft = pts[np.argmax(diff)]

            pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

            w1 = abs(bottomRight[0]-bottomLeft[0])
            w2 = abs(topRight[0] - topLeft[0])
            h1 = abs(topRight[1] - bottomRight[1])
            h2 = abs(topLeft[1] - bottomLeft[1])
            width = int(max([w1, w2]))
            height = int(max([h1, h2]))

            pts2 = np.float32([[0, 0], [width-1, 0], 
                                [width-1, height-1], [0, height-1]])
            
            mtrx = cv2.getPerspectiveTransform(pts1, pts2)
            res = cv2.warpPerspective(gray, mtrx, (width, height))

            cv2.namedWindow("scanned", cv2.WINDOW_NORMAL)
            cv2.imshow("scanned", res)
            cv2.imwrite("scanned.jpg", res)

            print("이미지 저장 완료")

cv2.imshow(win_name, gray)
cv2.setMouseCallback(win_name, onMouse)
cv2.waitKey(0)

resize = cv2.imread("scanned.jpg")
resize = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)

# 이미지 전처리
canny, thresh, img2, gaussian, highboost = preprocess(resize)
i = [canny, thresh, img2, gaussian, highboost]

# 폴더 안에 모든 이미지 가져오기
path = ["template/1/", "template/2/", "template/3/"]

# template 종류별로 서로 다른 폴더 생성
for p in path:
    symbol_list = os.listdir(p)
    symbol = [file for file in symbol_list if file.endswith((".png", ".jpg"))]
    # location = []
    prob = []

    # 폴더 내 각 template에 대하여 matching 결과 출력
    for image in symbol:
        tmp_path = os.path.join(p, image)
        tmp = cv2.imread(tmp_path)

        template = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        cv2.imshow("template", template)

        # template 이미지와 원본 이미지의 높이 맞추기
        th, tw = template.shape[:2]
        ih, iw = resize.shape[:2]
        resize = cv2.resize(gaussian, (int(th*iw/ih), th))
        cv2.imshow("gray origin", resize)

        result = cv2.matchTemplate(resize, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        match_val = max_val
        # location.append(top_left)
        prob.append(max_val)

        bottom_right = (top_left[0] + tw, top_left[1] + th)
        cv2.rectangle(resize, top_left, bottom_right, (0, 255, 0), 2)
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.imshow("result", resize)

        print("max_val :", max_val, "/ top left :", top_left)
        # cv2.waitKey(0)

    max_prob = max(prob)
    index2 = prob.index(max_prob)
    prob_path = os.path.join(p, symbol[index2])
    print(prob_path, ":", max_prob)
    img_prob = cv2.imread(prob_path)
    cv2.imshow("result by probablity", img_prob)

    cv2.waitKey(0)