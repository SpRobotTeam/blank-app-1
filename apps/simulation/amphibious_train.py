import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, info_message, sidebar_info

def display_amphibious_train_project():
    """
    수륙 양용 기차 개발 프로젝트 정보
    혁신적인 수륙 양용 교통수단의 개발 계획과 기술적 세부사항을 제공합니다.
    """
    # 도구 헤더 적용
    tool_header(
        "수륙 양용 기차 개발 프로젝트", 
        "혁신적인 수륙 양용 교통수단의 개발 계획, 기술적 도전과제, 그리고 미래 전망을 종합적으로 다룹니다. 차세대 교통 혁신의 비전을 확인해보세요."
    )

    # 사이드바에 프로젝트 정보 표시
    with st.sidebar:
        sidebar_info(version="2.0", update_date="2025-06-10")
        
        st.markdown("### 📊 프로젝트 현황")
        st.progress(0.25, text="25% 완료 (기초 연구 단계)")
        
        st.markdown("### 💰 예산 현황")
        total_budget = 38  # 억 달러
        spent_budget = 5   # 억 달러 (가정)
        remaining_budget = total_budget - spent_budget
        
        budget_data = pd.DataFrame({
            'Category': ['사용된 예산', '남은 예산'],
            'Amount': [spent_budget, remaining_budget]
        })
        
        fig_budget = px.pie(budget_data, values='Amount', names='Category', 
                           color_discrete_sequence=['#ff7f7f', '#90EE90'])
        fig_budget.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig_budget, use_container_width=True)
        
        st.metric("총 예산", f"${total_budget}억", f"-${spent_budget}억")

    # 탭으로 메뉴 생성
    tab_names = [
        "📋 프로젝트 개요",
        "🎯 프로젝트 목표", 
        "⚙️ 핵심 기술",
        "📅 개발 계획",
        "🛣️ 경로 및 활용",
        "🔧 기술적 도전",
        "🔨 유지보수 계획",
        "⚖️ 법적 준수사항",
        "📈 운영 최적화"
    ]
    
    tabs = st.tabs(tab_names)

    # 각 탭의 내용 정의
    with tabs[0]:
        display_project_overview()

    with tabs[1]:
        display_project_goals()

    with tabs[2]:
        display_core_technology()

    with tabs[3]:
        display_development_plan()

    with tabs[4]:
        display_routes_and_usage()

    with tabs[5]:
        display_technical_challenges()

    with tabs[6]:
        display_maintenance_plan()

    with tabs[7]:
        display_legal_compliance()

    with tabs[8]:
        display_operational_optimization()

def display_project_overview():
    """프로젝트 개요"""
    st.header("📋 프로젝트 개요")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🚄 수륙 양용 기차란?
        
        수륙 양용 기차는 육상 도로와 수상 경로를 자유롭게 이동할 수 있는 
        혁신적인 교통수단입니다. 기존 교통 인프라의 한계를 뛰어넘어 
        새로운 이동 패러다임을 제시합니다.
        
        ### 🌟 주요 특징
        - **양용 설계**: 육상과 수상을 자유롭게 이동
        - **친환경**: 하이브리드 동력 시스템 적용
        - **고효율**: 최적화된 에너지 소비
        - **안전성**: 첨단 안전 시스템 구비
        - **편의성**: 승객 중심의 설계
        """)
    
    with col2:
        # 주요 지표 표시
        st.markdown("### 📊 핵심 지표")
        st.metric("육상 최고 속도", "200+ km/h")
        st.metric("수상 최고 속도", "60 km/h")
        st.metric("전환 시간", "< 5초")
        st.metric("탄소 배출 감소", "50%+")
        st.metric("승객 정원", "300명")
    
    # 프로젝트 일정 시각화
    st.markdown("### 📅 프로젝트 일정")
    
    timeline_data = {
        'Phase': ['1단계: 기초 연구', '2단계: 실용화 연구', '3단계: 상업화 준비', '4단계: 상업 운영'],
        'Start': [2025, 2027, 2030, 2033],
        'Duration': [2, 3, 3, 2],
        'Budget': [3, 10, 25, 5]  # 억 달러
    }
    
    df_timeline = pd.DataFrame(timeline_data)
    df_timeline['End'] = df_timeline['Start'] + df_timeline['Duration']
    
    fig_timeline = px.timeline(
        df_timeline, 
        x_start='Start', 
        x_end='End', 
        y='Phase',
        color='Budget',
        color_continuous_scale='viridis',
        title='프로젝트 단계별 일정'
    )
    
    fig_timeline.update_layout(
        xaxis_title="연도",
        yaxis_title="개발 단계",
        height=400
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)

def display_project_goals():
    """프로젝트 목표"""
    st.header("🎯 프로젝트 목표")
    
    # 목표 카드 형태로 표시
    goals = [
        {
            "title": "🚄 수륙 양용 이동성",
            "description": "육상 도로와 수중 경로를 자유롭게 이동할 수 있는 수륙 양용 기차 개발",
            "details": [
                "도시 간 이동과 강, 호수, 해안선을 포함한 복합적인 운송 경로에서 활용",
                "기술 혁신을 통해 전환 과정의 속도와 신뢰성을 극대화",
                "육상-수상 통합 네트워크 구축"
            ]
        },
        {
            "title": "⚡ 고속 및 효율성",
            "description": "육상과 수상 환경에서 최적의 속도와 에너지 효율성 달성",
            "details": [
                "육상: 기존 고속철도 수준의 속도 유지",
                "수상: 평균 40-60km/h의 최적 속도 달성", 
                "하이브리드 동력 시스템으로 에너지 소비 최소화",
                "경량화 소재와 공기역학적 설계 적용"
            ]
        },
        {
            "title": "🌍 환경 친화적 설계",
            "description": "지속 가능한 교통수단으로서 환경 영향 최소화",
            "details": [
                "탄소 배출 50% 이상 감소",
                "친환경 연료 기술(전기, 수소) 채택",
                "소음 및 진동 억제 기술 적용",
                "수질 오염 방지 및 수중 생태계 보호"
            ]
        },
        {
            "title": "👥 승객 경험 최적화",
            "description": "안전하고 편리한 승객 경험 제공",
            "details": [
                "자동화된 안정화 시스템으로 안전 보장",
                "최적화된 내부 공간과 편의시설",
                "시각적 경험을 극대화하는 창문 및 좌석 배열",
                "긴급 상황 대응 비상 시스템 구비"
            ]
        },
        {
            "title": "💰 경제성 확보",
            "description": "지속 가능한 비즈니스 모델 구축",
            "details": [
                "모듈형 설계로 초기 개발 비용 절감",
                "유지보수 최적화로 운영 비용 절감",
                "다목적 활용 모델 개발",
                "투자 회수 기간 5년 내 목표"
            ]
        }
    ]
    
    for i, goal in enumerate(goals):
        with st.expander(f"{goal['title']}", expanded=(i==0)):
            st.markdown(f"**{goal['description']}**")
            st.markdown("**주요 내용:**")
            for detail in goal['details']:
                st.markdown(f"• {detail}")

def display_core_technology():
    """핵심 기술 요소"""
    st.header("⚙️ 핵심 기술 요소")
    
    # 기술 구성 요소 시각화
    tech_components = {
        'Component': ['전환 메커니즘', '부력 시스템', '추진 시스템', '제어 시스템', '안전 시스템'],
        'Complexity': [9, 8, 7, 8, 9],
        'Importance': [10, 9, 8, 9, 10],
        'Development_Status': [60, 40, 70, 50, 30]  # 개발 진행률 (%)
    }
    
    df_tech = pd.DataFrame(tech_components)
    
    fig_tech = px.scatter(
        df_tech, 
        x='Complexity', 
        y='Importance',
        size='Development_Status',
        color='Component',
        title='기술 구성 요소별 복잡도 vs 중요도',
        labels={'Complexity': '기술 복잡도', 'Importance': '중요도'}
    )
    
    fig_tech.update_layout(height=500)
    st.plotly_chart(fig_tech, use_container_width=True)
    
    # 기술별 상세 설명
    st.subheader("🔧 주요 기술 시스템")
    
    tech_details = {
        "🔄 전환 메커니즘": {
            "description": "수륙 모드 간 자동 전환 시스템",
            "features": [
                "가변 차체 시스템으로 바퀴/프로펠러 자동 전환",
                "고강도 경량 소재 사용으로 내구성 보장",
                "5초 이내 전환으로 즉각 대응 가능",
                "진동/소음 최소화 설계"
            ]
        },
        "🎈 부력 조정 시스템": {
            "description": "수중 주행을 위한 자동 부력 제어",
            "features": [
                "공기 주입식 부력 튜브 시스템",
                "운행 조건에 따른 자동 팽창/수축",
                "부력 센서를 통한 실시간 자세 제어",
                "지상 주행 시 완전 접이식 구조"
            ]
        },
        "⚡ 하이브리드 동력": {
            "description": "육상/수상 최적화 동력 시스템",
            "features": [
                "전기 모터 + 내연기관 하이브리드",
                "환경별 최적 동력원 자동 선택",
                "회생 제동으로 에너지 회수",
                "친환경 연료(수소, 전기) 사용"
            ]
        },
        "🧠 지능형 제어": {
            "description": "AI 기반 통합 제어 시스템",
            "features": [
                "실시간 환경 감지 및 적응",
                "예측 제어로 최적 경로 산출",
                "자동 안전 모드 전환",
                "원격 모니터링 및 진단"
            ]
        }
    }
    
    for tech_name, tech_info in tech_details.items():
        with st.expander(tech_name, expanded=False):
            st.markdown(f"**{tech_info['description']}**")
            st.markdown("**주요 특징:**")
            for feature in tech_info['features']:
                st.markdown(f"• {feature}")

def display_development_plan():
    """단계별 개발 계획"""
    st.header("📅 단계별 개발 계획")
    
    # 개발 단계별 진행 상황
    phases = [
        {
            "phase": "1단계: 기초 연구 및 프로토타입",
            "period": "1-2년 (2025-2026)",
            "budget": "3억 달러",
            "progress": 25,
            "tasks": [
                "수륙 양용 기술의 기초 연구 및 설계",
                "소규모 프로토타입 제작 및 기본 성능 테스트", 
                "핵심 기술 특허 출원 및 지적재산권 확보",
                "기술 타당성 검증 및 시장 조사"
            ],
            "milestones": [
                "기본 설계 완료",
                "소형 프로토타입 시험 운행",
                "핵심 특허 3건 출원"
            ]
        },
        {
            "phase": "2단계: 실용화 연구 및 테스트",
            "period": "3-5년 (2027-2029)",
            "budget": "10억 달러", 
            "progress": 0,
            "tasks": [
                "실제 크기의 프로토타입 제작",
                "육상 및 수상 환경에서의 광범위한 테스트",
                "안전성 및 효율성 검증",
                "운영 시나리오별 성능 평가"
            ],
            "milestones": [
                "실물 크기 프로토타입 완성",
                "1000km 시험 운행 완료",
                "안전 인증 획득"
            ]
        },
        {
            "phase": "3단계: 상업화 준비", 
            "period": "6-8년 (2030-2032)",
            "budget": "25억 달러",
            "progress": 0,
            "tasks": [
                "대량 생산 체계 구축",
                "법적 승인 및 인증 획득",
                "파일럿 노선 운영",
                "운영 인력 교육 및 훈련"
            ],
            "milestones": [
                "생산 라인 구축 완료",
                "상업 운행 허가 획득",
                "파일럿 노선 개통"
            ]
        },
        {
            "phase": "4단계: 상업 운영 시작",
            "period": "9-10년 (2033-2034)",
            "budget": "5억 달러",
            "progress": 0,
            "tasks": [
                "정식 상업 운영 개시",
                "운영 데이터 수집 및 최적화", 
                "추가 노선 확장",
                "지속적 기술 개선"
            ],
            "milestones": [
                "첫 상업 노선 개통",
                "연간 100만 승객 수송",
                "투자비 회수 시작"
            ]
        }
    ]
    
    for i, phase in enumerate(phases):
        st.subheader(f"📍 {phase['phase']}")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**기간**: {phase['period']}")
            st.markdown(f"**예산**: {phase['budget']}")
            st.progress(phase['progress']/100, text=f"진행률: {phase['progress']}%")
        
        with col2:
            st.markdown("**주요 과제**")
            for task in phase['tasks']:
                st.markdown(f"• {task}")
        
        with col3:
            st.markdown("**핵심 성과**")
            for milestone in phase['milestones']:
                st.markdown(f"✅ {milestone}")
        
        if i < len(phases) - 1:
            st.markdown("---")

def display_routes_and_usage():
    """예상 경로 및 활용"""
    st.header("🛣️ 예상 경로 및 활용")
    
    # 활용 분야별 탭
    route_tab, usage_tab, market_tab = st.tabs(["🗺️ 운행 경로", "🎯 활용 분야", "📊 시장 분석"])
    
    with route_tab:
        st.subheader("🌍 주요 운행 경로")
        
        route_categories = {
            "🏖️ 해안-도서 연결": [
                "부산 ↔ 제주도 (국내 관광 활성화)",
                "오사카 ↔ 후쿠오카 (국제 노선)",
                "샌프란시스코 ↔ 알카트라즈 섬",
                "시드니 ↔ 태즈마니아"
            ],
            "🏙️ 도심 간 하천 활용": [
                "서울 한강 연계 도심 순환선",
                "파리 세느강 관광 노선",
                "런던 템스강 통근 노선",
                "뉴욕 허드슨강 연결선"
            ],
            "🌏 국경 연결 노선": [
                "유럽 라인강 국제 노선",
                "동남아시아 메콩강 연결선",
                "북미 오대호 국경 노선",
                "남미 아마존강 탐험 노선"
            ]
        }
        
        for category, routes in route_categories.items():
            with st.expander(category, expanded=True):
                for route in routes:
                    st.markdown(f"• {route}")
    
    with usage_tab:
        st.subheader("🎯 주요 활용 분야")
        
        # 활용 분야별 중요도 시각화
        usage_data = {
            'Field': ['여객 교통', '관광 산업', '화물 운송', '재난 구조', '군사 작전', '연구 탐사'],
            'Market_Size': [100, 80, 60, 30, 40, 20],  # 억 달러
            'Priority': [10, 9, 7, 8, 6, 5]  # 우선순위 (10점 만점)
        }
        
        df_usage = pd.DataFrame(usage_data)
        
        fig_usage = px.scatter(
            df_usage,
            x='Market_Size',
            y='Priority', 
            size='Market_Size',
            color='Field',
            title='활용 분야별 시장 규모 vs 우선순위'
        )
        
        st.plotly_chart(fig_usage, use_container_width=True)
        
        # 세부 활용 방안
        usage_details = {
            "🚶 여객 및 관광 운송": [
                "육상과 수상을 동시에 경험하는 독창적 여행 옵션",
                "고급 관광 상품과 연계한 관광 산업 활성화",
                "크루즈 서비스와 결합한 프리미엄 여행",
                "통근용 고속 교통수단으로 활용"
            ],
            "📦 해상-육상 화물 운송": [
                "해안 지역과 내륙 허브 직접 연결",
                "컨테이너형 화물칸으로 다양한 화물 운반",
                "물류 시간 단축 및 비용 절감",
                "복합 운송 네트워크 구축"
            ],
            "🚨 재난 구조 및 군사 작전": [
                "홍수, 해일 등 재난 상황 신속 대응",
                "의료 장비 및 긴급 물자 수송",
                "상륙 작전 및 병력 수송",
                "해안 경비 및 순찰 임무"
            ]
        }
        
        for usage_type, details in usage_details.items():
            with st.expander(usage_type):
                for detail in details:
                    st.markdown(f"• {detail}")
    
    with market_tab:
        st.subheader("📈 시장 분석 및 전망")
        
        # 시장 규모 예측
        years = list(range(2025, 2041))
        market_size = [0, 0, 0, 1, 3, 8, 15, 25, 35, 50, 70, 95, 120, 150, 180, 200]
        
        market_df = pd.DataFrame({
            'Year': years,
            'Market_Size_Billion_USD': market_size
        })
        
        fig_market = px.line(
            market_df,
            x='Year',
            y='Market_Size_Billion_USD', 
            title='수륙 양용 교통 시장 규모 예측',
            labels={'Market_Size_Billion_USD': '시장 규모 (억 달러)'}
        )
        
        fig_market.update_traces(line=dict(width=3))
        st.plotly_chart(fig_market, use_container_width=True)
        
        # 지역별 시장 잠재력
        st.markdown("**🌍 지역별 시장 잠재력**")
        
        regional_data = {
            'Region': ['아시아-태평양', '유럽', '북미', '남미', '중동-아프리카'],
            'Potential': [35, 25, 20, 10, 10],
            'Readiness': [80, 90, 85, 60, 50]
        }
        
        regional_df = pd.DataFrame(regional_data)
        
        fig_regional = px.bar(
            regional_df,
            x='Region',
            y=['Potential', 'Readiness'],
            title='지역별 시장 잠재력 및 기술 준비도',
            barmode='group'
        )
        
        st.plotly_chart(fig_regional, use_container_width=True)

def display_technical_challenges():
    """주요 기술적 도전과 해결 방안"""
    st.header("🔧 주요 기술적 도전과 해결 방안")
    
    challenges = [
        {
            "challenge": "🔄 수륙 전환 안정성",
            "difficulty": 9,
            "solutions": [
                "자동화된 전환 시스템과 정밀 제어 기술 도입",
                "전환 시 발생 가능한 충격을 완화하는 감쇠 장치 적용",
                "전환 과정의 실시간 센서 모니터링 및 피드백 제어",
                "수천 번의 전환 테스트를 통한 내구성 검증"
            ]
        },
        {
            "challenge": "🌊 수중 속도 저하",
            "difficulty": 8,
            "solutions": [
                "유체역학적으로 최적화된 차체 설계로 수중 저항 감소",
                "슈퍼캐비테이션 기술로 공기 기포 형성하여 마찰 감소",
                "프로펠러 설계 최적화 및 수중 전용 추진 엔진 사용",
                "표면 처리 기술로 마찰 계수 최소화"
            ]
        },
        {
            "challenge": "⛽ 연료 효율성",
            "difficulty": 7,
            "solutions": [
                "하이브리드 동력 시스템으로 환경별 최적 동력원 사용",
                "경량 소재와 에너지 관리 시스템으로 소비 최적화",
                "회생 제동 기술로 브레이크 에너지 회수 재사용",
                "AI 기반 운행 패턴 최적화로 연료 효율 극대화"
            ]
        },
        {
            "challenge": "💧 내압 및 방수",
            "difficulty": 8,
            "solutions": [
                "고강도 복합소재와 방수 코팅으로 내구성 강화",
                "중요 부위에 다중 밀폐 구조 적용",
                "정기 유지보수를 고려한 설계로 장치 수명 연장",
                "수압 테스트 및 장기 침수 시험을 통한 검증"
            ]
        },
        {
            "challenge": "🌍 환경 영향",
            "difficulty": 6,
            "solutions": [
                "저소음 추진 시스템과 진동 억제 기술 적용",
                "친환경 연료(수소, 전기) 사용으로 배출가스 최소화",
                "수중 생태계 보호를 위한 생물학적 영향 분석",
                "운행 경로 최적화로 생태계 영향 구간 최소화"
            ]
        }
    ]
    
    # 도전과제별 난이도 시각화
    challenge_names = [c["challenge"] for c in challenges]
    difficulties = [c["difficulty"] for c in challenges]
    
    fig_challenges = px.bar(
        x=challenge_names,
        y=difficulties,
        title='기술적 도전과제별 난이도',
        labels={'x': '도전과제', 'y': '난이도 (10점 만점)'},
        color=difficulties,
        color_continuous_scale='Reds'
    )
    
    fig_challenges.update_layout(height=400)
    st.plotly_chart(fig_challenges, use_container_width=True)
    
    # 도전과제별 상세 해결방안
    for challenge in challenges:
        with st.expander(f"{challenge['challenge']} (난이도: {challenge['difficulty']}/10)", expanded=False):
            st.markdown("**해결 방안:**")
            for solution in challenge['solutions']:
                st.markdown(f"• {solution}")

def display_maintenance_plan():
    """유지보수 및 정비 계획"""
    st.header("🔨 유지보수 및 정비 계획")
    
    # 유지보수 계획 개요
    maintenance_tabs = st.tabs(["📅 정기 점검", "🔬 내구성 테스트", "🔧 수리 접근성", "💻 디지털 관리"])
    
    with maintenance_tabs[0]:
        st.subheader("📅 정기 점검 계획")
        
        # 점검 주기별 항목
        inspection_schedule = {
            '일일 점검': [
                '외관 및 기본 시스템 상태 확인',
                '배터리 충전 상태 점검',
                '안전 장치 작동 확인',
                '운행 로그 검토'
            ],
            '주간 점검': [
                '동력 시스템 성능 테스트',
                '전환 메커니즘 작동 테스트',
                '부력 시스템 점검',
                '브레이크 시스템 점검'
            ],
            '월간 점검': [
                '전기 시스템 종합 점검',
                '유압 시스템 압력 테스트',
                '방수 밀폐성 검사',
                '타이어 및 프로펠러 마모 점검'
            ],
            '분기별 점검': [
                '엔진 오버홀 및 성능 측정',
                '전환 장치 정밀 조정',
                '안전 시스템 종합 테스트',
                '소프트웨어 업데이트'
            ],
            '연간 점검': [
                '차체 구조 안전성 검사',
                '모든 시스템 종합 성능 평가',
                '법정 안전 인증 갱신',
                '주요 부품 교체 검토'
            ]
        }
        
        for period, items in inspection_schedule.items():
            with st.expander(period, expanded=(period == '일일 점검')):
                for item in items:
                    st.markdown(f"• {item}")
    
    with maintenance_tabs[1]:
        st.subheader("🔬 내구성 테스트")
        
        # 테스트 항목별 기준
        durability_tests = {
            '방수 밀폐성': {
                'frequency': '분기별',
                'method': '수중 운행 시 방수 코팅 및 밀폐 구조 장기 내구성 평가',
                'criteria': '100m 수심에서 24시간 무누수',
                'target': '10년 이상 유지'
            },
            '부력 시스템': {
                'frequency': '월별',
                'method': '팽창식 튜브와 공기 주입 장치 성능 및 내구성 테스트',
                'criteria': '10,000회 팽창/수축 반복',
                'target': '99.9% 신뢰성'
            },
            '차체 강도': {
                'frequency': '연간',
                'method': '수압, 충격, 진동에 따른 피로 수명 분석',
                'criteria': '설계 수명 30년 기준',
                'target': '안전계수 3.0 이상'
            },
            '전환 메커니즘': {
                'frequency': '주간',
                'method': '수륙 전환 반복 테스트 및 정밀도 측정',
                'criteria': '100,000회 전환 테스트',
                'target': '5초 이내 전환 유지'
            }
        }
        
        test_df = pd.DataFrame([
            [test, info['frequency'], info['criteria'], info['target']]
            for test, info in durability_tests.items()
        ], columns=['테스트 항목', '주기', '기준', '목표'])
        
        st.dataframe(test_df, use_container_width=True)
    
    with maintenance_tabs[2]:
        st.subheader("🔧 수리 접근성")
        
        st.markdown("""
        **모듈식 설계 원칙**
        - 주요 구성 요소를 독립적인 모듈로 설계
        - 동력부, 전환 메커니즘, 부력 튜브 개별 분리 가능
        - 표준화된 연결 인터페이스로 호환성 확보
        """)
        
        # 수리 시간 예상
        repair_times = {
            '부품명': ['배터리 모듈', '전환 모터', '부력 튜브', '프로펠러', '제어 유닛'],
            '예상 수리 시간': [2, 4, 3, 1, 6],  # 시간
            '필요 인력': [2, 3, 2, 1, 4],
            '비용 (만원)': [500, 1200, 300, 200, 2000]
        }
        
        repair_df = pd.DataFrame(repair_times)
        
        fig_repair = px.scatter(
            repair_df,
            x='예상 수리 시간',
            y='비용 (만원)',
            size='필요 인력',
            color='부품명',
            title='부품별 수리 시간 vs 비용'
        )
        
        st.plotly_chart(fig_repair, use_container_width=True)
    
    with maintenance_tabs[3]:
        st.subheader("💻 디지털 유지보수 시스템")
        
        digital_features = [
            "**실시간 상태 모니터링**",
            "• IoT 센서를 통한 주요 부품 성능 지속 확인",
            "• 클라우드 기반 데이터 수집 및 분석",
            "• 이상 징후 자동 감지 및 알림",
            "",
            "**예측 유지보수**",
            "• 머신러닝 기반 부품 고장 예측",
            "• 최적 교체 시기 자동 산출",
            "• 예방 정비로 다운타임 최소화",
            "",
            "**디지털 정비 이력**",
            "• 블록체인 기반 정비 이력 관리",
            "• 차량별 맞춤형 점검 계획 수립", 
            "• AR/VR 기술 활용 정비 지원"
        ]
        
        for feature in digital_features:
            if feature.startswith("**"):
                st.markdown(feature)
            elif feature.startswith("•"):
                st.markdown(f"  {feature}")
            else:
                st.markdown(feature)

def display_legal_compliance():
    """법적/규제 준수 사항"""
    st.header("⚖️ 법적/규제 준수 사항")
    
    # 규제 분야별 탭
    legal_tabs = st.tabs(["🚢 해상/철도 법규", "🌍 환경 규제", "🌏 국제 운항", "🛡️ 안전 규정"])
    
    with legal_tabs[0]:
        st.subheader("🚢 해상/철도 법규")
        
        regulations = {
            '해상 운항 규제': [
                '선박안전법 및 해양환경관리법 준수',
                '항로 설정 및 항해 장치 인증 요건',
                '해상교통관제 시스템 연동',
                '선원 자격 및 운항 면허 요건'
            ],
            '철도 및 육상 교통': [
                '철도안전법 및 도로교통법 준수',
                '육상 교통 신호 체계 적합성',
                '철도 안전관리 시스템 적용',
                '운전자 자격 및 교육 요건'
            ],
            '수륙 양용 특별 규제': [
                '새로운 차량 분류 및 등록 기준',
                '전환 구간 안전 관리 규정',
                '복합 교통수단 보험 체계',
                '사고 조사 및 책임 소재 규정'
            ]
        }
        
        for category, items in regulations.items():
            with st.expander(category, expanded=True):
                for item in items:
                    st.markdown(f"• {item}")
    
    with legal_tabs[1]:
        st.subheader("🌍 환경 규제")
        
        # 환경 기준 테이블
        env_standards = {
            '규제 항목': ['배출가스', '수질 오염', '소음', '진동', '생태계 영향'],
            '현재 기준': ['IMO Tier III', '0.1ppm 이하', '65dB 이하', '0.5G 이하', 'EIA 필수'],
            '목표 성능': ['50% 감소', '무배출', '55dB 이하', '0.3G 이하', '영향 최소화'],
            '달성 방법': ['하이브리드', '밀폐 시스템', '저소음 설계', '진동 억제', '경로 최적화']
        }
        
        env_df = pd.DataFrame(env_standards)
        st.dataframe(env_df, use_container_width=True)
    
    with legal_tabs[2]:
        st.subheader("🌏 국제 운항")
        
        international_reqs = [
            "**국제 해사 협약**",
            "• SOLAS (해상인명안전협약) 준수",
            "• MARPOL (해양오염방지협약) 적용",
            "• STCW (선원훈련감시협약) 준수",
            "",
            "**국제 교통 협정**", 
            "• 각국 운송 규제 적합성 확보",
            "• 관세 및 운항 허가 요건 충족",
            "• 국제 항만 접근 절차 준수",
            "",
            "**인증 및 표준**",
            "• ISO 9001 품질 관리 시스템",
            "• CE 마킹 (유럽 적합성 인증)",
            "• FCC 승인 (전자 장비)"
        ]
        
        for req in international_reqs:
            if req.startswith("**"):
                st.markdown(req)
            elif req.startswith("•"):
                st.markdown(f"  {req}")
            else:
                st.markdown(req)
    
    with legal_tabs[3]:
        st.subheader("🛡️ 안전 규정")
        
        # 안전 시스템 구성
        safety_systems = {
            'System': ['충돌 방지', '화재 감지', '침수 대응', '비상 탈출', '통신 시스템'],
            'Technology': ['레이더+LiDAR', '연기/열 감지', '자동 배수', '다중 탈출구', '위성 통신'],
            'Response_Time': [0.5, 2, 5, 30, 1],  # 초
            'Reliability': [99.9, 99.8, 99.5, 99.9, 99.7]  # %
        }
        
        safety_df = pd.DataFrame(safety_systems)
        
        fig_safety = px.scatter(
            safety_df,
            x='Response_Time',
            y='Reliability',
            size='Response_Time',
            color='System',
            title='안전 시스템별 응답시간 vs 신뢰성',
            labels={'Response_Time': '응답시간 (초)', 'Reliability': '신뢰성 (%)'}
        )
        
        st.plotly_chart(fig_safety, use_container_width=True)

def display_operational_optimization():
    """운영 최적화"""
    st.header("📈 운영 최적화")
    
    # 최적화 영역별 탭
    optimization_tabs = st.tabs(["🌤️ 기상 대응", "🗺️ 경로 최적화", "📊 수요 예측", "💰 비용 분석"])
    
    with optimization_tabs[0]:
        st.subheader("🌤️ 기상 대응 시스템")
        
        weather_conditions = {
            '기상 조건': ['맑음', '비', '강풍', '눈', '안개', '높은 파도'],
            '운행 제한': ['없음', '속도 50% 감소', '운행 중단', '전환 금지', '시정 불량', '수상 금지'],
            '대응 시스템': ['정상 운행', '자동 감속', '안전 대기', '육상 전용', 'GPS 항법', '육상 우회'],
            '위험도': [1, 3, 8, 5, 6, 9]
        }
        
        weather_df = pd.DataFrame(weather_conditions)
        
        fig_weather = px.bar(
            weather_df,
            x='기상 조건',
            y='위험도',
            color='위험도',
            title='기상 조건별 운행 위험도',
            color_continuous_scale='Reds'
        )
        
        st.plotly_chart(fig_weather, use_container_width=True)
        
        st.dataframe(weather_df, use_container_width=True)
    
    with optimization_tabs[1]:
        st.subheader("🗺️ 경로 최적화")
        
        route_factors = [
            "**실시간 최적화 요소**",
            "• GPS 및 GIS 기반 실시간 위치 추적",
            "• 교통 상황 및 수상 흐름 분석",
            "• 에너지 소비 최소화 경로 계산",
            "• 승객 편의 및 안전성 고려",
            "",
            "**AI 예측 모델**",
            "• 머신러닝 기반 교통 패턴 분석",
            "• 계절별/시간대별 최적 경로 학습",
            "• 날씨 변화에 따른 경로 자동 조정",
            "• 연료 효율 및 시간 단축 균형점 탐색"
        ]
        
        for factor in route_factors:
            if factor.startswith("**"):
                st.markdown(factor)
            elif factor.startswith("•"):
                st.markdown(f"  {factor}")
            else:
                st.markdown(factor)
        
        # 경로 효율성 시뮬레이션
        st.markdown("**경로별 효율성 비교**")
        
        route_comparison = {
            'Route': ['기존 도로', '기존 해상', '수륙 복합 A', '수륙 복합 B', '최적 수륙'],
            'Distance_km': [120, 80, 100, 90, 85],
            'Time_hours': [2.5, 3.0, 2.0, 1.8, 1.5],
            'Energy_cost': [100, 120, 80, 75, 65]
        }
        
        route_df = pd.DataFrame(route_comparison)
        
        fig_route = px.scatter(
            route_df,
            x='Time_hours',
            y='Energy_cost',
            size='Distance_km',
            color='Route',
            title='경로별 시간 vs 에너지 비용',
            labels={'Time_hours': '소요시간 (시간)', 'Energy_cost': '에너지 비용 (상대값)'}
        )
        
        st.plotly_chart(fig_route, use_container_width=True)
    
    with optimization_tabs[2]:
        st.subheader("📊 수요 예측 및 운영 계획")
        
        # 시간대별 수요 패턴
        hours = list(range(24))
        demand_pattern = [10, 5, 3, 3, 5, 15, 35, 60, 45, 30, 25, 30, 
                         35, 40, 35, 45, 70, 85, 60, 40, 30, 25, 20, 15]
        
        demand_df = pd.DataFrame({
            'Hour': hours,
            'Demand': demand_pattern
        })
        
        fig_demand = px.line(
            demand_df,
            x='Hour',
            y='Demand',
            title='시간대별 승객 수요 패턴',
            labels={'Hour': '시간', 'Demand': '수요 (%)'}
        )
        
        fig_demand.update_traces(line=dict(width=3))
        st.plotly_chart(fig_demand, use_container_width=True)
        
        # 수요 대응 전략
        demand_strategies = {
            '시간대': ['새벽 (0-6시)', '출근 (7-9시)', '오전 (10-12시)', '오후 (13-17시)', '퇴근 (18-20시)', '야간 (21-23시)'],
            '수요 수준': ['낮음', '매우 높음', '보통', '높음', '매우 높음', '보통'],
            '운행 전략': ['최소 운행', '증편 운행', '정기 운행', '관광 중심', '증편 운행', '야간 운행'],
            '요금 정책': ['할인', '정상', '정상', '정상', '정상', '할인']
        }
        
        strategy_df = pd.DataFrame(demand_strategies)
        st.dataframe(strategy_df, use_container_width=True)
    
    with optimization_tabs[3]:
        st.subheader("💰 운영 비용 분석")
        
        # 비용 구조 분석
        cost_breakdown = {
            'Category': ['연료비', '인건비', '유지보수', '보험', '인프라', '기타'],
            'Percentage': [30, 25, 20, 10, 10, 5],
            'Monthly_Cost_Million': [15, 12.5, 10, 5, 5, 2.5]
        }
        
        cost_df = pd.DataFrame(cost_breakdown)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_cost_pie = px.pie(
                cost_df,
                values='Percentage',
                names='Category',
                title='운영 비용 구조'
            )
            st.plotly_chart(fig_cost_pie, use_container_width=True)
        
        with col2:
            fig_cost_bar = px.bar(
                cost_df,
                x='Category',
                y='Monthly_Cost_Million',
                title='월간 운영 비용 (백만원)',
                color='Monthly_Cost_Million',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_cost_bar, use_container_width=True)
        
        # ROI 분석
        st.markdown("**📈 투자 회수 분석**")
        
        years = list(range(2025, 2041))
        cumulative_investment = [-3, -13, -25, -38, -35, -30, -20, -5, 15, 40, 70, 105, 145, 190, 240, 295]
        annual_revenue = [0, 0, 0, 5, 12, 18, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115]
        
        roi_df = pd.DataFrame({
            'Year': years,
            'Cumulative_Investment': cumulative_investment,
            'Annual_Revenue': annual_revenue
        })
        
        fig_roi = px.line(
            roi_df,
            x='Year',
            y=['Cumulative_Investment', 'Annual_Revenue'],
            title='투자 회수 및 연간 수익 전망',
            labels={'value': '금액 (억 달러)', 'variable': '구분'}
        )
        
        # Break-even point 표시
        fig_roi.add_hline(y=0, line_dash="dash", line_color="red", 
                         annotation_text="손익분기점")
        
        st.plotly_chart(fig_roi, use_container_width=True)
        
        # 핵심 성과 지표
        st.markdown("**🎯 핵심 성과 지표 (KPI)**")
        
        kpis = {
            'KPI': ['승객 만족도', '정시 운행률', '안전 사고율', '에너지 효율', '수익성'],
            'Current': ['-', '-', '-', '-', '-'],
            'Target_2030': ['95%', '98%', '< 0.01%', '40% 개선', '15% ROI'],
            'Target_2035': ['98%', '99%', '< 0.005%', '60% 개선', '25% ROI']
        }
        
        kpi_df = pd.DataFrame(kpis)
        st.dataframe(kpi_df, use_container_width=True)

# 메인 실행
if __name__ == "__main__":
    display_amphibious_train_project()
