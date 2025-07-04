# Week 1 연구노트: 프로젝트 개요 및 연구 착수 목적 정리

## 1. 실험/연구 배경 및 목적
SHI 자동 용접로봇 B-LINE 컨셉 프로젝트는 선박용 소부재의 용접 공정을 자동화하여 무인 생산체계를 구축하는 것을 핵심 목표로 한다. 현재 수작업 중심의 용접 공정은 품질 편차, 인력 의존도, 안전성 등의 문제가 존재하며, 이를 극복하기 위한 자동화 시스템 도입이 절실하다. 본 연구노트는 해당 프로젝트의 착수단계에서 전체 시스템 개요를 정리하고, 연구 수행의 방향성과 핵심 검토 항목을 설정하는 데 목적이 있다.

## 2. 실험/연구 개요
| 항목 | 내용 |
|------|------|
| 연구 주제 | 자동 용접로봇 기반 B-LINE 무인 생산 공정 구축 |
| 수행 기간 | 2025년 1월 ~ 2025년 12월 |
| 연구 기관 | (주)에스피시스템스 |
| 주요 기술 분야 | 자동화 설비 설계, 갠트리 로봇 시스템, 실시간 제어, 3D 계측 |
| Week 1 주요 목표 | 시스템 아키텍처 구성, 주요 기술 항목 정의, 전체 일정 로드맵 도출 |

## 3. 실험/연구 절차 및 방법
- 기존 유사 프로젝트 및 선행 기술 문헌 분석 (5건)
- B-LINE 시스템 요구사항 도출 (기능별 요구 조건 정의)
- 시스템 구성 요소 기능분해 (갠트리, 용접, 계측, 제어 시스템)
- 시스템 블록 다이어그램 및 데이터 흐름 작성
- 관련 법규 및 안전기준(로봇, 전기, 통신) 검토

## 4. 사용 장비 및 자재 (Week 1 해당 없음)
※ 본 주차는 설계 검토 및 이론 정리 중심으로 실물 장비/자재 사용 없음.

## 5. 실험/연구 결과
### 5-1. 시스템 구성 요소 정의
| 구성 모듈 | 주요 기능 |
|------------|------------|
| 갠트리 로봇 | XYZR 4축 제어, 고속 위치 이송, 프레임 구조 지지체 역할 |
| 용접 로봇 | 정밀 용접 작업 수행 (CO2, MAG 등), 실시간 용접 궤적 제어 |
| 3D 계측 시스템 | 글로벌/로컬 정밀 계측, 실시간 좌표 보정 및 정렬 매핑 |
| 통합 제어 시스템 | 경로 최적화, 작업 순서 제어, 데이터 기록 및 품질 추적 |

### 5-2. 시스템 구성 비중 예측
```chart
bar
    갠트리 로봇       : 30
    용접 로봇         : 25
    계측 시스템       : 20
    제어 및 스케줄링  : 25
```

### 5-3. 시스템 운영 시나리오 요약
1. 작업 공정 시작 → 자재 투입 감지
2. 3D 스캐너로 부품 위치 계측
3. 계측값 기반 로봇 용접 경로 자동 보정
4. 갠트리 로봇을 통해 각 위치 이동
5. 용접 완료 후 품질 측정 및 기록

## 6. 해석 및 고찰
이번 주차는 프로젝트 추진의 기본 전제 및 방향성을 정리하는 데 초점을 두었다. 갠트리 구조와 로봇 기능 간 연계성을 확보해야 하며, 각 구성 요소 간 인터페이스 조건과 사양 정합성 확보가 추후 기술 단계에서 매우 중요할 것으로 예상된다. 초기 개념설계 단계에서 전체 공정 흐름을 가시화함으로써 기술 요소 간 종속관계를 명확히 정리할 수 있었다.

## 7. 결론 및 향후 계획
- 전체 시스템 구조 정의 완료
- 구성 요소별 기능 분해 및 주요 사양 방향 정리 완료
- 2주차에는 갠트리 구조물에 대한 상세 사양 정의 및 동작 범위 정리를 진행할 예정이며, 설계기준(하중, 강성, 반복정밀도) 설정이 핵심이 될 것임

## 8. 참고자료
- SHI 2023년 자동용접 B-LINE 기획안
- (주)에스피시스템스 사양서_초안_v0.1.pdf
- 한국로봇산업진흥원 “스마트 제조를 위한 로봇활용 가이드북(2022)”
- ISO 9283: Industrial Robots – Performance Criteria and Related Test Methods

## 9. 서명
| 작성자 | 검토자 |
|--------|--------|
| OOO   | OOO   |

