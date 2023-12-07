## 얼굴 영역 검출
import numpy as np
import cv2
import os
### 학습용 얼굴 검출 & 저장 알고리즘
base_dir = 'C:\\Users\\iniyo\\Desktop\\craw_img\\warm\\IU\\' # crawling된 이미지 파일들 저장하는 곳 절대경로
cool_worm=['warm'] # crawling_img 바로 하위 디렉토리 cool, worm 하나씩 있지만 enumrate 반복을 위해 하나씩 더 추가
cool = ['wf'] #cool 의 하위 디렉토리 이름 
worm = ['IU'] #worm 의 하위 디렉토리 이름
# lower = np.array([0, 48, 80], dtype = "uint8") # HSV 하한선
# upper = np.array([20, 255, 255], dtype = "uint8") # HSV 상한선
lower = np.array([0,133,77], dtype = np.uint8) # Ycrcb lower
upper = np.array([255,173,127], dtype = np.uint8) # Ycrcb upper
# 학습된 haar-cascade xml파일 들고오기
face_cascade = cv2.CascadeClassifier('C:\\haar\\haarcascade_frontalface_default.xml')
train_image_count = 1 # 학습할 이미지 카운트 == 디텍팅 완료된 이미지 파일 카운트
# image_dir='' # 
cool_count = 0 # cool의 count
worm_count = 0 # worm의 count
# 전역 슬레쉬 홀딩 방식
rite_dir = 'C:\\Users\\iniyo\\Desktop\\sample\\otsu\\'
train_image_list = os.listdir(base_dir)

try: # 에러발생이 안되면 실행
    face_img = cv2.imread(base_dir+"107.jpg") # 가져올 이미지 경로 (절대지정)
    gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY) #cvtColor함수를 사용하여 이미지gray scale로 변환 == mask에 사용
    faces = face_cascade.detectMultiScale(gray_face_img, 1.2, 3) # gray변환된 이미지에 스케일 팩터를 1.2로 min_nehgbor 3로 설정 : 1.2가 더욱 빠르게 연산된다고 함
    for (x,y,w,h) in faces:
        face_crop = face_img[y:y+h, x:x+w] # face_img를 x,y,w,h 에 따라 크롭
        gray_scale = gray_face_img[y:y+h, x:x+w]
    face_img_Ycrcb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2YCrCb) # ycrcb 이미지로 변환한 face_img
    t, otsu_mask1= cv2.threshold(gray_scale, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)#otsu 알고리즘, 특정 기준으로 lower은 0 upper은 1로 설정
    mask1 = cv2.inRange(face_img_Ycrcb, lower, upper) #ycrcb이미지에서 lower, upper 사이의 값
    otsu_mask = cv2.bitwise_and(otsu_mask1, otsu_mask1, mask = mask1) #mask1 과 otsu_mask를 and 연산하여 0이 아닌 부분을 남김
    # (x,y,w,h) 영역을 받아옴. 이 부분 아직 미완성
    ### 피부색 영역 추출
    skin = cv2.bitwise_and(face_crop, face_crop, mask = otsu_mask) # face_img 원본, maxking된 face_img를 bit단위 and연산 = mask가 씌워진 부분이 픽셀만 남게 됨.
    resize_skin = cv2.resize(skin,(224,224)) # mask와 and 연산된 face_img == skin 이미지를 resizing
    # 크롭한 이미지 저장
    cv2.imwrite(rite_dir+'2.jpg', cv2.resize(gray_face_img,(512,512))) #resize된 이미지를 저장할 공간을 write_path의 절대경로로 지정
    train_image_count += 1 # 계속해서 카운트 증가
except:
    pass







# try: # 에러발생이 안되면 실행
#     face_img = cv2.imread(base_dir+"107.jpg") # 가져올 이미지 경로 (절대지정)
#     gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY) #cvtColor함수를 사용하여 이미지gray scale로 변환 == mask에 사용
#     faces = face_cascade.detectMultiScale(gray_face_img, 1.2, 3) # gray변환된 이미지에 스케일 팩터를 1.2로 min_nehgbor 3로 설정 : 1.2가 더욱 빠르게 연산된다고 함
#     face_img_Ycrcb = cv2.cvtColor(face_img, cv2.COLOR_BGR2YCrCb) # ycrcb 이미지로 변환한 face_img
#     t, otsu_mask1= cv2.threshold(gray_face_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)#otsu 알고리즘, 특정 기준으로 lower은 0 upper은 1로 설정
#     mask1 = cv2.inRange(face_img_Ycrcb, lower, upper) #ycrcb이미지에서 lower, upper 사이의 값
#     otsu_mask = cv2.bitwise_and(otsu_mask1, otsu_mask1, mask = mask1) #mask1 과 otsu_mask를 and 연산하여 0이 아닌 부분을 남김
#     # (x,y,w,h) 영역을 받아옴. 이 부분 아직 미완성
#     for (x,y,w,h) in faces:
#         face_crop = face_img[y:y+h, x:x+w] # face_img를 x,y,w,h 에 따라 크롭
#         maskin_img = otsu_mask[y:y+h, x:x+w] # masking할 이미지 otsu로 머리카락, 눈, 코 등을 제거 후 피부색 연산으로 피부만 추출된 이미지
#     ### 피부색 영역 추출
#     skin = cv2.bitwise_and(face_crop, face_crop, mask = maskin_img) # face_img 원본, maxking된 face_img를 bit단위 and연산 = mask가 씌워진 부분이 픽셀만 남게 됨.
#     resize_skin = cv2.resize(skin,(512,512)) # mask와 and 연산된 face_img == skin 이미지를 resizing
#     # 크롭한 이미지 저장
#     cv2.imwrite(rite_dir+'2.jpg', cv2.resize(face_crop,(512,512))) #resize된 이미지를 저장할 공간을 write_path의 절대경로로 지정
#     train_image_count += 1 # 계속해서 카운트 증가
# except:
#     pass
