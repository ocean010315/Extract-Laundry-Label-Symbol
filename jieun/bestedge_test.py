import cv2
import numpy as np
import matplotlib.pylab as plt

# 이미지 전처리
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
    gaussian = cv2.GaussianBlur(gray, (1, 1), sigmaX=0, sigmaY=0)
    return gaussian

def preprocess_hpf(gray):
    gaussian = cv2.GaussianBlur(gray, (1, 1), sigmaX=0, sigmaY=0)
    edge = cv2.subtract(gray, gaussian)
    highboost = cv2.add(gray, edge)
    # cv2.namedWindow("Highboost", cv2.WINDOW_NORMAL)
    # cv2.imwrite("Highboost.jpg", highboost)
    return highboost

def preprocess_thresCanny(gray):
    #가우시안 블러
    thresCanny = cv2.GaussianBlur(gray, (1, 1), sigmaX=0, sigmaY=0)
    
    # 이미지 이진화(배경 흰색, 물체 검은색)
    t1, thresh = cv2.threshold(thresCanny, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret, thresh = cv2.threshold(thresCanny, t1, 255, cv2.THRESH_BINARY_INV)
    
    return thresCanny
   

# 이미지 불러오기
image = cv2.imread("CropImg/croplabel12(1).jpg", cv2.IMREAD_GRAYSCALE)
canny = preprocess_canny(image)
thresh = preprocess_thresh(image)
contour = preprocess_contour(image)
gaussian = preprocess_gaussian(image)
highboost = preprocess_hpf(image)
threshCanny = preprocess_thresCanny(image)

# 전처리된 이미지 출력
cv2.imshow("canny", canny)
cv2.imshow("thresh", thresh)
cv2.imshow("contour", contour)
cv2.imshow("gaussian", gaussian)
cv2.imshow("highboost", highboost)
cv2.imshow("thresCanny", threshCanny)
cv2.waitKey(0)

# 1. 케어라벨 기호 5종류로 전처리
# 2-1. 해당 케어라벨 기호에 해당하는 template 불러와서 전처리한 케어라벨과 유사도 검사
# 2-2. 템플릿 불러와서 매칭까지 했을 때의 케어라벨-템플릿 유사도 검사
# 3. 기호 5종에 대해 비교, 제일 높은 유사도 나온 걸로 선택

# 유사도 검사
template = cv2.imread("Templatete/symbol2-1.png", cv2.IMREAD_GRAYSCALE)

# 각 이미지와 템플릿 이미지의 유사도 계산 - Comparing histogram
def calculate_similarity(template, image):
    # 히스토그램 계산
    hist_template = cv2.calcHist([template], [0], None, [256], [0, 256])
    hist_image = cv2.calcHist([image], [0], None, [256], [0, 256])

    # 히스토그램 정규화
    cv2.normalize(hist_template, hist_template, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist_image, hist_image, 0, 1, cv2.NORM_MINMAX)

    # 히스토그램 유사도 계산
    similarity = cv2.compareHist(hist_template, hist_image, cv2.HISTCMP_CORREL)
    return similarity

canny_similarity = calculate_similarity(template, canny)
thresh_similarity = calculate_similarity(template, thresh)
contour_similarity = calculate_similarity(template, contour)
gaussian_similarity = calculate_similarity(template, gaussian)
highboost_similarity = calculate_similarity(template, highboost)
threshCanny_similarity = calculate_similarity(template, threshCanny)

print("histogram")
print(canny_similarity)
print(thresh_similarity)
print(contour_similarity)
print(gaussian_similarity)
print(highboost_similarity)
print(threshCanny_similarity)

# 각 이미지와 템플릿 이미지의 유사도 계산 - Template matching
def calculate_similarity_2(template, image):
    template = template.astype(np.uint8)
    image = image.astype(np.uint8)
    # 템플릿 매칭 수행
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, similarity, _, _ = cv2.minMaxLoc(result)
    return similarity

canny_similarity_2 = calculate_similarity_2(template, canny)
thresh_similarity_2 = calculate_similarity_2(template, thresh)
contour_similarity_2 = calculate_similarity_2(template, contour)
gaussian_similarity_2 = calculate_similarity_2(template, gaussian)
highboost_similarity_2 = calculate_similarity_2(template, highboost)
threshCanny_similarity_2 = calculate_similarity(template, threshCanny)

print("template matching")
print(canny_similarity_2)
print(thresh_similarity_2)
print(contour_similarity_2)
print(gaussian_similarity_2)
print(highboost_similarity_2)
print(threshCanny_similarity_2)

# 각 이미지와 템플릿 이미지의 유사도 계산 - Feature matching
def calculate_similarity_3(template, image):
    # 특징 매칭을 위한 ORB 검출기 생성
    orb = cv2.ORB_create()

    # 특징점과 디스크립터 계산
    keypoints_template, descriptors_template = orb.detectAndCompute(template, None)
    keypoints_image, descriptors_image = orb.detectAndCompute(image, None)

    # 특징 매칭을 위한 BFMatcher 생성
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 특징 매칭 수행
    matches = matcher.match(descriptors_template, descriptors_image)

    # 매칭 결과 정렬
    matches = sorted(matches, key=lambda x: x.distance)

    # 상위 N개 매칭 결과 선택
    top_matches = matches[:5]

    # 매칭 결과 유사도 계산
    similarity = sum([match.distance for match in top_matches]) / len(top_matches)

    return similarity

canny_similarity_3 = calculate_similarity_3(template, canny)
thresh_similarity_3 = calculate_similarity_3(template, thresh)
contour_similarity_3 = calculate_similarity_3(template, contour)
gaussian_similarity_3 = calculate_similarity_3(template, gaussian)
highboost_similarity_3 = calculate_similarity_3(template, highboost)
threshCanny_similarity_3 = calculate_similarity(template, threshCanny)

print("feature matching")
print(canny_similarity_3)
print(thresh_similarity_3)
print(contour_similarity_3)
print(gaussian_similarity_3)
print(highboost_similarity_3)
print(threshCanny_similarity_3)

# python3 bestedge_test.py