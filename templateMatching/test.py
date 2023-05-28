import cv2
import matplotlib as plt
import numpy as np


img = cv2.imread('C:/CV2/tt.jpg')

x,y,w,h = cv2.selectROI('img', img, False)
if w and h:
    roi = img[y:y+h, x:x+w]
    cv2.imshow('cropped', roi)                   # ROI 지정 영역을 새창으로 표시
    cv2.moveWindow('cropped', 600, 600)              # 새창을 화면 측 상단으로 이동
    cv2.imwrite('C:/CV2/img/cropped2.jpg',roi)  # 해당 위치의 폴더에 crop된 파일 저장


img2 = cv2.imread('C:/CV2/img/cropped2.jpg',cv2.IMREAD_GRAYSCALE)
template = cv2.imread('C:/CV2/img/6.jpg',cv2.IMREAD_GRAYSCALE)


th, tw = template.shape[:2]
cv2.imshow('template', template)

# 3가지 매칭 메서드 순회
methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', \
                                     'cv2.TM_SQDIFF_NORMED']
for i, method_name in enumerate(methods):
    img_draw = img2.copy()
    method = eval(method_name)
    # 템플릿 매칭   ---①
    res = cv2.matchTemplate(img2, template, method)
    # 최솟값, 최댓값과 그 좌표 구하기 ---②
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(method_name, min_val, max_val, min_loc, max_loc)

    # TM_SQDIFF의 경우 최솟값이 좋은 매칭, 나머지는 그 반대 ---③
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        match_val = min_val
    else:
        top_left = max_loc
        match_val = max_val
    # 매칭 좌표 구해서 사각형 표시   ---④      
    bottom_right = (top_left[0] + tw, top_left[1] + th)
    cv2.rectangle(img_draw, top_left, bottom_right, (0,255,0),2)
    # 매칭 포인트 표시 ---⑤
    cv2.putText(img_draw, str(match_val), top_left, \
                cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0), 1, cv2.LINE_AA)
    cv2.imshow(method_name, img_draw)
    
cv2.waitKey(50000)
cv2.destroyAllWindows()    


# convex hull
# dst = roi.copy()


# gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
# ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

# for i in contours:
#     hull = cv2.convexHull(i, clockwise=True)
#     cv2.drawContours(dst, [hull], 0, (0, 0, 255), 2)

# cv2.imshow("convex hull", dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()