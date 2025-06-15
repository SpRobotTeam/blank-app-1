#!/bin/bash

# 🚀 SPsystems 웹앱 통합 배포 스크립트
# 사용법: ./deploy.sh [patch|minor|major] [메시지]

set -e

# 색상 설정
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 파라미터 확인
VERSION_TYPE=${1:-patch}
COMMIT_MESSAGE=${2:-"자동 배포"}

# 유효한 버전 타입 확인
if [[ ! "$VERSION_TYPE" =~ ^(patch|minor|major)$ ]]; then
    log_error "잘못된 버전 타입: $VERSION_TYPE"
    echo "사용법: ./deploy.sh [patch|minor|major] [메시지]"
    exit 1
fi

log_info "SPsystems 웹앱 배포 시작"
log_info "버전 타입: $VERSION_TYPE"
log_info "커밋 메시지: $COMMIT_MESSAGE"

# 1. Git 상태 확인
log_info "Git 상태 확인 중..."
if [[ -n $(git status --porcelain) ]]; then
    log_warning "커밋되지 않은 변경사항이 있습니다:"
    git status --short
    read -p "계속 진행하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "배포 취소됨"
        exit 1
    fi
fi

# 2. 현재 브랜치 확인
CURRENT_BRANCH=$(git branch --show-current)
log_info "현재 브랜치: $CURRENT_BRANCH"

# 3. 테스트 실행 (선택사항)
if [ -f "tests/test_main.py" ] || [ -d "tests" ]; then
    log_info "테스트 실행 중..."
    python -m pytest tests/ -v || {
        log_error "테스트 실패! 배포를 중단합니다."
        exit 1
    }
    log_success "모든 테스트 통과"
fi

# 4. 린트 체크 (선택사항)
if command -v flake8 &> /dev/null; then
    log_info "코드 품질 검사 중..."
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || {
        log_warning "린트 경고가 있지만 계속 진행합니다."
    }
fi

# 5. 버전 업데이트
log_info "버전 업데이트 중..."
python scripts/update_version.py --type $VERSION_TYPE --changelog "$COMMIT_MESSAGE" --tag

# 새 버전 가져오기
NEW_VERSION=$(python scripts/update_version.py --current | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
log_success "버전 업데이트 완료: v$NEW_VERSION"

# 6. 변경사항 커밋
log_info "변경사항 커밋 중..."
git add .
git commit -m "chore: bump version to $NEW_VERSION - $COMMIT_MESSAGE"

# 7. 태그 푸시
log_info "태그 푸시 중..."
git push origin "v$NEW_VERSION"

# 8. 메인 브랜치에 푸시
log_info "브랜치 푸시 중..."
git push origin $CURRENT_BRANCH

# 9. Docker 이미지 빌드 (선택사항)
if [ -f "Dockerfile" ]; then
    log_info "Docker 이미지 빌드 중..."
    docker build -t "spsystems-analysis-tool:$NEW_VERSION" .
    docker tag "spsystems-analysis-tool:$NEW_VERSION" "spsystems-analysis-tool:latest"
    log_success "Docker 이미지 빌드 완료"
fi

# 10. 배포 완료 알림
log_success "🎉 배포 완료!"
echo ""
echo "📋 배포 정보:"
echo "- 버전: v$NEW_VERSION"
echo "- 브랜치: $CURRENT_BRANCH"
echo "- 커밋 메시지: $COMMIT_MESSAGE"
echo "- 배포 시간: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "🔗 다음 단계:"
echo "1. GitHub에서 릴리스 노트 작성"
echo "2. Streamlit Cloud 자동 배포 확인"
echo "3. 운영 환경 동작 확인"

# 11. 자동으로 브라우저에서 GitHub 릴리스 페이지 열기 (선택사항)
if command -v xdg-open &> /dev/null; then
    REPO_URL=$(git config --get remote.origin.url | sed 's/\.git$//')
    if [[ $REPO_URL == *"github.com"* ]]; then
        xdg-open "$REPO_URL/releases/new?tag=v$NEW_VERSION" 2>/dev/null &
        log_info "GitHub 릴리스 페이지가 열렸습니다."
    fi
fi

log_success "스크립트 실행 완료!"
