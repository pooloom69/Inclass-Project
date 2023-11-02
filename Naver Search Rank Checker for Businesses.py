from selenium import webdriver   # 셀레니움4 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 네이버 view 블로그 수위 추적 프로그램 로직
# view tracking
# selenium 크롬창을 코드로 제어하는것 화면에 보이는 모든걸 컨트롤 할수 있음


# chromedriver 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
import time
# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬드라이버매니저를 이용해서 크롬드라이버를 자동으로 설치해서 최신버전을 자동으로 가져오게함 
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = chrome_options)
driver.implicitly_wait(5) # 웹페이지가 로딩 될때까지 5초는 기다림


queries = ["꿀사과"]
target_product_codes = ["35889305810"]
for query, target_product_code in zip(queries, target_product_codes):
    real_ranking = -1
    ranking = -1
    for page_index in range(1,15):  # 1~15 페이지까지 중
    # 1. url로 페이지 1 방문
        shopping_link = f"https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery=%EA%BF%80%EC%82%AC%EA%B3%BC&pagingIndex={page_index}&pagingSize=40&productSet=total&query={query}&sort=rel&timestamp=&viewType=list"
        driver.get(shopping_link)
        time.sleep(3)

        # 2. 페이지 4-5 밑으로 내리기 상품 더 불러오기
        for _ in range(5):
            driver.execute_script("window.scrollBy(0,10000);") 
            time.sleep(0.5)
        # 3. 타겟 상품이 페이지에 노출되고 있는 지 확인하기 
        try:
            target_product_selector= f"a[data-i='{target_product_code}']"
            target_product_element = driver.find_element(By.CSS_SELECTOR,target_product_selector)
            data = target_product_element.get_attribute('data-nclick') # 코드안 정보 다 가져올수 있음 그중에 특정할수 있음
            real_ranking = data.split(f",i:{target_product_code}")[0].split("N=a:lst*N.image,r:")[1]
    # N=a:lst*N.image,r:162,i:35889305810
            ranking = int(real_ranking) - (int(page_index) -1) * 40    # 페이지당 40개 개시물 페이지 넘어가면 등수도 40등 추가됨 
            break # 페이지 인덱스 for문 탈출  페이지 잘 찾았을경우 스탑 
        except:
            print(f"{page_index} 페이지에서 타겟 상품을 못찾음. ")
    print(" 내 상품의 진짜 등수는 ", real_ranking, "등 입니다. ")
    print(f"내 상품은 {page_index} 페이지의 {ranking}등에 노출되고 있습니다. ")

    # 4. 없다면 -> url next page 방문 
input()





