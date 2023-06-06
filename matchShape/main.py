import cv2
import numpy as np
import os
import glob

# 마우스 이벤트 처리를 위한 함수
roi = []
def roi_selection(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(roi) < 4: # 4개의 점만 선택하도록 제한
            roi.append((x, y))
            cv2.circle(label_img, (x,y), 5, (255, 0, 0), -1) # 좌표 파란색으로 출력

cv2.namedWindow('image')
cv2.setMouseCallback('image', roi_selection)

# 이미지를 불러오고, 그레이스케일 변환 후 블러 처리
label_path = 'label/label1.png'
label_img = cv2.imread(label_path)
gray_img = cv2.cvtColor(label_img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_img, (5,5), 0)

while True:
    cv2.imshow('image', label_img)
    if len(roi) == 4:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

roi = np.array(roi)
s = roi.sum(axis=1)
roi_image = blur_img[np.min(roi[:,1]):np.max(roi[:,1]), np.min(roi[:,0]):np.max(roi[:,0])]

# label 이미지의 윤곽선 추출
roi_edges = cv2.Canny(roi_image, 30, 150)

# template 폴더에서 모든 이미지를 불러옴
template_dir = ['template/1/', 'template/2/', 'template/3/', 'template/4/', 'template/5/', 'template/6/', 'template/7/' ]
templates = []

for dir in template_dir:
    for file in glob.glob(dir + '*.*'):
        if file.endswith('.png') or file.endswith('.jpg'):
            temp_img = cv2.imread(file)
            gray_temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
            blur_temp_img = cv2.GaussianBlur(gray_temp_img, (5,5), 0)
            templates.append(blur_temp_img)

# template 이미지들의 윤곽선 추출
template_edges = [cv2.Canny(template, 30, 150) for template in templates]

# 윤곽선 비교를 통해 가장 비슷한 template 이미지를 찾음
matches = [cv2.matchShapes(roi_edges, template_edge, cv2.CONTOURS_MATCH_I2, 0) for template_edge in template_edges]
# 가장 비슷한 template 3개의 index (오름차순 3개)
top3_index = np.argsort(matches)[:3]

# 가장 유사한 template 이미지 3개 출력
for i, index in enumerate(top3_index):
    cv2.imshow('Matched Template {}'.format(i+1), templates[index])

cv2.waitKey(0)
cv2.destroyAllWindows()