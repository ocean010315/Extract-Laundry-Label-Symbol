import requests
import uuid
import time
import json
import cv2
import numpy as np

api_url = 'https://muup4mej2d.apigw.ntruss.com/custom/v1/22881/056de427fd2cd96fe1db9786a4c1e8821b41eaf796f4402fd23a6a5a0b1c7702/general'
secret_key = 'RElSV0t4QnRoSHplYVZLUGZOT2xCeGdvWHB0VkZZd1Q='




def printText(text):
  for i in range (0 , len(text)):
    if "클리닝" in text[i]:
      print("본 제품은 드라이 클리닝이 가능 합니다.\n")
    
    if "산소" in text[i] :
      print("본 제품은 산소계 표백제로 표백 또는 표백 할 수 없습니다. 기호 내 x 여부를 확인하세요.\n")
  
    if "염소" in text[i] :
      print("본 제품은 염소계 표백제로 표백 또는 표백 할 수 없습니다. 기호 내 x 여부를 확인하세요.\n")
    
    if "손" in text[i] :
      print("본 제품은 손세탁만 가능하며 세탁기를 사용하는 세탁은 불가 합니다.\n")
      if("30") in text[i]:
        print("물 온도는 30도를 유지 하시고 중성세제를 사용하여 세탁하세요.\n")
    
    if "95" in text[i] :
      print("본 제품은 95도로 세탁 가능 합니다.\n 세제 종류의 제한이 없으며 세탁기 나 손세탁이 가능 합니다.\n")
    
    if "60" in text[i] :
      print("본 제품은 60도로 세탁 가능 합니다.\n 세제 종류의 제한이 없으며 세탁기 나 손세탁이 가능 합니다.\n")
    
    if "40" in text[i] :
      print("본 제품은 40도로 세탁 가능 합니다.\n 세제 종류의 제한이 없으며 세탁기 나 손세탁이 가능 합니다.\n")
    
    if "30" in text[i] :
      print("본 제품은 30도로 세탁이 가능 합니다.\n")
      if("중성") in text[i]:
        print("중성 세제를 사용하세요. \n")
    
    if "드라이" in text[i] :
      print("본 제품은 드라이 클리닝이 가능 및 불가능 합니다. 기호 내 x 기호를 확인 하세요. \n")
      if("석유")in text[i]:
        print("용제는 석유계를 사용하세요.")
    else:
      return    
    
    

image_file = 'C:/CV2/img/test-30.jpg' # 결과물 보여줄 크롭 이미지 읽어오는 위치 경로
output_file = 'C:/CV2/img/output.png'

# 이미지 파일 읽기
image = cv2.imread('C:/CV2/img/test-10.jpg', cv2.IMREAD_GRAYSCALE)

# cv::UMat 타입으로 이미지 변환
image_um = cv2.UMat(image)

# threshold 적용
_, thresholded_image = cv2.threshold(image_um, 127, 255, cv2.THRESH_BINARY)

# 결과 이미지 파일로 저장
cv2.imwrite('C:/CV2/img/test-30.jpg', thresholded_image.get())


request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

res = json.loads(response.text.encode('utf8'))
images = res.get("images")
text = []
for list in images:
  fields = list.get("fields")
  for i in fields:
    result = i.get("inferText")
    text.append(result)
    for i in range(0 , len(text)):
      print("추출된 기호는 : " + " " +  text[i])
printText(text)
    
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(res, outfile, indent=4, ensure_ascii=False)