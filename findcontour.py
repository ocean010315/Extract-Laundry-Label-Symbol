import cv2
import easy_ocr
import numpy as np

label = cv2.imread('label/label1.png')
label_gray = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)

template = cv2.imread('logo/tricoDryW.png')
# template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

cv2.imshow('label', label)
cv2.imshow('template', template)

_, label_threshold = cv2.threshold(label_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# label contour
contours, _ = cv2.findContours(label_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
coutour_image = label.copy()

template_contour, hierarchy = cv2.findContours(template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
template_contour = max(template_contour, key=cv2.contourArea)

cv2.drawContours(coutour_image, contours, -1, (0,255,0), 2)

cv2.imshow('Contours', coutour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 입력 이미지에서 세탁 기호 윤곽선 추출
# _, binary_image = cv2.threshold(label_gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(label_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 세탁 기호 유사도 비교
for contour in contours:
    # 세탁 기호 윤곽선과 템플릿 윤곽선의 매칭 점수 계산
    similarity_score = cv2.matchShapes(template_contour, contour, cv2.CONTOURS_MATCH_I1, 0)

    # 유사도 점수가 일정 기준 이상인 경우 해당 윤곽선에 빨간 박스 표시
    if similarity_score < 0.1:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(label, (x, y), (x + w, y + h), (0, 0, 255), 2)

# 물세탁 기호 검사
# 산소, 염소 표백부호 검사
# 다림질 부호 검사
# 드라이클리닝 부호 검사
# 건조 부호 검사

cv2.imshow('result', label)
cv2.waitKey(0)
cv2.destroyAllWindows()