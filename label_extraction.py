import cv2
# import matplotlib as mlp
import numpy as np
import os

# 혹시 이미지 전처리 따로 쓸 일 있을까 봐..
# def preprocess(gray):
#     # Threshold
#     t1, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     ret, thresh = cv2.threshold(gray, t1, 255, cv2.THRESH_BINARY)

#     # Find Contour
#     img2 = gray.copy()
#     contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(img2, contours, -1, (255, 0, 0), 1)

#     return img2

# 이미지 gray-scale로 변환
img = cv2.imread("label17.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
draw = gray.copy()

# 이미지에서 라벨 영역 추출
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
gaussian = cv2.GaussianBlur(resize, (0, 0), 4)

# 폴더 안에 모든 이미지 가져오기
path = ["template/1/", "template/2/", "template/3/", "template/4/", "template/5/"]

# template 종류별로 서로 다른 폴더 생성했음. 종류별로 구분할 거임.
for p in path:
    symbol_list = os.listdir(p)
    symbol = [file for file in symbol_list if file.endswith((".png", ".jpg"))]
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
        target = cv2.resize(gaussian, (int(th*iw/ih), th))
        cv2.imshow("gray origin", target)

        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        match_val = max_val
        prob_ = (max_val, tmp_path)
        prob.append(prob_)

        bottom_right = (top_left[0] + tw, top_left[1] + th)
        cv2.rectangle(target, top_left, bottom_right, (0, 255, 0), 2)
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.imshow("result", target)

        print("max_val :", max_val, "/ top left :", top_left)
        # cv2.waitKey(0)

    # 가장 높은 확률 세 개 뽑기
    sort = []
    sort = tuple(sorted(prob, reverse=True))
    for i in range (1, 4):
        print(sort[i][1], ":", sort[i][0])
        img_prob = cv2.imread(sort[i][1])
        cv2.imshow("result by probability", img_prob)
        cv2.waitKey(0)

    cv2.waitKey(0)