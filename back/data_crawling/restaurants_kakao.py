from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

url = 'https://map.kakao.com/'
driver = webdriver.Chrome()  # 크롬 드라이버 경로
driver.get(url)

searchloc = input('찾고 싶은 음식 종류 : ')

# 음식점 입력 후 찾기 버튼 클릭 
search_area = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')   # 검색창
search_area.send_keys(searchloc)
driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
time.sleep(2)

# 장소 버튼 클릭 
driver.find_element(By.XPATH, '//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER)
time.sleep(2)

def storeNamePrint(page):
    time.sleep(0.5)  # 페이지 로딩 대기

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    store_lists = soup.select('.placelist > .PlaceItem')
    list = []

    for store in store_lists:
        temp = []
        name = store.select('.head_item > .tit_name > .link_name')[0].text
        degree = store.select('.rating > .score > .num')[0].text
        review_element = store.select_one('.review > em[data-id="numberofreview"]')
        review_num = review_element.text if review_element else '0'
        addr = store.select('.info_item > .addr')[0].text.splitlines()[1]  # 도로명주소 
        tel = store.select('.info_item > .contact > .phone')[0].text

        print(name, degree, review_num, addr, tel, '-')

        temp.append(name)
        temp.append(degree)
        temp.append(review_num)
        temp.append(addr)
        temp.append(tel)

        list.append(temp)

    # 첫 번째 페이지인 경우 CSV 파일 생성, 이후에는 추가
    mode = 'w' if page == 1 else 'a'
    with open('중랑구 맛집.csv', mode, encoding='utf-8-sig', newline='') as f:
        writercsv = csv.writer(f)
        if page == 1:
            writercsv.writerow(['name', 'degree', 'review num', 'address', 'tel'])  # 헤더 추가
        writercsv.writerows(list)


# 첫 번째 페이지 데이터 크롤링
storeNamePrint(1)

try:
    page = 1
    while True:
        # 1~5, 6~10, 11~15 ... 페이지 크롤링
        for i in range(1, 6):
            try:
                xPath = f'//*[@id="info.search.page.no{i}"]'
                driver.find_element(By.XPATH, xPath).send_keys(Keys.ENTER)
                time.sleep(0.5)
                storeNamePrint(page)
                page += 1
            except:
                print("더 이상 페이지 없음.")
                break

        # "다음" 버튼 찾기
        next_btn = driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]')

        # "다음" 버튼이 비활성화 상태이면 크롤링 종료
        if "disabled" in next_btn.get_attribute("class"):
            print("마지막 페이지입니다. 크롤링 종료.")
            break

        # "다음" 버튼 클릭하여 다음 페이지 그룹으로 이동
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)

except Exception as e:
    print(f"오류 발생: {e}")
