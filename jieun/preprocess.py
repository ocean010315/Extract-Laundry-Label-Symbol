import cv2
import numpy as np
import os

def preprocess_canny(gray):
    # Canny Edge Detection - thresh value를 지정해줘야 하는 번거로움
    canny = cv2.Canny(gray, 50, 200)
    # cv2.namedWindow("Canny Edge", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Canny Edge.jpg", canny)
    return canny

def preprocess_thresh(gray):
    # Threshold
    t1, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret, thresh = cv2.threshold(gray, t1, 255, cv2.THRESH_BINARY)
    # cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Thresh.jpg", thresh)
    return thresh

def preprocess_contour(gray):
    # Find Contour
    img2 = gray.copy()
    t1, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret, thresh = cv2.threshold(gray, t1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img2, contours, -1, (255, 0, 0), 1)
    # cv2.namedWindow("Contour", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Contour.jpg", img2)
    return img2

def preprocess_gaussian(gray):
    # Highboost Filtering
    gaussian = cv2.GaussianBlur(gray, (0, 0), 4)
    return gaussian

def preprocess_hpf(gray):
    gaussian = cv2.GaussianBlur(gray, (0, 0), 4)
    edge = cv2.subtract(gray, gaussian)
    highboost = cv2.add(gray, edge)
    # cv2.namedWindow("Highboost", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Highboost.jpg", highboost)
    return highboost

# 이미지, template 불러와서 각각 gray scale로 변환
img = cv2.imread("CropImg/croplabel1(1).jpg", cv2.IMREAD_GRAYSCALE)
resize = cv2.resize(img, dsize=(0,0), fx=3.0, fy=3.0)
# 이미지 전처리
canny = preprocess_canny(resize)
thresh = preprocess_thresh(resize)
img2 = preprocess_contour(resize)
gaussian = preprocess_gaussian(resize)
highboost = preprocess_hpf(resize)
i = (canny, thresh, img2, gaussian, highboost)

# 폴더 안에 모든 이미지 가져오기
path = ["template/1/", "template/2/", "template/3/", 
        "template/4/", "template/5/", "template/6/", "template/7/"]

# template 종류별로 서로 다른 폴더 생성
for p in path:
    symbol_list = os.listdir(p)
    symbol = [file for file in symbol_list if file.endswith((".png", ".jpg", ".PNG", ".JPG"))]
    # location = []
    prob = []

    # 폴더 내 각 template에 대하여 matching 결과 출력
    for image in symbol:
        tmp_path = os.path.join(p, image)
        tmp = cv2.imread(tmp_path)

        template = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)

        # template 이미지와 원본 이미지의 높이 맞추기
        th, tw = template.shape[:2]
        ih, iw = resize.shape[:2]
        resize = cv2.resize(gaussian, (int(th*iw/ih), th))

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