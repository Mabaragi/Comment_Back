# 1. 베이스 이미지 설정
FROM python:3.12

# 2. 환경 변수 설정
ENV POETRY_VIRTUALENVS_CREATE=false
#     POETRY_HOME="/opt/poetry" \
#     PATH="$POETRY_HOME/bin:$PATH" \
#     POETRY_VIRTUALENVS_IN_PROJECT=true \
#     POETRY_NO_INTERACTION=1

# 3. 필수 패키지 설치
RUN pip install poetry
    # apt-get update && apt-get install -y curl build-essential && \
    # curl -sSL https://install.python-poetry.org | python3 - && \
    # apt-get purge -y --auto-remove curl build-essential && \
    # rm -rf /var/lib/apt/lists/*

# 4. 작업 디렉토리 설정
WORKDIR /app

# 5. 의존성 파일 복사
COPY pyproject.toml poetry.lock* /app/

# 6. 의존성 설치
RUN poetry install
# 7. 애플리케이션 코드 복사
COPY . /app

# 8. 애플리케이션 빌드 (필요시)
# RUN poetry build

# 9. 실행 명령 설정
# 0.0.0.0 을 해야 외부에서 접근할 수 있다.
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]