# 🎯 **멀티 분석 도구 웹앱**

## 📊 **기능 소개**

다양한 분석 도구와 유틸리티를 하나의 웹앱에서 제공하는 통합 플랫폼입니다.

### 🛠️ **주요 기능**

1. **📈 3D 선형성 평가** - 3차원 데이터의 선형성 분석
2. **🚀 속도 및 가속도 분석** - 운동 데이터 분석 도구
3. **📊 프로젝트 BOM 분석** - 엑셀 기반 프로젝트 분석
4. **🚂 수륙양용 기차 프로젝트** - 혁신적 교통수단 개발 계획
5. **📅 프로젝트 진행 간트차트** - 엑셀 기반 프로젝트 관리
6. **🤖 로봇 자율주행 시뮬레이션** - 2가지 버전 제공
7. **⚙️ 모터 용량 계산** - 모터 사양 계산 도구
8. **🎮 오목 게임** - AI와 대전하는 오목 게임
9. **💬 게시판** - 간단한 커뮤니티 기능

## 🚀 **로컬 실행 방법**

### 1. 레포지토리 클론
```bash
git clone [repository-url]
cd blank-app-1
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 앱 실행
```bash
streamlit run streamlit_app.py
```

## 🌐 **라이브 데모**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](your-app-url)

## 🚀 **배포 방법**

### Streamlit Cloud
```bash
# GitHub에 푸시 후 Streamlit Cloud에서 자동 배포
git push origin main
```

### Docker
```bash
# Docker 이미지 빌드 및 실행
docker build -t spsystems-analysis-tool .
docker run -p 8501:8501 spsystems-analysis-tool
```

### Docker Compose
```bash
# 전체 스택 실행
docker-compose up -d
```

자세한 배포 가이드는 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)를 참조하세요.

## 📋 **시스템 요구사항**

- Python 3.7+
- Streamlit 1.28.0+
- 기타 패키지는 requirements.txt 참조

## 🔧 **주요 업데이트**

### v2.1.0 성능 최적화 (2025.06.15)
- ✅ 성능 모니터링 시스템 추가
- ✅ Docker 및 Docker Compose 지원
- ✅ CI/CD 파이프라인 구축
- ✅ 에러 처리 및 로깅 시스템 강화
- ✅ 캐싱 및 메모리 최적화

### 간트차트 기능 개선 (2025.06.10)
- ✅ 엑셀 입력 순서대로 차트 표시
- ✅ 바 크기 1/3로 축소하여 가독성 향상
- ✅ 실시간 진행률 업데이트 기능

## 📝 **사용 방법**

1. **간트차트**: 엑셀 파일 업로드 → 진행률 업데이트 → 프로젝트 관리
2. **분석 도구**: 데이터 입력 → 분석 실행 → 결과 확인
3. **게임**: 즉시 플레이 가능
4. **시뮬레이션**: 파라미터 설정 → 시뮬레이션 실행

## 🛠️ **기술 스택**

- **Frontend**: Streamlit
- **Data Visualization**: Plotly, Matplotlib
- **Data Processing**: Pandas, NumPy
- **ML/Analysis**: Scikit-learn
- **File Processing**: OpenPyXL, XlsxWriter

## 👥 **개발팀**

**SPsystems 연구소 개발팀**에서 개발 및 유지보수하고 있습니다.

## 🎨 **새로운 기능**

### 🚀 성능 최적화
- **매모리 사용량 모니터링**: 실시간 리소스 사용량 확인
- **지능형 캐싱**: 데이터 로딩 속도 향상
- **에러 바운드리**: 강화된 예외 처리

### 🔐 배포 옵션
- **Docker 지원**: 컴테이너 기반 배포
- **CI/CD**: GitHub Actions 자동 배포
- **환경 변수 관리**: 설정 파일 분리

### 📊 고급 분석
- **통계 기반 결과**: 데이터 기반 인사이트
- **인터랙티브 차트**: Plotly 기반 동적 시각화
- **대용량 데이터 처리**: 최적화된 메모리 사용

## 📧 **문의사항**

버그 리포트나 기능 요청은 Issues에 등록해주세요.
