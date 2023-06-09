import cv2
import numpy as np
import os
from PIL import Image, ImageFont, ImageDraw

# 템플릿 이미지에 대한 설명을 저장할 딕셔너리 생성
descriptions = {
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1.png"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1-1.jpg"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1-2.jpg"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1-3.jpg"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1-4.jpg"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1-5.jpg"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1-6.jpg"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/1-7.jpg"
    : "                                          [ 물세탁 방법 ]\n\n물의 온도 30도를 표준으로 하여 세탁기로 약하게 손세탁하세요.\n\t* 약한 손세탁에는 흔들어 빨기, 눌러 빨기, 주물러 빨기가 포함됩니다.\n세탁기 사용은 금지됩니다.\n세제 종류는 중성 세제를 사용하세요!",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/2.png"
    :"                                          [ 물세탁 방법 ]\n\n물세탁을 하지 말아주세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/2-1.jpg"
    :"                                          [ 물세탁 방법 ]\n\n물세탁을 하지 말아주세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/2-2.jpg"
    :"                                          [ 물세탁 방법 ]\n\n물세탁을 하지 말아주세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/2-3.jpg"
    :"                                          [ 물세탁 방법 ]\n\n물세탁을 하지 말아주세요!",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/3.png"
    : "                                          [ 물세탁 방법 ]\n\n세탁기 사용이 가능합니다.\n기호에 적혀 있는 온도가 최적의 세탁 온도입니다.\n* 약 30도 중성이라고 명시된 경우, 중성 세제를 사용하시고,\n 약한 손세탁도 가능합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/3-1.jpg"
    : "                                          [ 물세탁 방법 ]\n\n세탁기 사용이 가능합니다.\n기호에 적혀 있는 온도가 최적의 세탁 온도입니다.\n* 약 30도 중성이라고 명시된 경우, 중성 세제를 사용하시고,\n 약한 손세탁도 가능합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/3-2.png"
    : "                                          [ 물세탁 방법 ]\n\n세탁기 사용이 가능합니다.\n기호에 적혀 있는 온도가 최적의 세탁 온도입니다.\n* 약 30도 중성이라고 명시된 경우, 중성 세제를 사용하시고,\n 약한 손세탁도 가능합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/3-3.png"
    : "                                          [ 물세탁 방법 ]\n\n세탁기 사용이 가능합니다.\n기호에 적혀 있는 온도가 최적의 세탁 온도입니다.\n* 약 30도 중성이라고 명시된 경우, 중성 세제를 사용하시고,\n 약한 손세탁도 가능합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/3-4.png"
    : "                                          [ 물세탁 방법 ]\n\n세탁기 사용이 가능합니다.\n기호에 적혀 있는 온도가 최적의 세탁 온도입니다.\n* 약 30도 중성이라고 명시된 경우, 중성 세제를 사용하시고,\n 약한 손세탁도 가능합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/3-5.png"
    : "                                          [ 물세탁 방법 ]\n\n세탁기 사용이 가능합니다.\n기호에 적혀 있는 온도가 최적의 세탁 온도입니다.\n* 약 30도 중성이라고 명시된 경우, 중성 세제를 사용하시고,\n 약한 손세탁도 가능합니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/1.png"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n그 어떤 표백제 사용도 불가합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/1-1.jpg"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n그 어떤 표백제 사용도 불가합니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/2.png"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계 표백제 사용이 불가합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/2-1.jpg"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계 표백제 사용이 불가합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/2-2.jpg"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계 표백제 사용이 불가합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/2-3.jpg"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계 표백제 사용이 불가합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/3.png"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계, 산소계 표백제 모두 사용이 불가합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제\n\t* 산소계 표백제 : 과탄산소다 등 과탄산나트륨 성분의 일반 표백제",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/3-1.jpg"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계, 산소계 표백제 모두 사용이 불가합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제\n\t* 산소계 표백제 : 과탄산소다 등 과탄산나트륨 성분의 일반 표백제",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/4.PNG"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계 표백제 사용이 가능합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제\n\t* 염소계 표백제는 물과 희석해 단독으로 사용하세요.\n\t* 염소계 표백제는 신체에 닿지 않도록 주의하세요.\n\t* 염소계 표백제는 밀폐된 용기에 보관하지 마세요.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/5.PNG"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n산소계 표백제 사용이 가능합니다.\n\t* 산소계 표백제 : 과탄산소다 등 과탄산나트륨 성분의 일반 표백제",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/6.PNG"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n염소계, 산소계 표백제 모두 사용이 가능합니다.\n\t* 염소계 표백제 : 락스 등 치아염소산나트륨 성분의 표백제\n\t* 산소계 표백제 : 과탄산소다 등 과탄산나트륨 성분의 일반 표백제\n\t* 염소계 표백제는 물과 희석해 단독으로 사용하세요.\n\t* 염소계 표백제는 신체에 닿지 않도록 주의하세요.\n\t* 염소계 표백제는 밀폐된 용기에 보관하지 마세요.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/7.PNG"
    : "                                [ 산소 또는 염소 표백의 가부 ]\n\n산소계 표백제 사용이 불가합니다.\n\t* 산소계 표백제 : 과탄산소다 등 과탄산나트륨 성분의 일반 표백제",
            
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/1.png"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 가능합니다.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/1-1.png"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 가능합니다.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/1-2.jpg"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 가능합니다.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/1-3.png"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 가능합니다.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/1-4.jpg"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 가능합니다.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",

    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2.png"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-1.jpg"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-2.jpg"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-3.jpg"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-4.jpg"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-5.png"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-6.jpg"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-7.jpg"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/2-8.jpg"
    : "                                          [ 다림질 방법 ]\n\n헝겊을 덮고 다리미를 사용하세요.\n기호에 적혀 있는 온도가 가능한 다리미의 온도입니다.\n\t* 분류 : 180도~210도, 140도~160도, 80도~120도",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/3.png"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 불가합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/3-1.jpg"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 불가합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/3-2.png"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 불가합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/3-3.jpg"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 불가합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/3-4.jpg"
    : "                                          [ 다림질 방법 ]\n\n다리미 사용이 불가합니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/1.png"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있습니다.\n용체의 종류는 퍼클로로에틸렌 또는 석유계를 사용하십시오.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/1-1.jpg"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있습니다.\n용체의 종류는 퍼클로로에틸렌 또는 석유계를 사용하십시오.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/1-2.jpg"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있습니다.\n용체의 종류는 퍼클로로에틸렌 또는 석유계를 사용하십시오.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/1-3.jpg"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있습니다.\n용체의 종류는 퍼클로로에틸렌 또는 석유계를 사용하십시오.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/2.png"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있습니다.\n용체의 종류는 석유계로 제한됩니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/2-1.jpg"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있습니다.\n용체의 종류는 석유계로 제한됩니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/2-2.jpg"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있습니다.\n용체의 종류는 석유계로 제한됩니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/3.png"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝을 할 수 있지만, 셀프서비스는 불가합니다.\n전문점에 드라이클리닝을 맡기십시오.\n\t* 전문점이란 일반 가정에서 취급이 어려운 가죽, 모피 등의 제품을\n 취급하는 업소입니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/4.png"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝이 불가합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/4-1.jpg"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝이 불가합니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/4-2.jpg"
    : "                                         [ 드라이클리닝 ]\n\n드라이클리닝이 불가합니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/1.png"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 옷걸이에 걸어 건조시키세요!",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/2.png"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 옷걸이에 걸어 그늘에서 건조시키세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/2-1.jpg"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 옷걸이에 걸어 그늘에서 건조시키세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/2-2.jpg"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 옷걸이에 걸어 그늘에서 건조시키세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/2-3.jpg"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 옷걸이에 걸어 그늘에서 건조시키세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/2-4.jpg"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 옷걸이에 걸어 그늘에서 건조시키세요!",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/2-5.jpg"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 옷걸이에 걸어 그늘에서 건조시키세요!",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/3.png"
    : "                                        [ 일광 건조 방법 ]\n\n햇빛에서 뉘어서 건조시키세요!\n옷걸이에 걸 경우, 옷감의 변형이 생길 수 있습니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/4.png"
    : "                                        [ 일광 건조 방법 ]\n\n그늘에 뉘어서 건조시키세요!\n옷걸이에 걸 경우, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/4-1.jpg"
    : "                                        [ 일광 건조 방법 ]\n\n그늘에 뉘어서 건조시키세요!\n옷걸이에 걸 경우, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/4-2.jpg"
    : "                                        [ 일광 건조 방법 ]\n\n그늘에 뉘어서 건조시키세요!\n옷걸이에 걸 경우, 옷감의 변형이 생길 수 있습니다.",
        
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/1.png"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 가능합니다.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2.png"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-1.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-2.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-3.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-4.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-5.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-6.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-7.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-8.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-9.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/2-10.jpg"
    : "                                        [ 기계 건조 방법 ]\n\n세탁 후 건조할 때 기계 건조가 불가합니다.\n기계 건조 시, 옷감의 변형이 생길 수 있습니다.",
        
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/1.png"
    : "                                            [ 짜는 방법 ]\n\n손으로 짜는 경우에는 약하게 짜고,\n 원심 탈수기인 경우는 단시간에 짜도록 하세요.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/1-1.jpg"
    : "                                            [ 짜는 방법 ]\n\n손으로 짜는 경우에는 약하게 짜고,\n 원심 탈수기인 경우는 단시간에 짜도록 하세요.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/1-2.jpg"
    : "                                            [ 짜는 방법 ]\n\n손으로 짜는 경우에는 약하게 짜고,\n 원심 탈수기인 경우는 단시간에 짜도록 하세요.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/1-3.jpg"
    : "                                            [ 짜는 방법 ]\n\n손으로 짜는 경우에는 약하게 짜고,\n 원심 탈수기인 경우는 단시간에 짜도록 하세요.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/1-4.jpg"
    : "                                            [ 짜는 방법 ]\n\n손으로 짜는 경우에는 약하게 짜고,\n 원심 탈수기인 경우는 단시간에 짜도록 하세요.",
    
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/2.png"
    : "                                            [ 짜는 방법 ]\n\n짜지 마십시오.\n옷을 짤 시, 옷감의 변형이 생길 수 있습니다.",
    "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/2-1.jpg"
    : "                                            [ 짜는 방법 ]\n\n짜지 마십시오.\n옷을 짤 시, 옷감의 변형이 생길 수 있습니다."
}  

# 이미지 gray-scale로 변환
img = cv2.imread("C:\openSource\Extract-Laundry-Label-Symbol\osh\Image\CV2/tt.jpg")
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

def description(template, tmp_path):
    textImg = cv2.imread("C:/openSource/Extract-Laundry-Label-Symbol/osh/text.png", cv2.IMREAD_COLOR)
   
    # description image에 템플릿 이미지 출력
    desc_h, desc_w = textImg.shape[:2]
    template_rgb = cv2.cvtColor(template, cv2.COLOR_GRAY2RGB)
    template_h, template_w = template_rgb.shape[:2]
        
    # 같은 비율로 template image resize
    template_aspect_ratio = template_w / template_h
        
    if template_aspect_ratio > 1:
        new_template_w = int(120 * template_aspect_ratio)
        new_template_h = 120
    else:
        new_template_w = 120
        new_template_h = int(120 / template_aspect_ratio)
            
    resized_template = cv2.resize(template_rgb, (new_template_w, new_template_h))
    resized_h, resized_w = resized_template.shape[:2]
        
    x_offset = desc_w - resized_w
    y_offset = desc_h - resized_h
        
    # description image의 crop된 일부에 resized_template 합성
    crop = textImg[y_offset-70:desc_h-70, x_offset-50:desc_w-50]
    template_resized = cv2.resize(template_rgb, (crop.shape[1], crop.shape[0]))
    crop[:] = template_resized
        
    # 템플릿 이미지에 대한 설명 출력
    text_pillow = Image.fromarray(textImg)
    fontpath = "C:\\Users\\지은\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NanumSquareRoundEB.ttf"
    font = ImageFont.truetype(fontpath, 15)
        
    b, g, r = 0, 0, 0
    draw = ImageDraw.Draw(text_pillow, 'RGB')
        
    # 딕셔너리에서 template image별 설명을 불러와 출력
    description = descriptions.get(tmp_path)
    alert = "                세탁 기호는 한국산업표준에 의해 분류되었습니다."
    if description is not None:
        draw.text((50, 250), description, font=font, fill=(b,g,r))
        draw.text((50, 480), alert, font=font, fill=(b,g,r))
        
    cv2_image = np.array(text_pillow)
    cv2.imshow("description", cv2_image)          
    
cv2.imshow(win_name, gray)
cv2.setMouseCallback(win_name, onMouse)
cv2.waitKey(0)

resize = cv2.imread("scanned.jpg")
resize = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)

# 이미지 전처리
gaussian = cv2.GaussianBlur(resize, (0, 0), 4)

# 폴더 안에 모든 이미지 가져오기
path = ["C:/openSource/Extract-Laundry-Label-Symbol/osh/template/1/", "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/2/", "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/3/",
        "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/4/", "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/5/", "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/6/",
        "C:/openSource/Extract-Laundry-Label-Symbol/osh/template/7/"]

# template 종류별로 서로 다른 폴더 생성했음. 종류별로 구분
for p in path:
    symbol_list = os.listdir(p)
    symbol = [file for file in symbol_list if file.endswith((".png", ".jpg", ".PNG", ".JPG"))]
    prob = []

    # 폴더 내 각 template에 대하여 matching 결과 출력
    for image in symbol:
        tmp_path = os.path.join(p, image)
        tmp = cv2.imread(tmp_path)

        template = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)      
        
        description(template, tmp_path)
            
        # template 이미지와 원본 이미지의 높이 맞추기
        th, tw = template.shape[:2]
        ih, iw = resize.shape[:2]
        target = cv2.resize(gaussian, (int(th*iw/ih), th))

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
    
        # 터미널 창에서 확률 확인
        print("max_val :", max_val, "/ top left :", top_left)

# 가장 높은 확률로 매칭된 템플릿 세 개만 결과로 띄우기
sort = []
sort = tuple(sorted(prob, reverse=True))
for i in range (1, 4):
    print(sort[i][1], ":", sort[i][0])
    img_prob = cv2.imread(sort[i][1], cv2.IMREAD_GRAYSCALE)
    img_prob_path = sort[i][1]
    description(img_prob, img_prob_path)
    cv2.imshow("result by probability", img_prob)
    cv2.waitKey(0)