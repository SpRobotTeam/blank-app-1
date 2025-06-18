import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, info_message, sidebar_info

def display_laser_technology_project():
    """
    조선업 소부재용 레이저 소스 30kW 이상급 레이저 점단 시스템 개발
    첨단 레이저 기술을 활용한 조선업 혁신 프로젝트의 기술적 세부사항과 개발 계획을 종합적으로 다룹니다.
    """
    # 도구 헤더 적용
    tool_header(
        "조선업 레이저 시스템 개발 프로젝트", 
        "30kW급 고출력 레이저를 활용한 조선업 소부재 가공 시스템 개발 프로젝트입니다. 첨단 레이저 기술과 정밀 가공의 융합을 통한 조선업 혁신 비전을 확인해보세요."
    )

    # 사이드바에 프로젝트 정보 표시
    with st.sidebar:
        sidebar_info(version="1.0", update_date="2025-06-15")
        
        st.markdown("### 📊 프로젝트 현황")
        st.progress(0.05, text="5% 완료 (과제 시작 단계)")
        
        st.markdown("### 💰 예산 현황")
        total_budget = 90.35  # 억원
        spent_budget = 0      # 억원 (시작 단계)
        remaining_budget = total_budget - spent_budget
        
        budget_data = pd.DataFrame({
            'Category': ['사용된 예산', '남은 예산'],
            'Amount': [spent_budget, remaining_budget]
        })
        
        fig_budget = px.pie(budget_data, values='Amount', names='Category', 
                           color_discrete_sequence=['#ff7f7f', '#90EE90'])
        fig_budget.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig_budget, use_container_width=True)
        
        st.metric("총 예산", f"{total_budget}억원", f"남은 예산 {remaining_budget}억원")

    # 탭으로 메뉴 생성
    tab_names = [
        "📋 프로젝트 개요",
        "🎯 연구개발 목표",
        "⚙️ 핵심 기술",
        "📅 개발 로드맵",
        "🏢 참여기관 현황",
        "🔧 기술적 도전",
        "💼 시장 분석",
        "📈 기대효과",
        "🛠️ 위험관리"
    ]
    
    tabs = st.tabs(tab_names)

    # 각 탭의 내용 정의
    with tabs[0]:
        display_project_overview()

    with tabs[1]:
        display_research_goals()

    with tabs[2]:
        display_core_technology()

    with tabs[3]:
        display_development_roadmap()

    with tabs[4]:
        display_participating_organizations()

    with tabs[5]:
        display_technical_challenges()

    with tabs[6]:
        display_market_analysis()

    with tabs[7]:
        display_expected_effects()

    with tabs[8]:
        display_risk_management()

def display_project_overview():
    """프로젝트 개요"""
    st.header("📋 프로젝트 개요")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🔬 조선업 레이저 시스템이란?
        
        30kW급 고출력 레이저를 활용하여 조선업 소부재를 정밀하게 
        가공할 수 있는 혁신적인 시스템입니다. 기존 가공 방식의 
        한계를 뛰어넘는 새로운 제조 패러다임을 제시합니다.
        
        ### 🌟 주요 특징
        - **고출력**: 30kW급 레이저 소스 적용
        - **정밀성**: μm 단위 정밀 가공 가능
        - **효율성**: 기존 대비 50% 이상 가공 시간 단축
        - **친환경**: 무공해 가공 공정
        - **자동화**: 스마트 제조 시스템 연동
        """)
    
    with col2:
        # 주요 지표 표시
        st.markdown("### 📊 핵심 지표")
        st.metric("레이저 출력", "30+ kW")
        st.metric("가공 정밀도", "±10 μm")
        st.metric("처리 속도", "500% 향상")
        st.metric("에너지 효율", "40% 개선")
        st.metric("불량률 감소", "90%+")
    
    # 프로젝트 일정 시각화
    st.markdown("### 📅 프로젝트 단계별 일정")
    
    timeline_data = {
        'Phase': ['1년차: 기초연구', '2년차: 시스템 설계', '3년차: 프로토타입', '4년차: 실용화'],
        'Start': [2025, 2026, 2027, 2028],
        'Duration': [1, 1, 1, 1],
        'Budget': [15.5, 22.7, 30.8, 21.35]  # 억원
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
        title='연도별 개발 단계 및 예산 배분'
    )
    
    fig_timeline.update_layout(
        xaxis_title="연도",
        yaxis_title="개발 단계",
        height=400
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)

def display_research_goals():
    """연구개발 목표"""
    st.header("🎯 연구개발 목표")
    
    goals = [
        {
            "title": "🔥 30kW급 고출력 레이저 소스 개발",
            "description": "조선업 소부재 가공에 최적화된 고출력 레이저 시스템 구축",
            "details": [
                "연속파(CW) 30kW급 파이버 레이저 개발",
                "빔 품질 M² < 1.2 달성으로 정밀 가공 실현",
                "전력 효율 40% 이상으로 에너지 절약",
                "24시간 연속 운전 가능한 안정성 확보"
            ]
        },
        {
            "title": "⚡ 정밀 레이저 점단 시스템 구현",
            "description": "μm 단위 정밀도를 가진 레이저 점단 가공 시스템 개발",
            "details": [
                "±10μm 이내 가공 정밀도 달성",
                "다양한 소재(강재, 알루미늄, 티타늄) 대응",
                "실시간 품질 모니터링 시스템",
                "자동화된 가공 경로 최적화"
            ]
        },
        {
            "title": "🤖 스마트 제조 시스템 연동",
            "description": "Industry 4.0 기반 지능형 제조 시스템과의 통합",
            "details": [
                "AI 기반 가공 조건 최적화",
                "IoT 센서를 통한 실시간 모니터링",
                "디지털 트윈 기술 적용",
                "예측 유지보수 시스템 구축"
            ]
        },
        {
            "title": "🌍 조선업 공정 혁신",
            "description": "기존 조선업 제조 공정의 혁신적 개선",
            "details": [
                "가공 시간 50% 이상 단축",
                "소재 손실률 30% 감소",
                "작업 환경 안전성 대폭 향상",
                "제품 품질 일관성 확보"
            ]
        },
        {
            "title": "🏭 상용화 및 산업 확산",
            "description": "개발 기술의 조선업계 전반 확산 및 해외 진출",
            "details": [
                "국내 조선소 5곳 이상 기술 이전",
                "해외 시장 진출을 위한 인증 획득",
                "관련 특허 20건 이상 출원",
                "기술 표준화 및 가이드라인 제정"
            ]
        }
    ]
    
    for i, goal in enumerate(goals):
        with st.expander(f"{goal['title']}", expanded=(i==0)):
            st.markdown(f"**{goal['description']}**")
            st.markdown("**세부 목표:**")
            for detail in goal['details']:
                st.markdown(f"• {detail}")

def display_core_technology():
    """핵심 기술 요소"""
    st.header("⚙️ 핵심 기술 요소")
    
    # 기술 성숙도 시각화
    tech_components = {
        'Technology': ['레이저 소스', '빔 전달 시스템', '가공 헤드', '제어 시스템', 'AI 최적화'],
        'Complexity': [9, 7, 8, 6, 9],
        'Importance': [10, 8, 9, 7, 8],
        'TRL': [6, 7, 5, 8, 4]  # Technology Readiness Level
    }
    
    df_tech = pd.DataFrame(tech_components)
    
    fig_tech = px.scatter(
        df_tech, 
        x='Complexity', 
        y='Importance',
        size='TRL',
        color='Technology',
        title='핵심 기술별 복잡도 vs 중요도 (크기: 기술성숙도)',
        labels={'Complexity': '기술 복잡도', 'Importance': '중요도'}
    )
    
    fig_tech.update_layout(height=500)
    st.plotly_chart(fig_tech, use_container_width=True)
    
    # 기술별 상세 설명
    st.subheader("🔧 주요 기술 시스템")
    
    tech_details = {
        "🔥 30kW급 파이버 레이저": {
            "description": "고출력 연속파 파이버 레이저 시스템",
            "features": [
                "Yb 도핑 파이버를 이용한 고효율 증폭",
                "모듈형 구조로 확장성 및 유지보수성 확보",
                "능동형 냉각 시스템으로 열적 안정성 보장",
                "실시간 출력 모니터링 및 피드백 제어"
            ]
        },
        "🎯 정밀 빔 전달 시스템": {
            "description": "고품질 레이저빔의 정밀 전달 및 집속 시스템",
            "features": [
                "광섬유 기반 유연한 빔 전달",
                "적응형 광학계를 통한 빔 품질 보정",
                "다축 갈바노 스캐너로 고속 정밀 위치 제어",
                "실시간 빔 프로파일 모니터링"
            ]
        },
        "⚙️ 지능형 가공 헤드": {
            "description": "다양한 가공 조건에 대응하는 스마트 가공 헤드",
            "features": [
                "자동 초점 조절 시스템",
                "다중 가스 보조 시스템",
                "실시간 가공 상태 모니터링",
                "적응형 가공 파라미터 조절"
            ]
        },
        "🧠 AI 기반 제어 시스템": {
            "description": "인공지능 기반 통합 제어 및 최적화 시스템",
            "features": [
                "머신러닝 기반 가공 조건 최적화",
                "실시간 품질 예측 및 보정",
                "예측 유지보수 알고리즘",
                "디지털 트윈 기반 가상 검증"
            ]
        }
    }
    
    for tech_name, tech_info in tech_details.items():
        with st.expander(tech_name, expanded=False):
            st.markdown(f"**{tech_info['description']}**")
            st.markdown("**주요 특징:**")
            for feature in tech_info['features']:
                st.markdown(f"• {feature}")

def display_development_roadmap():
    """개발 로드맵"""
    st.header("📅 개발 로드맵")
    
    # 연도별 개발 계획
    roadmap_data = {
        '구분': ['레이저 소스', '빔 전달', '가공 헤드', '제어 시스템', 'AI 최적화', '시스템 통합'],
        '1년차 (2025)': ['기초 연구', '설계', '요구사항 분석', '아키텍처 설계', '알고리즘 연구', '시스템 분석'],
        '2년차 (2026)': ['프로토타입', '시제품', '기본 모델', '기본 제어', '기초 AI', '부분 통합'],
        '3년차 (2027)': ['고도화', '최적화', '정밀화', '고급 제어', 'AI 고도화', '전체 통합'],
        '4년차 (2028)': ['상용화', '안정화', '양산 설계', '최종 검증', '실용화', '완성']
    }
    
    roadmap_df = pd.DataFrame(roadmap_data)
    st.dataframe(roadmap_df, use_container_width=True)
    
    # 마일스톤 시각화
    st.subheader("🎯 주요 마일스톤")
    
    milestones = {
        'Milestone': [
            '10kW 프로토타입 완성',
            '20kW 시제품 개발',
            '30kW 풀시스템 구축',
            'AI 최적화 적용',
            '실증 테스트 완료',
            '상용화 버전 출시'
        ],
        'Target_Date': ['2025-12', '2026-06', '2026-12', '2027-06', '2027-12', '2028-12'],
        'Progress': [0, 0, 0, 0, 0, 0],
        'Importance': [7, 8, 10, 8, 9, 10]
    }
    
    milestone_df = pd.DataFrame(milestones)
    
    fig_milestone = px.scatter(
        milestone_df,
        x='Target_Date',
        y='Importance',
        size='Importance',
        color='Progress',
        hover_data=['Milestone'],
        title='주요 마일스톤 일정 및 중요도'
    )
    
    st.plotly_chart(fig_milestone, use_container_width=True)

def display_participating_organizations():
    """참여기관 현황"""
    st.header("🏢 참여기관 현황")
    
    # 참여기관 정보
    orgs_data = {
        '기관명': [
            '주식회사 에이치케이',
            '한국기계연구원',
            '에이치디한국조선해양',
            '에스피시스템스',
            '삼성중공업'
        ],
        '구분': ['주관', '공동', '공동', '공동', '공동'],
        '역할': [
            '전체 시스템 통합 및 사업화',
            '레이저 소스 핵심 기술 개발',
            '조선업 적용 기술 및 실증',
            '제어 시스템 및 소프트웨어',
            '시스템 검증 및 현장 적용'
        ],
        '연구비(억원)': [50.0, 20.0, 10.0, 5.35, 5.0],
        '연구기간': ['48개월', '48개월', '36개월', '36개월', '24개월']
    }
    
    orgs_df = pd.DataFrame(orgs_data)
    st.dataframe(orgs_df, use_container_width=True)
    
    # 연구비 배분 시각화
    col1, col2 = st.columns(2)
    
    with col1:
        fig_budget_pie = px.pie(
            orgs_df,
            values='연구비(억원)',
            names='기관명',
            title='기관별 연구비 배분',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_budget_pie, use_container_width=True)
    
    with col2:
        fig_budget_bar = px.bar(
            orgs_df,
            x='기관명',
            y='연구비(억원)',
            color='구분',
            title='기관별 연구비 현황',
            text='연구비(억원)'
        )
        fig_budget_bar.update_traces(texttemplate='%{text}억원', textposition='outside')
        st.plotly_chart(fig_budget_bar, use_container_width=True)
    
    # 기관별 상세 역할
    st.subheader("🎯 기관별 세부 역할")
    
    org_details = {
        "🏭 주식회사 에이치케이 (주관기관)": [
            "프로젝트 전체 관리 및 총괄 조정",
            "시스템 통합 및 최종 검증",
            "사업화 전략 수립 및 실행",
            "시장 진출 및 고객 대응"
        ],
        "🔬 한국기계연구원": [
            "30kW급 파이버 레이저 소스 개발",
            "레이저 빔 품질 최적화 기술",
            "열관리 시스템 설계",
            "안전성 평가 및 검증"
        ],
        "⚓ 에이치디한국조선해양": [
            "조선업 현장 적용 기술 개발",
            "실제 생산라인 실증 테스트",
            "공정 표준화 및 최적화",
            "품질 관리 시스템 구축"
        ],
        "💻 에스피시스템스": [
            "통합 제어 시스템 개발",
            "AI 기반 최적화 알고리즘",
            "사용자 인터페이스 설계",
            "데이터 분석 및 관리 시스템"
        ],
        "🚢 삼성중공업": [
            "대형 조선소 검증 및 평가",
            "대량 생산 적용성 검토",
            "경제성 분석 및 ROI 평가",
            "해외 시장 진출 지원"
        ]
    }
    
    for org_name, roles in org_details.items():
        with st.expander(org_name):
            for role in roles:
                st.markdown(f"• {role}")

def display_technical_challenges():
    """기술적 도전과 해결 방안"""
    st.header("🔧 기술적 도전과 해결 방안")
    
    challenges = [
        {
            "challenge": "🔥 고출력 레이저의 열관리",
            "difficulty": 9,
            "solutions": [
                "다단계 능동형 냉각 시스템 구축",
                "고효율 방열 소재 및 구조 적용",
                "실시간 온도 모니터링 및 피드백 제어",
                "모듈형 설계로 열원 분산"
            ]
        },
        {
            "challenge": "⚡ 빔 품질 및 안정성 확보",
            "difficulty": 8,
            "solutions": [
                "적응형 광학계를 통한 실시간 빔 보정",
                "진동 절연 시스템으로 외부 영향 차단",
                "고정밀 빔 진단 장비 도입",
                "환경 변화에 강인한 시스템 설계"
            ]
        },
        {
            "challenge": "🎯 μm급 정밀 가공 정확도",
            "difficulty": 9,
            "solutions": [
                "고분해능 위치 제어 시스템",
                "실시간 피드백 기반 오차 보정",
                "AI 기반 가공 경로 최적화",
                "환경 요인 보상 알고리즘"
            ]
        },
        {
            "challenge": "🤖 AI 최적화 시스템 구현",
            "difficulty": 7,
            "solutions": [
                "대용량 가공 데이터 수집 및 학습",
                "디지털 트윈 기반 가상 검증",
                "실시간 추론 가능한 경량 AI 모델",
                "지속 학습 기능으로 성능 개선"
            ]
        },
        {
            "challenge": "🏭 조선업 현장 적용성",
            "difficulty": 6,
            "solutions": [
                "현장 환경 분석 및 맞춤형 설계",
                "기존 생산 라인과의 호환성 확보",
                "작업자 교육 및 훈련 프로그램",
                "단계적 도입을 통한 리스크 최소화"
            ]
        }
    ]
    
    # 도전과제별 난이도 시각화
    challenge_names = [c["challenge"] for c in challenges]
    difficulties = [c["difficulty"] for c in challenges]
    
    fig_challenges = px.bar(
        x=challenge_names,
        y=difficulties,
        title='기술적 도전과제별 난이도 평가',
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

def display_market_analysis():
    """시장 분석"""
    st.header("💼 시장 분석")
    
    market_tabs = st.tabs(["🌍 시장 규모", "🎯 타겟 시장", "🏆 경쟁사 분석"])
    
    with market_tabs[0]:
        st.subheader("📈 글로벌 시장 규모")
        
        # 시장 규모 예측
        years = list(range(2025, 2036))
        market_size = [450, 520, 600, 690, 795, 915, 1050, 1200, 1380, 1580, 1810]
        
        market_df = pd.DataFrame({
            'Year': years,
            'Market_Size_Million_USD': market_size
        })
        
        fig_market = px.line(
            market_df,
            x='Year',
            y='Market_Size_Million_USD',
            title='글로벌 레이저 가공 시스템 시장 규모 예측',
            labels={'Market_Size_Million_USD': '시장 규모 (백만 달러)'}
        )
        fig_market.update_traces(line=dict(width=3))
        st.plotly_chart(fig_market, use_container_width=True)
        
        # 지역별 시장 분포
        regional_data = {
            'Region': ['아시아-태평양', '유럽', '북미', '기타'],
            'Market_Share': [45, 25, 20, 10],
            'Growth_Rate': [12.5, 8.2, 6.8, 9.1]
        }
        
        regional_df = pd.DataFrame(regional_data)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_regional = px.pie(
                regional_df,
                values='Market_Share',
                names='Region',
                title='지역별 시장 점유율 (%)'
            )
            st.plotly_chart(fig_regional, use_container_width=True)
        
        with col2:
            fig_growth = px.bar(
                regional_df,
                x='Region',
                y='Growth_Rate',
                title='지역별 연평균 성장률 (%)',
                color='Growth_Rate',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_growth, use_container_width=True)
    
    with market_tabs[1]:
        st.subheader("🎯 타겟 시장 분석")
        
        target_markets = {
            '산업 분야': ['조선업', '자동차', '항공우주', '중공업', '철강', '기타'],
            '시장 규모(억원)': [150, 280, 120, 200, 180, 70],
            '성장률(%)': [15.2, 8.5, 12.3, 9.8, 6.2, 11.1],
            '진입 용이성': [9, 6, 7, 8, 7, 8]
        }
        
        target_df = pd.DataFrame(target_markets)
        
        fig_target = px.scatter(
            target_df,
            x='성장률(%)',
            y='시장 규모(억원)',
            size='진입 용이성',
            color='산업 분야',
            title='산업별 시장 매력도 분석'
        )
        st.plotly_chart(fig_target, use_container_width=True)
        
        st.markdown("**🎯 1차 타겟: 조선업**")
        st.markdown("• 높은 성장률과 큰 시장 규모")
        st.markdown("• 참여기관의 도메인 전문성 활용 가능")
        st.markdown("• 정부 정책 지원 및 산업 혁신 요구")
    
    with market_tabs[2]:
        st.subheader("🏆 주요 경쟁사 분석")
        
        competitors = {
            '경쟁사': ['IPG Photonics', 'nLIGHT', 'Coherent', 'TRUMPF', 'Raycus'],
            '시장점유율(%)': [35, 15, 12, 20, 8],
            '기술수준': [9, 8, 8, 9, 7],
            '가격경쟁력': [6, 7, 6, 5, 9]
        }
        
        comp_df = pd.DataFrame(competitors)
        
        fig_comp = px.scatter(
            comp_df,
            x='기술수준',
            y='가격경쟁력',
            size='시장점유율(%)',
            color='경쟁사',
            title='주요 경쟁사 기술 수준 vs 가격 경쟁력'
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.markdown("**💡 차별화 전략**")
        st.markdown("• 조선업 특화 솔루션으로 틈새시장 공략")
        st.markdown("• AI 기반 스마트 제조 시스템 통합")
        st.markdown("• 국내 조선소와의 긴밀한 협력 관계")

def display_expected_effects():
    """기대효과"""
    st.header("📈 기대효과")
    
    effect_tabs = st.tabs(["💰 경제적 효과", "🔬 기술적 효과", "🌍 사회적 효과"])
    
    with effect_tabs[0]:
        st.subheader("💰 경제적 효과")
        
        # 경제적 효과 시뮬레이션
        economic_effects = {
            '구분': [
                '직접 매출 창출',
                '수입 대체 효과',
                '수출 증대',
                '고용 창출',
                '투자 유발',
                '총 경제적 효과'
            ],
            '1년차': [0, 0, 0, 20, 10, 30],
            '3년차': [50, 30, 20, 100, 80, 280],
            '5년차': [200, 150, 100, 300, 250, 1000],
            '10년차': [800, 600, 500, 800, 700, 3400]
        }
        
        economic_df = pd.DataFrame(economic_effects)
        
        # 연도별 누적 효과
        years = [1, 3, 5, 10]
        total_effects = [30, 280, 1000, 3400]
        
        fig_economic = px.line(
            x=years,
            y=total_effects,
            title='총 경제적 효과 (억원)',
            labels={'x': '년차', 'y': '누적 경제적 효과 (억원)'}
        )
        fig_economic.update_traces(line=dict(width=3))
        st.plotly_chart(fig_economic, use_container_width=True)
        
        st.dataframe(economic_df, use_container_width=True)
    
    with effect_tabs[1]:
        st.subheader("🔬 기술적 효과")
        
        tech_effects = [
            "**🎯 정밀 가공 기술 향상**",
            "• 기존 대비 10배 향상된 정밀도 (±10μm)",
            "• 복잡 형상 가공 능력 대폭 개선",
            "• 다양한 소재에 대한 범용성 확보",
            "",
            "**⚡ 생산성 혁신**",
            "• 가공 속도 500% 향상",
            "• 불량률 90% 감소",
            "• 자동화율 95% 이상 달성",
            "",
            "**🧠 AI 융합 기술**",
            "• 실시간 품질 예측 및 보정",
            "• 예측 유지보수로 가동률 향상",
            "• 디지털 트윈 기반 가상 검증",
            "",
            "**📚 지적재산권 확보**",
            "• 핵심 특허 20건 이상 출원",
            "• 국제 표준화 참여 및 주도",
            "• 기술 라이선싱을 통한 수익 창출"
        ]
        
        for effect in tech_effects:
            if effect.startswith("**"):
                st.markdown(effect)
            elif effect.startswith("•"):
                st.markdown(f"  {effect}")
            else:
                st.markdown(effect)
    
    with effect_tabs[2]:
        st.subheader("🌍 사회적 효과")
        
        social_effects = [
            "**👥 고용 창출**",
            "• 직접 고용: 연구개발 인력 100명",
            "• 간접 고용: 관련 산업 500명",
            "• 고급 기술 인력 양성 및 전문성 향상",
            "",
            "**🏭 산업 경쟁력 강화**",
            "• 조선업의 스마트 제조 전환 가속화",
            "• 국내 제조업의 글로벌 경쟁력 향상",
            "• 미래 성장동력 산업 기반 구축",
            "",
            "**🌱 환경 친화적 제조**",
            "• 무공해 가공으로 작업 환경 개선",
            "• 에너지 효율 향상으로 탄소 배출 감소",
            "• 소재 손실 최소화로 자원 절약",
            "",
            "**🎓 기술 인력 양성**",
            "• 산학연 협력을 통한 전문 인력 교육",
            "• 레이저 기술 분야 전문가 육성",
            "• 기술 확산을 통한 산업 전반 역량 강화"
        ]
        
        for effect in social_effects:
            if effect.startswith("**"):
                st.markdown(effect)
            elif effect.startswith("•"):
                st.markdown(f"  {effect}")
            else:
                st.markdown(effect)

def display_risk_management():
    """위험관리"""
    st.header("🛠️ 위험관리")
    
    risk_tabs = st.tabs(["⚠️ 위험 분석", "🛡️ 대응 전략", "📊 모니터링"])
    
    with risk_tabs[0]:
        st.subheader("⚠️ 주요 위험 요소")
        
        risks = {
            '위험 요소': [
                '기술적 위험',
                '시장 위험',
                '재정적 위험',
                '인력 위험',
                '규제 위험',
                '경쟁 위험'
            ],
            '발생 가능성': [7, 5, 4, 6, 3, 8],
            '영향도': [9, 8, 7, 6, 5, 7],
            '위험도': [63, 40, 28, 36, 15, 56]
        }
        
        risk_df = pd.DataFrame(risks)
        risk_df['위험도'] = risk_df['발생 가능성'] * risk_df['영향도']
        
        fig_risk = px.scatter(
            risk_df,
            x='발생 가능성',
            y='영향도',
            size='위험도',
            color='위험 요소',
            title='위험 요소별 발생 가능성 vs 영향도'
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # 위험도 순위
        risk_sorted = risk_df.sort_values('위험도', ascending=False)
        st.markdown("**🚨 고위험 순위**")
        for idx, row in risk_sorted.iterrows():
            risk_level = "🔴 높음" if row['위험도'] > 50 else "🟡 중간" if row['위험도'] > 30 else "🟢 낮음"
            st.markdown(f"{row['위험 요소']}: {risk_level} (위험도: {row['위험도']})")
    
    with risk_tabs[1]:
        st.subheader("🛡️ 위험별 대응 전략")
        
        risk_strategies = {
            "🔧 기술적 위험": [
                "다중 기술 경로 동시 개발로 실패 위험 분산",
                "단계별 검증을 통한 조기 위험 발견",
                "외부 전문기관과의 기술 협력",
                "충분한 예비 연구 기간 확보"
            ],
            "📈 시장 위험": [
                "다양한 산업 분야로 적용 확대",
                "고객사와의 사전 수요 확약",
                "해외 시장 진출을 통한 리스크 분산",
                "유연한 사업 모델 적용"
            ],
            "💰 재정적 위험": [
                "단계별 자금 조달 계획 수립",
                "정부 R&D 지원 사업 적극 활용",
                "전략적 투자자 유치",
                "조기 수익 창출 모델 개발"
            ],
            "👥 인력 위험": [
                "핵심 인력 장기 계약 체결",
                "경쟁력 있는 보상 체계 구축",
                "지속적인 교육 및 역량 개발",
                "백업 인력 확보 및 양성"
            ],
            "📋 규제 위험": [
                "관련 법규 사전 검토 및 대응",
                "정부 및 규제기관과의 소통",
                "안전 기준 준수 및 인증 획득",
                "국제 표준 동향 지속 모니터링"
            ],
            "🏆 경쟁 위험": [
                "차별화된 기술 및 서비스 개발",
                "빠른 시장 진입을 통한 선점",
                "강력한 지적재산권 포트폴리오",
                "전략적 파트너십 구축"
            ]
        }
        
        for risk_type, strategies in risk_strategies.items():
            with st.expander(risk_type):
                for strategy in strategies:
                    st.markdown(f"• {strategy}")
    
    with risk_tabs[2]:
        st.subheader("📊 위험 모니터링 체계")
        
        monitoring_system = [
            "**📅 정기 위험 평가**",
            "• 월별 위험 요소 모니터링 회의",
            "• 분기별 종합 위험 평가 실시",
            "• 연간 위험 관리 계획 수정",
            "",
            "**🚨 조기 경보 시스템**",
            "• 핵심 지표 실시간 모니터링",
            "• 임계치 도달 시 자동 알림",
            "• 신속한 대응팀 가동",
            "",
            "**📈 위험 지표 관리**",
            "• 기술 개발 진도율",
            "• 예산 집행률 및 잔여 자금",
            "• 핵심 인력 이탈률",
            "• 시장 변화 및 경쟁사 동향",
            "",
            "**📋 문서화 및 보고**",
            "• 위험 관리 이력 체계적 기록",
            "• 정기 위험 관리 보고서 작성",
            "• 교훈 사항 정리 및 공유"
        ]
        
        for item in monitoring_system:
            if item.startswith("**"):
                st.markdown(item)
            elif item.startswith("•"):
                st.markdown(f"  {item}")
            else:
                st.markdown(item)

# 메인 실행
if __name__ == "__main__":
    display_laser_technology_project()
