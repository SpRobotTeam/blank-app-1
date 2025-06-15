# 🚀 배포 가이드

## 📋 목차

1. [로컬 개발 환경](#-로컬-개발-환경)
2. [Streamlit Cloud 배포](#-streamlit-cloud-배포)
3. [Docker 배포](#-docker-배포)
4. [성능 최적화](#-성능-최적화)
5. [모니터링](#-모니터링)

## 🏠 로컬 개발 환경

### 요구사항
- Python 3.9 이상
- pip 또는 conda

### 설치 및 실행
```bash
# 1. 저장소 클론
git clone <repository-url>
cd blank-app-1

# 2. 가상 환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정 (선택사항)
cp .env.example .env
# .env 파일을 편집하여 설정 조정

# 5. 애플리케이션 실행
streamlit run streamlit_app.py
```

## ☁️ Streamlit Cloud 배포

### 자동 배포
1. GitHub에 저장소 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud)에 접속
3. GitHub 계정 연결
4. 저장소 선택 및 배포 설정
5. 자동 배포 완료

### 설정 파일
```toml
# .streamlit/config.toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
headless = true
enableCORS = false
maxUploadSize = 200
```

### 환경 변수 (Streamlit Cloud)
```
APP_NAME=SPsystems 다기능 분석 도구
APP_VERSION=2.1.0
DEVELOPER=SPsystems 연구소 개발팀
```

## 🐳 Docker 배포

### Docker 이미지 빌드
```bash
# 이미지 빌드
docker build -t spsystems-analysis-tool .

# 컨테이너 실행
docker run -p 8501:8501 spsystems-analysis-tool
```

### Docker Compose 사용
```bash
# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

### 프로덕션 배포 (예: AWS ECS)
```bash
# 1. ECR에 이미지 푸시
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com

docker tag spsystems-analysis-tool:latest <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com/spsystems-analysis-tool:latest

docker push <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com/spsystems-analysis-tool:latest

# 2. ECS 서비스 업데이트
aws ecs update-service --cluster <cluster-name> --service <service-name> --force-new-deployment
```

## ⚡ 성능 최적화

### 1. 캐싱 활용
```python
import streamlit as st

@st.cache_data(ttl=3600)
def load_large_dataset():
    # 대용량 데이터 로딩
    pass

@st.cache_data
def expensive_computation(data):
    # 복잡한 계산
    pass
```

### 2. 메모리 최적화
```python
# 대용량 DataFrame 처리
def process_large_dataframe(df):
    # 청크 단위 처리
    chunk_size = 10000
    for chunk in pd.read_csv(file, chunksize=chunk_size):
        # 처리 로직
        pass
```

### 3. 세션 상태 관리
```python
# 불필요한 상태 정리
def cleanup_session_state():
    keep_keys = ['user_id', 'current_project']
    for key in list(st.session_state.keys()):
        if key not in keep_keys:
            del st.session_state[key]
```

## 📊 모니터링

### 성능 모니터링 활성화
```python
from utils.performance_enhanced import enable_performance_mode

# 앱 시작 시 호출
enable_performance_mode()
```

### 로그 모니터링
```bash
# 실시간 로그 확인
tail -f logs/app.log
tail -f logs/performance.log

# 로그 분석
grep "ERROR" logs/app.log
grep "slow" logs/performance.log
```

### 시스템 리소스 모니터링
```bash
# CPU, 메모리 사용률 확인
htop
# 또는
top

# 디스크 사용량
df -h

# 네트워크 연결
netstat -tulpn | grep 8501
```

## 🔧 문제 해결

### 일반적인 문제들

#### 1. 메모리 부족
```bash
# 스왑 파일 생성 (Linux)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 2. 포트 충돌
```bash
# 사용 중인 포트 확인
lsof -i :8501

# 프로세스 종료
kill -9 <PID>
```

#### 3. 의존성 충돌
```bash
# 가상 환경 재생성
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📈 배포 후 체크리스트

- [ ] 애플리케이션 정상 접속 확인
- [ ] 모든 기능 동작 테스트
- [ ] 성능 지표 모니터링 설정
- [ ] 로그 수집 설정
- [ ] 백업 계획 수립
- [ ] 보안 설정 점검
- [ ] 사용자 문서 업데이트

## 🔒 보안 고려사항

### 환경 변수 관리
```bash
# 민감한 정보는 환경 변수로 관리
export SECRET_KEY="your-secret-key"
export DATABASE_URL="your-database-url"
```

### 접근 제어 (선택사항)
```python
# streamlit-authenticator 사용
import streamlit_authenticator as stauth

# 사용자 인증 설정
authenticator = stauth.Authenticate(...)
```

## 📞 지원

문제가 발생하면 다음 정보와 함께 문의하세요:

1. 오류 메시지
2. 로그 파일 (logs/ 디렉토리)
3. 시스템 환경 정보
4. 재현 단계

**개발팀**: SPsystems 연구소 개발팀
**문의**: GitHub Issues 또는 내부 문의 채널
