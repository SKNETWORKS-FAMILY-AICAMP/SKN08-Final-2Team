from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 웹드라이버 실행
url = 'https://map.kakao.com/'
driver = webdriver.Chrome()
driver.get(url)

searchloc = input('찾고 싶은 음식 종류 : ')

# 검색어 입력 및 검색 실행
search_area = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')
search_area.send_keys(searchloc)
driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
time.sleep(2)

# 장소 버튼 클릭
driver.find_element(By.XPATH, '//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER)
time.sleep(2)

def get_store_details(store_element):
    """상세보기 페이지에서 메뉴 및 후기 정보 가져오기"""
    try:
        # `moreview` 버튼 찾기 (BeautifulSoup 활용)
        moreview_button = store_element.select_one('.contact .moreview')
        if not moreview_button:
            print("moreview 버튼 없음, 건너뜁니다.")
            return "메뉴 없음", "후기 없음"

        # Selenium을 활용하여 `moreview` 버튼 클릭
        try:
            moreview_button_element = store_element.find_element(By.CSS_SELECTOR, ".contact .moreview")
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(moreview_button_element))
            driver.execute_script("arguments[0].click();", moreview_button_element)  # JavaScript로 강제 클릭
            time.sleep(2)
        except Exception as e:
            print(f"moreview 클릭 실패: {e}")
            return "메뉴 없음", "후기 없음"

        # 새 탭이 열렸는지 확인
        if len(driver.window_handles) < 2:
            print("새 창이 열리지 않음, 건너뜁니다.")
            return "메뉴 없음", "후기 없음"

        # 새 창으로 전환
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

        # HTML 파싱
        detail_html = driver.page_source
        detail_soup = BeautifulSoup(detail_html, 'html.parser')

        # 메뉴 정보 가져오기
        menu_list = []
        menu_elements = detail_soup.select('.cont_menu .list_menu li')
        for menu in menu_elements:
            menu_name = menu.select_one('.info_menu .loss_word')
            menu_price = menu.select_one('.info_menu .price_menu')
            if menu_name:
                menu_text = menu_name.text.strip()
                price_text = menu_price.text.strip() if menu_price else "가격 없음"
                menu_list.append(f"{menu_text}({price_text})")

        # 후기에 있는 모든 정보 가져오기
        review_list = []
        review_elements = detail_soup.select('.list_evaluation .comment_info')
        for review in review_elements:
            review_text = review.text.strip()
            review_list.append(review_text)

        # 메뉴 및 후기 데이터 정리
        menu_text = ", ".join(menu_list) if menu_list else "메뉴 없음"
        review_text = "\n".join(review_list) if review_list else "후기 없음"

        # 상세보기 페이지 닫기 및 원래 페이지로 이동
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        return menu_text, review_text

    except Exception as e:
        print(f"상세 정보 크롤링 실패: {e}")

        # 만약 세션 오류가 발생하면 다시 원래 창으로 이동
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])

        return "메뉴 없음", "후기 없음"

def storeNamePrint(page):
    """음식점 리스트 크롤링 + 상세정보 크롤링"""
    time.sleep(0.5)

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
        addr = store.select('.info_item > .addr')[0].text.splitlines()[1]
        tel = store.select('.info_item > .contact > .phone')[0].text

        # 상세정보 가져오기 (메뉴 및 후기)
        menu_text, review_text = get_store_details(store)

        print(name, degree, review_num, addr, tel, menu_text, review_text)

        temp.append(name)
        temp.append(degree)
        temp.append(review_num)
        temp.append(addr)
        temp.append(tel)
        temp.append(menu_text)
        temp.append(review_text)

        list.append(temp)

    # CSV 파일 저장
    mode = 'w' if page == 1 else 'a'
    with open('맛집_상세정보.csv', mode, encoding='utf-8-sig', newline='') as f:
        writercsv = csv.writer(f)
        if page == 1:
            writercsv.writerow(['name', 'degree', 'review num', 'address', 'tel', 'menu', 'reviews'])
        writercsv.writerows(list)

# 첫 번째 페이지 크롤링
storeNamePrint(1)

try:
    page = 1
    while True:
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

        # "다음" 버튼 클릭하여 다음 페이지 그룹으로 이동
        next_btn = driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]')

        # "다음" 버튼이 비활성화 상태이면 크롤링 종료
        if "disabled" in next_btn.get_attribute("class"):
            print("마지막 페이지입니다. 크롤링 종료.")
            break

        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)

except Exception as e:
    print(f"오류 발생: {e}")

# 웹드라이버 종료
driver.quit()
