from flask import Flask, render_template, Response, redirect, request
from flask_cors import CORS
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time

import selenium.common.exceptions as expt

app = Flask(__name__)
CORS(app)

# 환경 변수 설정
SELENIUM_SERVER = 'http://selenium-server:4444/wd/hub'
DEFAULT_WAIT_TIME = 10
LONG_WAIT_TIME = 60

def initialize_driver(link):
    # """드라이버 초기화 및 페이지 열기"""
    options = Options()
    try:
        driver = webdriver.Remote(command_executor=SELENIUM_SERVER, options=options)
        driver.get(link)
        driver.implicitly_wait(DEFAULT_WAIT_TIME)
        return driver
    except expt.WebDriverException as e:
        print(f"WebDriverException 발생: {e}")
    except Exception as e:
        print(f"드라이버 초기화 중 예외 발생: {e}")
    return None



###### 간편인증 로그인으로 이동
def login_redirect(driver):
    try:
        #로그인버튼 클릭
        driver.find_element(By.ID, 'group1544').click()

        #화면로딩대기
        driver.implicitly_wait(60)

        #iframe 내부요소선택
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "txppIframe"))
        )
        #방화벽/보안프로그램 이용 동의체크
        # 체크박스 요소를 찾습니다.
        checkbox_0 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "w2checkbox_item_0"))
        )
        checkbox_1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "w2checkbox_item_1"))
        )
        apply_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnApply"))
        )

        # 체크박스가 체크되어 있지 않다면 클릭합니다.
        if not checkbox_0.is_selected():
            checkbox_0.click()

        if not checkbox_1.is_selected():
            checkbox_1.click()

        # 두 체크박스 모두 체크되어 있으면 '적용' 버튼 클릭
        if checkbox_0.is_selected() and checkbox_1.is_selected():
            apply_button.click()
            
        #화면로딩대기
        time.sleep(1)
        #메인컨텐츠 재선택
        driver.switch_to.default_content()
        # iframe이 로드될 때까지 최대 10초간 기다립니다.
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "txppIframe"))
        )
        #간편인증 선택
        driver.find_element(By.ID, "anchor14").click()
        #화면로딩대기
        time.sleep(0.5)
        #간편인증 버튼클릭
        driver.find_element(By.ID, "anchor23").click()

        WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "UTECMADA02_iframe"))
        )
        WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "simple_iframeView"))
        )
    except Exception as e:
        print(f"로그인 리다이렉트 중 오류 발생: {e}")

########## 간편인증 로그인으로 이동
def login_easy(driver:webdriver,name,birth,phone1,phone2):

    try:
        #통신사패스 빼고는 본인인증란 동일
        # name = "yourname"
        # birth = "yyyymmdd"
        # phone = "00000000"


        #간편인증 선택된 항목 클릭
        text = "네이버"
        # XPath를 사용하여 조건에 맞는 label 선택
        # 이 XPath는 'label' 내부에 클래스가 'label-nm'인 'span'이 있고, 그 안에 텍스트가 '원하는 텍스트'인 'p' 태그가 있는 요소를 찾습니다.
        label_to_click = driver.find_element(By.XPATH, f"//label[.//span[contains(@class, 'label-nm')]//p[text()='{text}']]")

        # 찾은 label 클릭
        label_to_click.click()

        try:
            # 드롭다운 요소를 찾습니다.
            dropdown_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'select[data-id="oacx_phone1"]'))
            )
            select = Select(dropdown_element)
            select.select_by_value(phone1)  # phone1은 해당 드롭다운에서 선택하려는 옵션의 value입니다.

            # 이름 입력 필드
            name_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-id="oacx_name"]'))
            )
            name_field.send_keys(name)

            # 생년월일 입력 필드
            birth_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-id="oacx_birth"]'))
            )
            birth_field.send_keys(birth)

            # 추가 전화번호 입력 필드
            phone2_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-id="oacx_phone2"]'))
            )
            phone2_field.send_keys(phone2)

        except expt.NoSuchElementException:
            print("요청한 요소를 찾을 수 없습니다.")
        except expt.TimeoutException:
            print("요청한 요소가 지정된 시간 내에 나타나지 않았습니다.")
        except Exception as e:
            print(f"예외가 발생했습니다: {e}")


        #서비스이용동의
        driver.find_element(By.ID, "totalAgree").click()
        time.sleep(0.5)

        #인증요청 버튼 클릭
        driver.find_element(By.ID, "oacx-request-btn-pc").click()

        try:
            # 'alertArea' 클래스가 보이는지 3초 동안 기다립니다.
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alertArea"))
            )
            # 'alertArea'가 보이면 사용자 정의 예외를 발생시킵니다.
            raise Exception("사용자 정보 불일치")
        except expt.TimeoutException:
            # 'alertArea'가 3초 동안 보이지 않으면, 정상적인 처리를 계속합니다.
            print("사용자 정보 확인")

        #인증확인했다고치고... 대기
        time.sleep(15)

        #인증확인 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, ".btnArea button:nth-of-type(2)").click()

        #화면로딩대기
        time.sleep(3)

    except Exception as e:
        print(f"간편인증 로그인 중 오류 발생: {e}")


#세무대리수임동의
def page_locate2(driver:webdriver):
    try:
        #메인컨텐츠 재선택
        driver.switch_to.default_content()
        
        #세무대리 납세관리 클릭
        driver.find_element(By.ID, "hdGrp920").click()

        #화면로딩대기_redirect
        driver.implicitly_wait(60)

        #메인컨텐츠 재선택
        driver.switch_to.default_content()
        # iframe이 로드될 때까지 최대 10초간 기다립니다.
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "txppIframe"))    
        )

        #세무대리 수임동의 클릭
        driver.find_element(By.ID, "a_a_4806020000").click()
    
    except Exception as e:
        print(f"세무대리수임동의 중 오류 발생: {e}")


## [Flask 서버 구동] ##########################################################

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    # """기본 라우트"""
    return "Hello World! Try /test for Selenium test."

@app.route('/form')
def form():
    return render_template('test.html')

@app.route('/gogo',methods=['post'])
def gogo():
    name = request.form['name']
    birth = request.form['birth']
    phone1 = request.form['phone1']
    phone2 = request.form['phone2']

    global driver
    link = "https://www.hometax.go.kr"
    driver = initialize_driver(link)
    login_redirect(driver)
    login_easy(driver,name,birth,phone1,phone2)
    page_locate2(driver)

    title = driver.title
    driver.quit()
    return f"Title: {title}"

@app.route('/test')
def test():
    # """Selenium 테스트 실행"""
    driver = initialize_driver("http://naver.com")
    if not driver:
        return "Driver initialization failed", 500

    try:
        login_redirect(driver)
        title = driver.title
        driver.quit()
        return f"Page Title: {title}"
    except Exception as e:
        driver.quit()
        return f"Error during Selenium operation: {str(e)}", 500

@app.route('/status')
def server_status():
    # """서버 상태 확인"""
    return "Server is up and running!"

    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)