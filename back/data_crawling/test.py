# 첨부된 파일은 최종 수정된 전체 코드입니다.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import requests
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

KAKAO_API_KEY = '6d9dc3df95f90cbe474e8b518e13f2f2'

seoul_gu_list = [
     "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

def get_lat_lon(address):
    import requests
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}

    time.sleep(0.2)  # <- 이 한 줄을 꼭 추가해주세요 (API 호출 간격 확보)

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json().get('documents', [])
        if result:
            return result[0]['y'], result[0]['x']
    return None, None

def init_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://map.kakao.com/')
    time.sleep(2)
    return driver

def search_keyword(driver, keyword):
    search_area = driver.find_element("id", 'search.keyword.query')
    search_area.clear()
    search_area.send_keys(keyword)
    search_area.send_keys(Keys.ENTER)
    time.sleep(3)
    remove_dimmed_layer(driver)
    click_place_tab(driver)
    click_place_more(driver)

def remove_dimmed_layer(driver):
    try:
        dimmed_layer = driver.find_element(By.ID, 'dimmedLayer')
        driver.execute_script("arguments[0].style.display='none';", dimmed_layer)
    except:
        pass

def click_place_tab(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="info.main.options"]/li[2]/a'))
    ).click()
    time.sleep(2)

def click_place_more(driver):
    try:
        driver.find_element(By.ID, 'info.search.place.more').click()
        time.sleep(2)
    except:
        pass

def expand_menu_tab_and_collect(driver):
    menu_items = []
    period_text = "영업시간 정보 없음"

    # 메뉴 탭 클릭 및 메뉴 수집
    try:
        menu_tab = driver.find_element(By.CSS_SELECTOR, 'a[href="#menuInfo"]')
        menu_tab.click()
        time.sleep(1)

        while True:
            try:
                more_button = driver.find_element(By.CSS_SELECTOR, '.wrap_more a.link_more')
                if more_button.is_displayed():
                    more_button.click()
                    time.sleep(1)
                else:
                    break
            except:
                break

        menu_elements = driver.find_elements(By.CSS_SELECTOR, '.list_goods > li')
        for element in menu_elements:
            name = element.find_element(By.CSS_SELECTOR, '.tit_item').text.strip()
            price = element.find_element(By.CSS_SELECTOR, '.desc_item').text.strip() if element.find_elements(By.CSS_SELECTOR, '.desc_item') else '가격정보 없음'
            menu_items.append(f'{name} ({price})')

    except Exception as e:
        menu_items = ['메뉴 없음']

    # 명확히 정보(info) 탭 클릭 후 영업시간 가져오기 (이 부분이 중요!)
    try:
        info_tab = driver.find_element(By.CSS_SELECTOR, 'a[href="#info"]')
        info_tab.click()
        time.sleep(1)

        # 정확한 선택자 사용
        period_element = driver.find_element(By.CSS_SELECTOR, '.openhour .periodWarp a')
        period_text = period_element.text.strip()
    except:
        period_text = "영업시간 정보 없음"

    return menu_items if menu_items else ['메뉴 없음'], period_text

def get_store_details(driver, detail_url):
    original_window = driver.current_window_handle
    driver.execute_script("window.open(arguments[0]);", detail_url)
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    menu_list, periodTxt = expand_menu_tab_and_collect(driver)
    menu_text = ', '.join(menu_list)
    driver.close()
    driver.switch_to.window(original_window)
    return menu_text, periodTxt

def crawl_all_pages(driver):
    all_data = []

    def process_current_page():
        nonlocal all_data
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        stores = soup.select('.placelist > .PlaceItem')

        for store in stores:
            try:
                name = store.select_one('.head_item .tit_name .link_name').text.strip()
                subcategory = store.select_one('.head_item .subcategory').text.strip()
                degree = store.select_one('.rating .score .num').text.strip()
                review_count = store.select_one('.review em[data-id="numberofreview"]').text.strip() or '0'
                address = store.select_one('.info_item .addr').text.strip()
                tel = store.select_one('.info_item .phone').text.strip() if store.select_one('.info_item .phone') else '전화번호 없음'
                detail_url = store.select_one('.contact .moreview')['href']

                # ✅ 이 부분에서 영업시간 바로 수집 (상세보기 들어가기 전)
                try:
                    period_element = store.select_one('div.openhour p.periodWarp > a')
                    periodTxt = period_element.text.strip() if period_element else "영업시간 정보 없음"
                except:
                    periodTxt = "영업시간 정보 없음"

                menu_text, _ = get_store_details(driver, detail_url)  # 메뉴만 상세보기에서 가져오기

                print(f"{name} | {subcategory} | 평점: {degree} | 리뷰: {review_count}개 | 영업시간: {periodTxt}")
                all_data.append([name, subcategory, degree, review_count, address, tel, menu_text, periodTxt])

            except Exception as e:
                print(f"❌ 매장 크롤링 실패: {e}")


    page = 1
    while True:
        process_current_page()
        try:
            next_btn = driver.find_element(By.ID, 'info.search.page.next') if page % 5 == 0 else driver.find_element(By.ID, f'info.search.page.no{page%5+1}')
            next_btn.click()
            page += 1
            time.sleep(2)
        except:
            break
    return all_data

if __name__ == '__main__':
    for gu in seoul_gu_list:
        driver = init_driver()
        search_keyword(driver, f'{gu} 맛집')
        data = crawl_all_pages(driver)
        today = datetime.now().strftime("%Y%m%d")
        filename = f'{today}_{gu}_맛집_크롤링.csv'
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['이름', '서브카테고리', '평점', '리뷰수', '주소', '위도', '경도', '전화번호', '메뉴', '영업시간'])
            for row in data:
                lat, lon = get_lat_lon(row[4])
                writer.writerow(row[:5] + [lat, lon] + row[5:])
        driver.quit()
