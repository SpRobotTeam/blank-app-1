# 🚀 SPsystems 다기능 분석 도구 - Makefile
# 개발 환경 자동화 도구

.PHONY: help install dev test lint format clean docker run version deploy

# 기본 설정
PYTHON := python
PIP := pip
STREAMLIT := streamlit
DOCKER := docker

# 색상 설정
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# 도움말 표시
help: ## 📋 사용 가능한 명령어 목록 표시
	@echo "$(BLUE)🚀 SPsystems 다기능 분석 도구 - 개발 도구$(NC)"
	@echo ""
	@echo "$(GREEN)📦 설치 및 환경 설정:$(NC)"
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z_-]+:.*?##.*install/ { printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)🛠️ 개발 도구:$(NC)"
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z_-]+:.*?##.*dev/ { printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)🧪 테스트 및 품질:$(NC)"
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z_-]+:.*?##.*test|quality/ { printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)🐳 Docker:$(NC)"
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z_-]+:.*?##.*docker/ { printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)🚀 배포:$(NC)"
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z_-]+:.*?##.*deploy/ { printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# 설치 및 환경 설정
install: ## 📦 install - 의존성 패키지 설치
	@echo "$(BLUE)📦 의존성 패키지 설치 중...$(NC)"
	$(PIP) install -r requirements.txt

install-dev: ## 📦 install - 개발 도구 포함 전체 설치
	@echo "$(BLUE)📦 개발 환경 설치 중...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest black isort flake8 bandit mypy pytest-cov
	@echo "$(GREEN)✅ 개발 환경 설치 완료!$(NC)"

# 개발 도구
dev: ## 🛠️ dev - 개발 모드로 앱 실행
	@echo "$(BLUE)🚀 개발 모드로 Streamlit 앱 실행...$(NC)"
	$(STREAMLIT) run streamlit_app.py --server.runOnSave true

run: ## 🛠️ dev - 일반 모드로 앱 실행
	@echo "$(BLUE)🚀 Streamlit 앱 실행...$(NC)"
	$(STREAMLIT) run streamlit_app.py

# 테스트 및 품질 관리
test: ## 🧪 test - 모든 테스트 실행
	@echo "$(BLUE)🧪 테스트 실행 중...$(NC)"
	$(PYTHON) -m pytest tests/ -v

test-cov: ## 🧪 test - 코드 커버리지 포함 테스트
	@echo "$(BLUE)🧪 커버리지 테스트 실행 중...$(NC)"
	$(PYTHON) -m pytest tests/ --cov=. --cov-report=html --cov-report=term

lint: ## 🔍 quality - 코드 린트 검사
	@echo "$(BLUE)🔍 코드 린트 검사 중...$(NC)"
	flake8 .
	@echo "$(GREEN)✅ 린트 검사 완료!$(NC)"

format: ## 🎨 quality - 코드 포맷팅
	@echo "$(BLUE)🎨 코드 포맷팅 중...$(NC)"
	black .
	isort .
	@echo "$(GREEN)✅ 코드 포맷팅 완료!$(NC)"

format-check: ## 🎨 quality - 코드 포맷팅 확인 (변경하지 않음)
	@echo "$(BLUE)🎨 코드 포맷팅 확인 중...$(NC)"
	black --check --diff .
	isort --check-only --diff .

security: ## 🔒 quality - 보안 취약점 검사
	@echo "$(BLUE)🔒 보안 검사 중...$(NC)"
	bandit -r . -f json -o security-report.json
	@echo "$(GREEN)✅ 보안 검사 완료! (결과: security-report.json)$(NC)"

type-check: ## 🔍 quality - 타입 체킹
	@echo "$(BLUE)🔍 타입 체킹 중...$(NC)"
	mypy . --ignore-missing-imports

quality: lint format-check security type-check ## 🔍 quality - 전체 코드 품질 검사

# Docker 관련
docker-build: ## 🐳 docker - Docker 이미지 빌드
	@echo "$(BLUE)🐳 Docker 이미지 빌드 중...$(NC)"
	$(DOCKER) build -t spsystems-analysis-tool:latest .
	@echo "$(GREEN)✅ Docker 이미지 빌드 완료!$(NC)"

docker-run: ## 🐳 docker - Docker 컨테이너 실행
	@echo "$(BLUE)🐳 Docker 컨테이너 실행 중...$(NC)"
	$(DOCKER) run -p 8501:8501 spsystems-analysis-tool:latest

docker-compose-up: ## 🐳 docker - Docker Compose로 전체 스택 실행
	@echo "$(BLUE)🐳 Docker Compose 실행 중...$(NC)"
	docker-compose up -d

docker-compose-down: ## 🐳 docker - Docker Compose 중지
	@echo "$(BLUE)🐳 Docker Compose 중지 중...$(NC)"
	docker-compose down

# 버전 관리
version: ## 📝 deploy - 현재 버전 확인
	@echo "$(BLUE)📝 현재 버전:$(NC)"
	@$(PYTHON) scripts/update_version.py --current

version-patch: ## 📝 deploy - 패치 버전 업데이트
	@echo "$(BLUE)📝 패치 버전 업데이트 중...$(NC)"
	$(PYTHON) scripts/update_version.py --type patch --changelog "버그 수정 및 개선"

version-minor: ## 📝 deploy - 마이너 버전 업데이트
	@echo "$(BLUE)📝 마이너 버전 업데이트 중...$(NC)"
	$(PYTHON) scripts/update_version.py --type minor --changelog "새 기능 추가"

version-major: ## 📝 deploy - 메이저 버전 업데이트
	@echo "$(BLUE)📝 메이저 버전 업데이트 중...$(NC)"
	$(PYTHON) scripts/update_version.py --type major --changelog "주요 변경사항"

# 배포
deploy-patch: test quality ## 🚀 deploy - 패치 버전 배포
	@echo "$(BLUE)🚀 패치 버전 배포 중...$(NC)"
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh patch "패치 배포"

deploy-minor: test quality ## 🚀 deploy - 마이너 버전 배포
	@echo "$(BLUE)🚀 마이너 버전 배포 중...$(NC)"
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh minor "마이너 버전 배포"

deploy-major: test quality ## 🚀 deploy - 메이저 버전 배포
	@echo "$(BLUE)🚀 메이저 버전 배포 중...$(NC)"
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh major "메이저 버전 배포"

# 유지보수
clean: ## 🧹 dev - 임시 파일 정리
	@echo "$(BLUE)🧹 임시 파일 정리 중...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@echo "$(GREEN)✅ 정리 완료!$(NC)"

logs: ## 📊 dev - 로그 파일 확인
	@echo "$(BLUE)📊 최근 로그:$(NC)"
	@if [ -d "logs" ]; then \
		find logs -name "*.log" -type f -exec tail -20 {} \; ; \
	else \
		echo "$(YELLOW)⚠️ 로그 디렉토리가 없습니다.$(NC)"; \
	fi

status: ## 📊 dev - 프로젝트 상태 확인
	@echo "$(BLUE)📊 프로젝트 상태:$(NC)"
	@echo "Git 상태:"
	@git status --short
	@echo ""
	@echo "현재 브랜치: $(shell git branch --show-current)"
	@echo "최근 커밃: $(shell git log -1 --pretty=format:'%h - %s (%an, %ar)')"
	@echo ""
	@$(PYTHON) scripts/update_version.py --current

# 개발 환경 초기화
init: install-dev ## 🚀 install - 프로젝트 초기 설정
	@echo "$(BLUE)🚀 프로젝트 초기 설정 중...$(NC)"
	@if [ ! -f ".env" ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✅ .env 파일 생성 완료!$(NC)"; \
	fi
	@echo "$(GREEN)🎉 프로젝트 초기 설정 완료!$(NC)"
	@echo "$(YELLOW)💡 이제 'make dev' 명령으로 개발을 시작하세요!$(NC)"

# 의존성 업데이트
update-deps: ## 📦 install - 의존성 패키지 업데이트
	@echo "$(BLUE)📦 의존성 패키지 업데이트 중...$(NC)"
	$(PIP) list --outdated
	$(PIP) install --upgrade -r requirements.txt

# 전체 CI 시뮬레이션
ci: clean install-dev quality test ## 🔄 test - CI 파이프라인 시뮬레이션
	@echo "$(GREEN)🎉 CI 파이프라인 시뮬레이션 완료!$(NC)"

# 기본 타겟
.DEFAULT_GOAL := help
