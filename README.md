# 🚀 Hometax & Public Scraping Engine (Prototype)



본 프로젝트는 홈택스(Hometax)를 포함한 공공기관 사이트의 복잡한 웹 구조를 분석하고, Docker 기반의 안정적인 수집 환경을 구축한 스크래핑 엔진 프로토타입입니다.



## 🛠 Key Features



* **복잡한 UI 완벽 제어**: 3중 이상의 iframe 구조 및 동적 보안 팝업에 대응하는 `WebDriverWait` 로직 구현

* **정밀한 데이터 추출**: ID가 유동적인 DOM 환경에서 동적 요소 추적 및 추출 

* **인프라 환경 표준화**: `Docker Compose`를 활용하여 M1 Mac(ARM)과 서버(Linux) 환경 간 아키텍처 불일치 해결

* **서비스화 검증**: Jupyter Notebook에서 검증된 로직을 Flask API 서버(`app3.py`)로 연동 및 구현



## 📂 Project Structure



* `app3.py`: Flask 기반의 메인 스크래핑 서비스 API

* `docker-compose.yml`: Selenium Grid 서버 및 Flask 앱 컨테이너 오케스트레이션

* `dockerfile`: Python 및 라이브러리 실행 환경 빌드 설정

* `research_note.ipynb`: 홈택스 웹 구조 분석 및 로직 검증 기록 (원본: 0529.ipynb)

* `templates/`: 서비스 테스트용 HTML 파일 (인증 정보 입력 폼 등)

* `requirements.txt`: 프로젝트 의존성 관리



## 💻 Tech Stack



* **Language**: Python 3.11

* **Automation**: Selenium, WebDriver

* **Backend**: Flask

* **Infrastructure**: Docker, Docker-Compose (Selenium Grid - Chromium)



---

*본 프로젝트는 개인정보가 마스킹 처리된 프로토타입 버전입니다.*
