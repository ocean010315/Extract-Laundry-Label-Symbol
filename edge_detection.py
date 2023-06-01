import cv2
import matplotlib as mlp
import numpy as np        

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
img = cv2.imread("label12.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
draw = gray.copy()

win_name = "gray origin"
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

template = cv2.imread("symbol3-2.png")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
cv2.imshow("template", template)

# template matching을 위해 원본 이미지의 높이와 template의 높이 맞추기
th, tw = template.shape[:2]
ih, iw = resize.shape[:2]
resize = cv2.resize(resize, (int(th*iw/ih), th))
cv2.imshow("gray origin", resize)

# 이미지 전처리
canny, thresh, img2, gaussian, highboost = preprocess(resize)
i = [canny, thresh, img2, gaussian, highboost]
name = ["canny", "thresh", "img2", "gaussian", "highboost"]

# 각각의 template matching 결과 출력
for n in range(0, 5):
    result = cv2.matchTemplate(i[n], template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    match_val = max_val

    bottom_right = (top_left[0] + tw, top_left[1] + th)
    cv2.rectangle(resize, top_left, bottom_right, (0, 255, 0), 2)
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.imshow("result", resize)

    print(name[n], ":", max_val)
    print("top left :", top_left)
    cv2.waitKey(0)

cv2.waitKey(0)