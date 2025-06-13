# GANTY-LODER 프로젝트 분석 도구 사용 가이드

## 🚀 실행 방법

### 1. 터미널에서 프로젝트 폴더로 이동
```bash
cd "C:\Users\user\Desktop\workfold\소부재\ABB_TSU_블스아이\blank-app-1"
```

### 2. Streamlit 앱 실행
```bash
streamlit run streamlit_app.py
```

### 3. 웹브라우저에서 접속
- 자동으로 브라우저가 열림 (일반적으로 http://localhost:8501)
- 만약 열리지 않으면 터미널에 표시된 URL로 접속

## 📊 GANTY-LODER 분석 도구 사용법

### 1. 사이드바에서 "📈 프로젝트 분석" 선택
### 2. "GANTY-LODER 프로젝트 분석" 선택
### 3. 6개 탭에서 다양한 분석 결과 확인:
   - **📊 프로젝트 개요**: 전체 프로젝트 요약 정보
   - **🔧 기계 어셈블리**: 어셈블리별 상세 분석
   - **💰 전체 구성**: 프로젝트 구성요소별 분석
   - **💎 고가 품목**: 주요 고가 부품 분석
   - **🛠️ 서비스 내역**: 설치/시운전 서비스 분석
   - **📈 분석 차트**: 종합 시각화 분석

## 📁 포함된 데이터 파일들
- `data/project_overview.csv`: 프로젝트 개요
- `data/assembly_data.csv`: 기계 어셈블리 데이터
- `data/project_composition.csv`: 전체 프로젝트 구성
- `data/expensive_items.csv`: 고가 품목 리스트
- `data/service_details.csv`: 서비스 상세 내역

## 🎯 주요 분석 결과
- **총 프로젝트 금액**: 9.8억원
- **제작 vs 구매 비율**: 30.6% vs 69.4%
- **핵심 고가 품목**: ABB 로봇 (1.1억), LINCOLN 용접기 (3,480만원)
- **프로젝트 성격**: 턴키 프로젝트 (완전 솔루션)

## 🔧 문제 해결
만약 실행 중 오류가 발생하면:
1. 패키지 설치 확인: `pip install -r requirements.txt`
2. Python 버전 확인: Python 3.8 이상 필요
3. 데이터 파일 경로 확인: data 폴더 내 CSV 파일들 존재 여부
