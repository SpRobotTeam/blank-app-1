# 🚀 SPsystems 웹앱 버전 관리 가이드

## 📋 버전 관리 전략

### 🔄 Git Flow 브랜치 구조
```
main (프로덕션)
  ├── develop (개발)
  ├── feature/* (기능 개발)
  ├── release/* (릴리스 준비)  
  └── hotfix/* (긴급 수정)
```

### 📝 버전 네이밍 규칙 (Semantic Versioning)
- **MAJOR.MINOR.PATCH** (예: 2.1.0)
- **MAJOR**: 호환성이 깨지는 변경사항
- **MINOR**: 하위 호환성을 유지하는 새 기능
- **PATCH**: 하위 호환성을 유지하는 버그 수정

## 🛠️ 실제 사용 방법

### 1. 일반적인 개발 워크플로우

#### 새 기능 개발
```bash
# 1. develop 브랜치에서 feature 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feature/새기능명

# 2. 개발 작업 수행
# ... 코딩 ...

# 3. 커밋 (Conventional Commits 사용)
git add .
git commit -m "feat: 3D 선형성 분석 알고리즘 개선"

# 4. 푸시 및 PR 생성
git push origin feature/새기능명
# GitHub에서 develop으로 PR 생성
```

#### 버그 수정
```bash
# 1. develop에서 버그 수정 브랜치 생성
git checkout -b fix/버그명

# 2. 수정 작업
git commit -m "fix: 간트차트 날짜 표시 오류 수정"

# 3. PR 생성 후 머지
```

### 2. 릴리스 과정

#### Step 1: 릴리스 브랜치 생성
```bash
git checkout develop
git checkout -b release/2.2.0
```

#### Step 2: 버전 업데이트 (자동화 스크립트 사용)
```bash
# 패치 버전 (버그 수정)
python scripts/update_version.py --type patch --changelog "버그 수정" "성능 개선"

# 마이너 버전 (새 기능)
python scripts/update_version.py --type minor --changelog "새 분석 도구 추가" "UI 개선" --tag

# 메이저 버전 (대대적 변경)
python scripts/update_version.py --type major --changelog "아키텍처 전면 개편" --tag
```

#### Step 3: 릴리스 완료
```bash
# 변경사항 커밋
git add .
git commit -m "chore: bump version to 2.2.0"

# main으로 머지
git checkout main
git merge release/2.2.0

# develop으로도 머지
git checkout develop  
git merge release/2.2.0

# 푸시
git push origin main
git push origin develop
git push origin v2.2.0  # 태그가 생성된 경우
```

### 3. 긴급 수정 (Hotfix)

```bash
# main에서 hotfix 브랜치 생성
git checkout main
git checkout -b hotfix/긴급수정

# 수정 작업
git commit -m "fix: 보안 취약점 긴급 수정"

# 버전 업데이트 (패치)
python scripts/update_version.py --type patch --changelog "보안 수정" --tag

# main과 develop에 머지
git checkout main
git merge hotfix/긴급수정
git checkout develop
git merge hotfix/긴급수정

git push origin main
git push origin develop
```

## 📊 커밋 메시지 규칙 (Conventional Commits)

### 형식
```
<타입>(<범위>): <설명>

<본문>

<푸터>
```

### 타입 종류
- **feat**: 새 기능
- **fix**: 버그 수정  
- **docs**: 문서 변경
- **style**: 코드 포맷팅
- **refactor**: 리팩토링
- **test**: 테스트 추가/수정
- **chore**: 빌드 프로세스, 패키지 매니저 설정

### 예시
```bash
feat(analysis): 3D 데이터 시각화 기능 추가
fix(gantt): 엑셀 업로드 시 인코딩 오류 수정
docs: API 문서 업데이트
refactor(ui): 컴포넌트 구조 개선
```

## 🏷️ 태그 관리

### 자동 태그 생성
```bash
# 버전 업데이트와 함께 태그 생성
python scripts/update_version.py --type minor --tag --changelog "새 기능들"
```

### 수동 태그 생성
```bash
git tag -a v2.1.1 -m "긴급 보안 수정"
git push origin v2.1.1
```

## 🔄 자동화된 CI/CD 워크플로우

### GitHub Actions 설정 (.github/workflows/release.yml)
```yaml
name: Release Workflow
on:
  push:
    tags: ['v*']
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Production
        run: |
          # 배포 스크립트 실행
          echo "Deploying version ${{ github.ref_name }}"
```

## 📈 버전 관리 모니터링

### 현재 버전 확인
```bash
python scripts/update_version.py --current
```

### 변경 이력 추적
- `package.json`의 changelog 섹션 확인
- Git 태그를 통한 릴리스 이력
- GitHub Releases 페이지 활용

## 🎯 베스트 프랙티스

### 1. 정기적인 릴리스 주기
- **주간 패치 릴리스**: 버그 수정
- **월간 마이너 릴리스**: 새 기능
- **분기별 메이저 검토**: 대규모 변경

### 2. 테스트 전략
```bash
# 릴리스 전 테스트 실행
python -m pytest tests/
python scripts/lint_check.py
```

### 3. 롤백 계획
```bash
# 이전 버전으로 롤백
git checkout v2.1.0
# 또는 Docker 이미지 롤백
docker run spsystems-analysis-tool:2.1.0
```

## 🚀 다음 단계 추천

1. **GitHub Actions CI/CD 파이프라인 구축**
2. **자동화된 테스트 도입**  
3. **Code Review 프로세스 정립**
4. **변경 이력 문서화 자동화**
5. **성능 모니터링 및 에러 트래킹**

---

**개발팀**: SPsystems 연구소  
**문서 버전**: 1.0.0  
**최종 업데이트**: 2025-06-15
