FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir .

# 소스 코드 복사
COPY src/ ./src/

# 환경 변수 설정
ENV PYTHONPATH=/app/src
ENV PORT=8000

# 포트 노출
EXPOSE 8000

# SSE 서버 실행
CMD ["python", "-m", "pyongyang_naengmyeon.mcp_server"]
