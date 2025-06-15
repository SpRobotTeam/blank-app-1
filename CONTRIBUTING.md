# 🤝 기여 가이드 (Contributing Guide)

**SPsystems 다기능 분석 도구**에 기여해주셔서 감사합니다! 이 문서는 효과적인 협업을 위한 가이드라인을 제공합니다.

## 📋 목차

- [🚀 빠른 시작](#-빠른-시작)
- [🔄 개발 워크플로우](#-개발-워크플로우)
- [📝 코드 스타일](#-코드-스타일)
- [🧪 테스트](#-테스트)
- [📖 문서화](#-문서화)
- [🐛 버그 리포트](#-버그-리포트)
- [✨ 기능 제안](#-기능-제안)
- [📋 Pull Request 가이드](#-pull-request-가이드)
- [🏷️ 릴리스 프로세스](#️-릴리스-프로세스)

## 🚀 빠른 시작

### 1. 개발 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/spsystems/multi-analysis-tool.git
cd multi-analysis-tool

# 2. 개발 환경 초기화
make init

# 3. 개발 서버 실행
make dev
```

### 2. 필수 도구 설치 확인

```bash
# 개발 도구들이 제대로 설치되었는지 확인
make quality
```

## 🔄 개발 워크플로우

### Git Flow 브랜치 전략

```
main (프로덕션)
  ├── develop (개발)
  ├── feature/기능명 (새 기능)
  ├── fix/버그명 (버그 수정)
  ├── hotfix/긴급수정 (긴급 수정)
  └── release/버전 (릴리스 준비)
```

### 새 기능 개발 프로세스

```bash
# 1. develop 브랜치에서 시작
git checkout develop
git pull origin develop

# 2. 기능 브랜치 생성
git checkout -b feature/새로운-분석-도구

# 3. 개발 작업
# ... 코딩 ...

# 4. 테스트 및 품질 검사
make test
make quality

# 5. 커밋 (Conventional Commits 사용)
git add .
git commit -m "feat: 새로운 3D 분석 도구 추가"

# 6. 푸시 및 PR 생성
git push origin feature/새로운-분석-도구
# GitHub에서 develop으로 PR 생성
```

## 📝 코드 스타일

### 1. Python 코드 스타일

- **PEP 8** 준수
- **Black** 포맷터 사용 (88자 줄 길이)
- **isort**로 import 정렬
- **Type hints** 권장

```python
from typing import List, Optional, Dict
import pandas as pd

def analyze_data(
    data: pd.DataFrame, 
    columns: List[str],
    threshold: Optional[float] = None
) -> Dict[str, float]:
    """데이터 분석 함수
    
    Args:
        data: 분석할 데이터프레임
        columns: 분석할 컬럼 목록
        threshold: 임계값 (선택사항)
        
    Returns:
        분석 결과 딕셔너리
    """
    # 구현 내용
    pass
```

### 2. 자동 포맷팅

```bash
# 코드 포맷팅 실행
make format

# 포맷팅 확인 (변경하지 않음)
make format-check
```

### 3. 커밋 메시지 규칙

**Conventional Commits** 형식 사용:

```
<타입>(<범위>): <설명>

<본문>

<푸터>
```

**타입 종류:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드 프로세스, 패키지 관리

**예시:**
```bash
feat(analysis): 3D 데이터 시각화 기능 추가

사용자가 3차원 데이터를 대화형으로 탐색할 수 있는
Plotly 기반 시각화 도구를 추가했습니다.

- 회전, 확대/축소 지원
- 색상 맵핑 옵션
- 데이터 포인트 라벨링

Closes #123
```

## 🧪 테스트

### 1. 테스트 작성 원칙

- **단위 테스트**: 개별 함수/클래스 테스트
- **통합 테스트**: 컴포넌트 간 상호작용 테스트
- **E2E 테스트**: 전체 사용자 플로우 테스트

### 2. 테스트 실행

```bash
# 전체 테스트 실행
make test

# 커버리지 포함 테스트
make test-cov

# 특정 테스트 파일 실행
python -m pytest tests/test_analysis.py -v
```

### 3. 테스트 작성 예시

```python
import pytest
import pandas as pd
from apps.analysis import DataAnalyzer

class TestDataAnalyzer:
    """데이터 분석기 테스트"""
    
    @pytest.fixture
    def sample_data(self):
        """테스트용 샘플 데이터"""
        return pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 6, 8, 10]
        })
    
    def test_linear_analysis(self, sample_data):
        """선형성 분석 테스트"""
        analyzer = DataAnalyzer()
        result = analyzer.analyze_linearity(sample_data)
        
        assert result['correlation'] > 0.9
        assert result['r_squared'] > 0.9
    
    def test_invalid_data_handling(self):
        """잘못된 데이터 처리 테스트"""
        analyzer = DataAnalyzer()
        
        with pytest.raises(ValueError):
            analyzer.analyze_linearity(pd.DataFrame())
```

## 📖 문서화

### 1. 코드 문서화

- **Docstring**: Google 스타일 사용
- **README**: 사용법과 예시 포함
- **API 문서**: 자동 생성 도구 활용

### 2. 문서 업데이트

새로운 기능을 추가할 때 다음 문서들을 업데이트해주세요:

- `README.md`: 기능 소개 및 사용법
- `VERSIONING_GUIDE.md`: 버전 관리 관련
- 코드 내 docstring
- 필요시 별도 가이드 문서

## 🐛 버그 리포트

버그를 발견하셨나요? 다음 템플릿을 사용해 이슈를 등록해주세요:

### 버그 리포트 템플릿

```markdown
## 🐛 버그 설명
간단하고 명확한 버그 설명

## 🔄 재현 단계
1. '...'로 이동
2. '...'를 클릭
3. '...'까지 스크롤
4. 오류 발생

## 🎯 예상 동작
무엇이 일어나야 하는지 설명

## 📱 환경 정보
- OS: [예: Windows 11]
- Browser: [예: Chrome 91.0]
- Python: [예: 3.9.7]
- 버전: [예: v2.1.0]

## 📷 스크린샷
가능하다면 스크린샷 첨부

## 📝 추가 정보
기타 관련 정보
```

## ✨ 기능 제안

새로운 기능을 제안하고 싶으신가요?

### 기능 제안 템플릿

```markdown
## 🚀 기능 설명
제안하는 기능에 대한 명확한 설명

## 💡 동기
이 기능이 왜 필요한지 설명

## 📝 상세 설계
구체적인 구현 방안 또는 아이디어

## 🎯 대안
고려해본 다른 해결책들

## 📋 체크리스트
- [ ] 기존 기능과의 호환성 확인
- [ ] 성능 영향 검토
- [ ] 문서화 계획
```

## 📋 Pull Request 가이드

### 1. PR 체크리스트

PR을 생성하기 전에 다음을 확인해주세요:

- [ ] 코드가 스타일 가이드를 준수하나요? (`make quality`)
- [ ] 모든 테스트가 통과하나요? (`make test`)
- [ ] 새로운 기능에 대한 테스트를 추가했나요?
- [ ] 문서를 업데이트했나요?
- [ ] 커밋 메시지가 컨벤션을 따르나요?

### 2. PR 템플릿

```markdown
## 📋 변경사항 요약
이 PR에서 변경된 내용을 간단히 설명

## 🎯 변경 이유
왜 이 변경이 필요한지 설명

## 🧪 테스트
어떻게 테스트했는지 설명

## 📷 스크린샷 (UI 변경시)
필요시 스크린샷 첨부

## 📝 체크리스트
- [ ] 코드 리뷰 준비 완료
- [ ] 테스트 통과
- [ ] 문서 업데이트
- [ ] 충돌 해결
```

### 3. 코드 리뷰 프로세스

- **최소 1명**의 승인 필요
- **자동 테스트** 통과 필수
- **충돌 해결** 후 머지

## 🏷️ 릴리스 프로세스

### 1. 자동 릴리스 (권장)

```bash
# 패치 버전 (버그 수정)
make deploy-patch

# 마이너 버전 (새 기능)
make deploy-minor

# 메이저 버전 (호환성 변경)
make deploy-major
```

### 2. 수동 릴리스

```bash
# 1. 릴리스 브랜치 생성
git checkout develop
git checkout -b release/v2.2.0

# 2. 버전 업데이트
python scripts/update_version.py --type minor --changelog "새 기능들" --tag

# 3. 테스트 및 품질 검사
make ci

# 4. main으로 머지
git checkout main
git merge release/v2.2.0
git push origin main
git push origin v2.2.0

# 5. develop에도 머지
git checkout develop
git merge release/v2.2.0
git push origin develop
```

## 🎉 기여해주셔서 감사합니다!

여러분의 기여가 **SPsystems 다기능 분석 도구**를 더욱 발전시킵니다!

### 📞 연락처

- **Issues**: [GitHub Issues](https://github.com/spsystems/multi-analysis-tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/spsystems/multi-analysis-tool/discussions)
- **Email**: spsystems.dev@example.com

### 🏆 기여자 인정

모든 기여자는 README.md의 Contributors 섹션에 추가됩니다!

---

**개발팀**: SPsystems 연구소  
**문서 버전**: 1.0.0  
**최종 업데이트**: 2025-06-15
