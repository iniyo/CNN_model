from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request # URL을 가져오기 위한 파이썬 모듈
import time
import os

cool_warm = ['cool','warm']
#이미지 다운시 특정 사이트의 경우 봇이 차단하는 것을 막기위해 브라우저를 속임
opener=urllib.request.build_opener() # 오프너 객체를 만드는 함수
# 지정된 헤더 및 값을 User-Agent HTTP 헤더에 추가
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# chromedriver를 미리 다운받아 줘야한다.
driver = webdriver.Chrome('C:\Temp\chromedriver.exe') #chrome 드라이버 절대경로 지정(내 노트북)
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&ogbl") # google의 이미지 검색 설정 URL

## 크롤링 할 연예인, 폴더 위치 설정
#다운받을 이미지 이름(연예인 말고도 가능)
celebrity_label ='박보영'
cool_warm = cool_warm[1] #cool이면 0 warm이면 1
dir = '박보영'

img_folder = 'C:\\Users\\iniyo\\Desktop\\craw_img\\{}\\{}\\'.format(cool_warm, dir) # 이미지를 저장할 폴더, cool, warm, celebrity_label에 따라 계속 바꿔줘야하는 번거로움이 있다. 
if not os.path.isdir(img_folder) : # dir 있는지 확인
    os.mkdir(img_folder) # 없으면 새로 생성

elem = driver.find_element_by_name("q") # 구글 입력창 name을 가져와서 접근 입력창 name이 q/ 클래스도 가능
elem.send_keys(celebrity_label) #send_keys를 통해 입력창에 아이유 입력
elem.send_keys(Keys.RETURN) #keys.RETURN은 엔터키를 의미한다. 엔터키 입력

SCROLL_PAUSE_TIME = 1 # 지연시간 지정
#java script 코드 실행, 브라우저의 높이값을 java script로 찾아서 last_height에 저장 document.body.scrollHeight가 브라우저의 높이
last_height = driver.execute_script('return document.body.scrollHeight') 

while True: # 무한반복문
    # 브라우저 끝까지 스크롤을 내림
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
    #page load 동안 시간 지연 / SCROLL_PAUSE_TIME = 1.5로 지정 (1.5sec)
    time.sleep(SCROLL_PAUSE_TIME) 
    # 브라우저의 높이를 다시 구해서 nwe_height에 담음
    new_height = driver.execute_script('return document.body.scrollHeight') 
    if new_height == last_height: #반복 종료문 즉
        try: # 해당 구문을 실행했을때 오류가 나면 except로 넘어가게 되고 break가 걸리게 된다.
            #.mye4qd class를 찾아서 click함수를 통해 click
            driver.find_element_by_css_selector('.mye4qd').click()  
        except:
            break
    last_height = new_height 
    
count = 1
images = driver.find_elements_by_css_selector('.rg_i.Q4LuWd') #css 선택기 해당 클래스를 선택
for image in images: 
    try:
        image.click() #css class 선택
        time.sleep(3) # 이미지 로드 시간을 벌기 위해 다음 코드 실행시간지연
        imgurl = driver.find_element_by_css_selector('.n3VNCb').get_attribute('src') 
        outfile = str(count)+'.jpg' # 저장할 이미지 이름 1부터 n까지
        #int count를 문자형으로 변환 후 더함 = 해당 파일명
        urllib.request.urlretrieve(imgurl, img_folder + outfile) 
        count += 1 
    except: # 오류발생시 실행
        pass
    
# naver에서 받아올 url.
url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query={}".format(celebrity_label) 
driver.get(url) #d위의 url을 driver에 받아옴
    
for i in range(10): #네이버는 최대 10번까지 스크롤을 지원하기 때문에 10으로 지정
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    soup = BeautifulSoup(driver.page_source, 'html.parser') # html parsing
    #find_all로 _iamge에 해당하는 태그를 모두 리스트로 반환, tag를 class 이름으로 찾는다.
    tags = soup.find_all('img', class_='_image') 
    print(tags) # tag 확인을 위한 출력
    
for i in range(len(tags)): #이미지가 이상하게 저장되는 현상이 있었다.
    if tags[i]["src"][0] != 'h': 
        img_file = tags[i]["data-lazy-src"].split('&')
    else:
        img_file = tags[i]["src"].split('&')
    #urllib.request.urlretrieve(imgurl, img_folder + outfile)
    # 저장될 위치와 이름 지정
    urllib.request.urlretrieve(img_file[0], img_folder + str(count)+'.'+img_file[0].split('.')[-1])
    count += 1


driver.close() # 모든 명령 수행후 웹브라우저 종료