import numpy as np
import os, cv2, glob
from sklearn.model_selection import train_test_split

# 기본 경로
base_dir = 'C:\\Users\\iniyo\\Desktop\\face_Datasets\\train_images' #학습에 사용될 이미지가 있는 폴더의 베이스
category = ['cool','warm'] # 베이스 폴더안의 학습할 폴더 목록
nb_classes = len(category) # category 길이 읽음 = 2;
X=[] # cool, warm 이미지 array 배열
Y=[] # cool, warm label 배열

for idx, cool_warm in enumerate(category): # idx에는 0, 1, value에는 cool, warm 저장
    #cool 이면 0 warm 이면 1
    data_label = (idx) # idx의 값 증가에 따라 label의 첫번째, 두번째 원소를 1로 변환
    image_dir = base_dir+'\\'+cool_warm+'\\' 
    files = glob.glob(image_dir+"/*.jpg")
    for file in files: #file = filename, filename 변수에 파일 저장
        #print(image_dir+filename) # image디렉토리 위치에 + filename 출력
        face_img = cv2.imread(file) # img변수에 이미지 imread로 계속 사진들 읽어오기 
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        precleaning_data = np.asarray(face_img)
        X.append(precleaning_data) # append를 통해 img를 마지막에 계속 추가
        Y.append(data_label) # data_label 추가 (0, 1) 0이면 cool, 1이면 warm
X = np.array(X) #array 배열로 X값 변경
Y = np.array(Y) #array 배열로 Y값 변경
# 데이타셋 저장
# defalut test_size=0.25
train_images, test_images, train_label, test_label = train_test_split(X, Y) 
xy = (train_images, test_images, train_label, test_label) #변수 xy에 나눠서 저장
np.save('C:\\Users\\iniyo\\Desktop\\face_Datasets\\learning_dataset=128.npy',xy)