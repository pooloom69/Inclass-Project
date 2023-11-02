from selenium import webdriver   # 셀레니움4 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
# chromedriver 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 크롬드라이버매니저를 이용해서 크롬드라이버를 자동으로 설치해서 최신버전을 자동으로 가져오게함 
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = chrome_options)
# 모바일로 봐야 링크 찾기 쉬움

# href="/hospital/1817665838?entry=pll"
# href="/hospital/13350771?entry=pll" 센텀린의원 4등
# href="/restaurant/17073562?entry=pll"  2등

# 4. 여러키워드 여러 업체의 순위를 찾는 프로그램으로 변경
store_ids = ["13350771","17073562"]
queries = ["부산피부과", "부산카페"]

for store_id, query in zip(store_ids,queries):

# 1. 네이버 검색창 + 쿼리로 드라이버 get
    search_link = f"https://m.search.naver.com/search.naver?where=m&sm=top_hty&fbm=0&ie=utf8&query={query}"
    driver.get(search_link)

    # 2. place 더보기 탭을 클릭하기 (업다면, 에러)
    try:
        more_selector = "a.cf8PL"  # class이름으로 셀렉터 
        place_more_element = driver.find_element(By.CSS_SELECTOR,more_selector )
        place_more_element.click() 
    except:
        print(f"{query}키워드로 업체의 플레이스 순위를 알 수 없습니다. ")
        continue
        # 여기서, 함수 종료해야함 
    # 3. 내가 찾으려는 업체의 id를 기반으로 찾기
    time.sleep(3)
    # 페이지 = 'abcdef' 일때  *= 'ab' 일경우 ab가 포함된 엘리먼트 페이지를 찾아줌   
    store_ID_selector = f"a[href*='/{store_id}?entry=pll']"

    # 3-2 없으면 인피니티 스크롤 5번 정도 실행
    for _ in range(5):
        store_elements = driver.find_elements(By.CSS_SELECTOR, store_ID_selector) # -> 리스트 형태로 업체를 찾아줌

        if len(store_elements) < 1 :  # 셀렉터를 찾아봤는데 못찾았을 경우 len은 0 이될것 임  0인 경우 스크롤필요 
            print("순위권에 업체가 없어서 스크롤을 합니다. ")
            scrolly = 20000  # 20000 pixel
            #driver.execute_script("window.scrollBy(0,20000);")  # execute_script 를 개발자툴 콘솔에 입력하면 스크롤
            ActionChains(driver).scroll(200,450,200,scrolly).perform() #(sx,sy,tx(target x),ty)# 플레이스는 스크롤이 지도에 고정되어 있기 때문에 execute_script 로 스크롤이 안될수 있음
            time.sleep(3)

    if len(store_elements) < 1:  # 스크롤했는데도 셀렉터로 못찾은 경우 
        print("검색 결과로는 순위가 잡히지 않는 업체입니다. ")
        continue
        # 여기서 해당키워드 작업은 종료해야함  업체for문 저위에 있는거에 적용 

    store_element = random.choice(store_elements)
    for _ in range(5):  # 위로 한칸씩 거슬러 올라가서 타겟업체의 LI태크 찾기 
        target_store_element = store_element.find_element(By.XPATH, "./..")
        tagname = target_store_element.get_attribute("tagName")
        if tagname == "li":
            print("li 태그를 잘 찾았습니다")
            break  
        store_element = target_store_element   


    # li 태그가 몇번 거슬로 올라갔는지는 알수 없으므로 전체 태그에서 찾도록함     
    entire_list_selector = "#_list_scroll_container > div > div > div:nth-child(2) > ul > li"
    entire_list_element = driver.find_elements(By.CSS_SELECTOR, entire_list_selector)
    rank = 1
    for each_element in entire_list_element:
        #try:
        #   each_element.find_element(By.CSS_SELECTOR,"광고")
        #   continue
        #except:
        #    pass   광고 없어서 패스  
        if each_element == target_store_element:
            break
        rank += 1  # 같지 않으면 돌아서 찾기 
    print(f"{query} // 현재 {rank} 등에 노출되고 있습니다")  # 타겟 업체가 몇등에 노출되고 있는지 찾는 프로그램 

input()


