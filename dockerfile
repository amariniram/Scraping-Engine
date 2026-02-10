FROM --platform=linux/x86_64 python:3.11.7-slim

# 환경 변수 설정
ENV FLASK_ENV=development

# 필요한 패키지 설치
# Flask와 Selenium 사용을 고려하여 필요한 패키지만 설치
RUN apt-get update && apt-get install -y \
    xvfb \ 
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정 및 소스 코드 복사
WORKDIR /app
COPY . /app

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 실행 명령
CMD ["python", "app3.py"]
