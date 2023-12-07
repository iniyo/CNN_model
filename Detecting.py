## 얼굴 영역 검출
import numpy as np
import cv2, glob
import os
### 학습용 얼굴 검출 & 저장 알고리즘
base_dir = 'C:\\Users\\iniyo\\Desktop\\craw_img' # crawling된 이미지 파일들 저장하는 곳 절대경로
cool_warm=['cool','cool','warm','warm'] # crawling_img 바로 하위 디렉토리 cool, warm 하나씩 있지만 반복을 위해 추가
cool = ['SYJ','KTL'] #cool 의 하위 디렉토리 이름 
warm = ['IU','SUJI'] #warm 의 하위 디렉토리 이름
# lower = np.array([0, 48, 80], dtype = "uint8") # HSV 하한선
# upper = np.array([20, 255, 255], dtype = "uint8") # HSV 상한선
lower = np.array([0,133,77], dtype = np.uint8) # Ycrcb lower
upper = np.array([255,173,127], dtype = np.uint8) # Ycrcb upper
# 학습된 haar-cascade xml파일 들고오기
face_cascade = cv2.CascadeClassifier('C:\\haar\\haarcascade_frontalface_default.xml')
train_image_count = 1 # 학습할 이미지 카운트 == 디텍팅 완료된 이미지 파일 카운트
# image_dir='' # 
cool_count = 0 # cool의 count
warm_count = 0 # warm의 count
# 전역 슬레쉬 홀딩 방식
for value in cool_warm: #value에 cool, warm이 차례로 들어감
    read_image_count = 1 # 각각의 연예인 사진들을 1~n까지 해둬서 다른 path로 갈때마다 1부터 시작할 수 있도록 정의
    high_dir = base_dir+'\\'+value # image 바로위의 dir
    if value == 'cool': # 해당 디렉토리 파일 경로의 cool의 경우 
        image_dir=high_dir+'\\'+cool[cool_count]+'\\' # cool_tone image가 있는 디렉토리 위치
        train_image_list = glob.glob(image_dir+"/*.jpg") # cool_tone imgae_dir 폴더 내의 파일 리스트 가지고 옴
        cool_count = 1 # 카운트 증가
        write_path = 'C:\\Users\\iniyo\\Desktop\\face_Datasets\\train_images\\cool\\' #cool-tone 저장할 절대경로
    elif value == 'warm':
        if warm_count == 0: # warm에서의 이미지 파일 이름을 1부터 초기화 하기 위해 추가 편의성을 위해 만듦
           train_image_count = 1 # cool이 끝나고 warm부터 시작할 때 1로 초기화
        image_dir=high_dir+'\\'+warm[warm_count]+'\\' # worm_tone image가 있는 디렉토리 위치
        train_image_list = glob.glob(image_dir+"/*.jpg") # warm_tone imgae_dir 폴더 내의 파일 리스트 가지고 옴
        warm_count = 1
        write_path = 'C:\\Users\\iniyo\\Desktop\\face_Datasets\\train_images\\warm\\' #warm-tone 저장할 절대경로

    for i in train_image_list: # 해당 폴더 내의 이미지 파일 리스트 만큼 반복
        try: # 에러발생이 안되면 실행
            # 가져올 이미지 경로 (절대지정)
            face_img = cv2.imread(image_dir+"{}.jpg".format(read_image_count)) 
            #cvtColor함수를 사용하여 이미지gray scale로 변환 == mask에 사용
            gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY) 
            # gray변환된 이미지에 스케일 팩터를 1.2로 min_nehgbor 3로 설정 : 1.2로 설정시 빠른 연산 가능
            faces = face_cascade.detectMultiScale(gray_face_img, 1.2, 3) 
            # Haar특징추출 영역만큼 이미지 crop
            for (x,y,w,h) in faces:
                face_crop = face_img[y:y+h, x:x+w] 
                gray_crop = gray_face_img[y:y+h, x:x+w]
            # ycrcb 이미지로 변환한 face_img    
            face_img_Ycrcb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2YCrCb) 
            #otsu 알고리즘, 특정 기준으로 lower은 0 upper은 1로 설정
            t, otsu_mask= cv2.threshold(gray_crop, 0, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            mask1 = cv2.inRange(face_img_Ycrcb, lower, upper) #ycrcb이미지에서 lower, upper 사이의 값
            #mask1 과 otsu_mask를 and 연산하여 0이 아닌 부분을 남김
            otsu_mask = cv2.bitwise_and(otsu_mask, otsu_mask, mask = mask1)
            ### 피부색 영역 추출
            # face_img 원본, maxking된 face_img를 bit단위 and연산 = mask가 씌워진 부분이 픽셀만 남게 됨.
            skin = cv2.bitwise_and(face_crop, face_crop, mask = otsu_mask) 
            # mask와 and 연산된 face_img == skin 이미지를 resizing
            resize_skin = cv2.resize(skin,(128,128))
            # 크롭한 이미지 저장
            #resize된 이미지를 저장할 공간을 write_path의 절대경로로 지정
            cv2.imwrite(write_path+'{}.jpg'.format(train_image_count), resize_skin) 
            read_image_count +=1 # 다음 value 시 초기화될 카운트
            train_image_count += 1 # 계속해서 카운트 증가
        except:
            pass
