from pdf2image import convert_from_path
import cv2
import preprocessing
import objectProcessing
import objectRecognition
import recognition_modules
import numpy as np
import functions as fs
import os
import pyxl_modules as pm
from openpyxl import Workbook

file_name = "canthave.png"
#
# pages = convert_from_path("./musicsheet/" + file_name)

workbook = Workbook()

# for i, page in enumerate(pages):
#     if i == 0: # 첫 페이지
sheet = pm.init_excel(workbook) # 액셀 파일 초기화


file = "./source/" + file_name
# page.save(file, "JPEG")

image = cv2.imread(file, 0)
img_gray = image
image = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
ret, img_gray = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
img_width, img_height = img_gray.shape[::-1]

masked_image = preprocessing.remove_noise(image)



noStaves_img, staves = preprocessing.rmStaves(masked_image)

normal_MS, staves = preprocessing.musicsheetNormalization(noStaves_img, staves, 150)
    # 4. 객체 검출 과정
normal_MS = fs.closing(normal_MS)
findObject, objects = objectProcessing.object_detection(normal_MS, staves)
#     #cv2.connectedComponentsWithStats(src, label, stats, centroids)
#     # src 입력 이미지, labels: 레이블 맵 행렬, stats: connected components를 감싸는 직사각형 및 픽셀 정보를 담고 있음 centroids: 각 connected components의 무게 중심 위치
#     # cv2.rectangle(img, pt1, pt2, color, thickness)
#     # img : 이미지 파일, pt1: 시작점 좌표, pt2: 종료점 좌표 color: 색상 , thickness : 선 두께
#
#     # 5. 객체 분석 과정
findObject, objects = objectRecognition.object_analysis(findObject, objects)
#
#     # 6. 인식 과정
findObject, key, beats, pitches = objectRecognition.recognition(findObject, staves, objects)
cv2.imwrite("./source/" + "검출" + ".png", findObject)
print("exit")

