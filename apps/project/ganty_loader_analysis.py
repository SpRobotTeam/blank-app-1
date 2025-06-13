import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def ganty_loader_analysis():
    """GANTY-LODER 프로젝트 분석 도구"""
    
    st.title("🏭 GANTY-LODER 프로젝트 분석")
    st.markdown("---")
    
    try:
        # 데이터 로드
        data = load_project_data()
        
        if data:
            # 탭 구성
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📊 프로젝트 개요", 
                "🔧 기계 어셈블리", 
                "💰 전체 구성", 
                "💎 고가 품목", 
                "🛠️ 서비스 내역",
                "📈 분석 차트"
            ])
            
            with tab1:
                display_project_overview(data['overview'])
            
            with tab2:
                display_assembly_analysis(data['assembly'])
            
            with tab3:
                display_project_composition(data['composition'])
            
            with tab4:
                display_expensive_items(data['expensive'])
            
            with tab5:
                display_service_details(data['service'])
            
            with tab6:
                display_analysis_charts(data)
        
        else:
            st.error("데이터를 로드할 수 없습니다.")
            st.info("data 폴더에 CSV 파일들이 있는지 확인해주세요.")
    
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

def load_project_data():
    """프로젝트 데이터 로드"""
    try:
        data = {}
        
        # 각 CSV 파일 로드
        data_files = {
            'overview': 'data/project_overview.csv',
            'assembly': 'data/assembly_data.csv',
            'composition': 'data/project_composition.csv',
            'expensive': 'data/expensive_items.csv',
            'service': 'data/service_details.csv'
        }
        
        for key, file_path in data_files.items():
            if os.path.exists(file_path):
                data[key] = pd.read_csv(file_path, encoding='utf-8')
            else:
                st.warning(f"파일을 찾을 수 없습니다: {file_path}")
                return None
        
        return data
    
    except Exception as e:
        st.error(f"데이터 로드 오류: {str(e)}")
        return None

def display_project_overview(df):
    """프로젝트 개요 표시"""
    st.subheader("🎯 프로젝트 개요")
    
    # 메트릭 카드 표시
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        total_amount = 980181870
        make_amount = 300063870
        buy_amount = 680118000
        make_ratio = 30.6
        
        with col1:
            st.metric(
                "총 프로젝트 금액",
                f"{total_amount:,}원",
                delta="9.8억원 규모"
            )
        
        with col2:
            st.metric(
                "제작/서비스 금액",
                f"{make_amount:,}원",
                delta=f"{make_ratio}%"
            )
        
        with col3:
            st.metric(
                "구매 금액",
                f"{buy_amount:,}원",
                delta=f"{100-make_ratio}%"
            )
        
        with col4:
            st.metric(
                "프로젝트 성격",
                "턴키 프로젝트",
                delta="완전 솔루션"
            )
    
    except Exception as e:
        st.error(f"개요 표시 오류: {str(e)}")
    
    st.markdown("---")
    
    # 상세 정보 테이블
    st.markdown("### 📋 상세 정보")
    
    # 데이터프레임 스타일링
    styled_df = df.copy()
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=200
    )

def display_assembly_analysis(df):
    """기계 어셈블리 분석"""
    st.subheader("🔧 기계 어셈블리 분석")
    
    # 어셈블리별 비용 분석
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 파이 차트 - 어셈블리별 금액 비율
        fig = px.pie(
            df, 
            values='총 금액 (원)', 
            names='어셈블리',
            title="어셈블리별 금액 분포",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 제작 비율 순위
        st.markdown("### 📊 제작 비율 순위")
        sorted_df = df.sort_values('제작 비율 (%)', ascending=False)
        
        for _, row in sorted_df.iterrows():
            st.metric(
                row['어셈블리'],
                f"{row['제작 비율 (%)']}%",
                delta=f"{row['총 금액 (원)']:,}원"
            )
    
    st.markdown("---")
    
    # 상세 테이블
    st.markdown("### 📋 어셈블리 상세 분석")
    
    # 금액 포맷팅
    display_df = df.copy()
    display_df['총 금액 (원)'] = display_df['총 금액 (원)'].apply(lambda x: f"{x:,}")
    display_df['제작/서비스 (원)'] = display_df['제작/서비스 (원)'].apply(lambda x: f"{x:,}")
    display_df['구매 금액 (원)'] = display_df['구매 금액 (원)'].apply(lambda x: f"{x:,}")
    
    st.dataframe(display_df, use_container_width=True)

def display_project_composition(df):
    """전체 프로젝트 구성 분석"""
    st.subheader("💰 전체 프로젝트 구성")
    
    # 구성 비율 차트
    col1, col2 = st.columns(2)
    
    with col1:
        # 전체 비율 파이 차트
        fig = px.pie(
            df[df['구분'] != '총계'], 
            values='전체 비율 (%)', 
            names='구분',
            title="프로젝트 구성 비율",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 제작 vs 구매 비율
        fig = px.bar(
            df[df['구분'] != '총계'],
            x='구분',
            y=['제작/서비스 (원)', '구매 금액 (원)'],
            title="구분별 제작 vs 구매 금액",
            barmode='stack',
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 상세 테이블
    st.markdown("### 📋 구성 상세 분석")
    
    # 금액 포맷팅
    display_df = df.copy()
    for col in ['총 금액 (원)', '제작/서비스 (원)', '구매 금액 (원)']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,}")
    
    st.dataframe(display_df, use_container_width=True)

def display_expensive_items(df):
    """고가 품목 분석"""
    st.subheader("💎 고가 품목 분석")
    
    # 고가 품목 차트
    fig = px.bar(
        df,
        x='품목명',
        y='금액 (원)',
        color='구분',
        title="고가 품목별 금액",
        text='금액 (원)',
        color_discrete_sequence=['#FF9999', '#66B2FF']
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(height=500, xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 구매 vs 제작 요약
    col1, col2 = st.columns(2)
    
    with col1:
        buy_items = df[df['구분'] == '구매']
        total_buy = buy_items['금액 (원)'].sum()
        st.metric(
            "구매 품목 총액",
            f"{total_buy:,}원",
            delta=f"{len(buy_items)}개 품목"
        )
    
    with col2:
        make_items = df[df['구분'] == '제작']
        total_make = make_items['금액 (원)'].sum()
        st.metric(
            "제작 품목 총액",
            f"{total_make:,}원",
            delta=f"{len(make_items)}개 품목"
        )
    
    # 상세 테이블
    st.markdown("### 📋 고가 품목 상세")
    display_df = df.copy()
    display_df['금액 (원)'] = display_df['금액 (원)'].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, use_container_width=True)

def display_service_details(df):
    """서비스 상세 내역"""
    st.subheader("🛠️ 서비스 상세 내역")
    
    # 서비스 비용 차트
    fig = px.bar(
        df,
        x='서비스 구분',
        y='금액 (원)',
        title="서비스별 금액",
        text='금액 (원)',
        color='비율 (%)',
        color_continuous_scale='Viridis'
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 서비스 요약
    total_service = df['금액 (원)'].sum()
    total_ratio = df['비율 (%)'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "총 서비스 금액",
            f"{total_service:,}원",
            delta=f"{total_ratio}%"
        )
    
    with col2:
        max_service = df.loc[df['금액 (원)'].idxmax()]
        st.metric(
            "최대 서비스",
            max_service['서비스 구분'],
            delta=f"{max_service['금액 (원)']:,}원"
        )
    
    with col3:
        st.metric(
            "서비스 항목 수",
            f"{len(df)}개",
            delta="전문 서비스"
        )
    
    # 상세 테이블
    st.markdown("### 📋 서비스 상세 내용")
    display_df = df.copy()
    display_df['금액 (원)'] = display_df['금액 (원)'].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, use_container_width=True)

def display_analysis_charts(data):
    """종합 분석 차트"""
    st.subheader("📈 종합 분석 차트")
    
    # 전체 프로젝트 구조 시각화
    composition_df = data['composition']
    assembly_df = data['assembly']
    
    # 1. 전체 구조 트리맵
    st.markdown("### 🗺️ 프로젝트 구조 트리맵")
    
    # 트리맵용 데이터 준비
    treemap_data = []
    
    # 어셈블리 데이터 추가
    for _, row in assembly_df.iterrows():
        treemap_data.append({
            'labels': row['어셈블리'],
            'parents': '기계 어셈블리',
            'values': row['총 금액 (원)'],
            'type': '어셈블리'
        })
    
    # 전체 구성 데이터 추가
    for _, row in composition_df[composition_df['구분'] != '총계'].iterrows():
        if row['구분'] != '기계 어셈블리':
            treemap_data.append({
                'labels': row['구분'],
                'parents': '전체 프로젝트',
                'values': row['총 금액 (원)'],
                'type': '구성'
            })
    
    # 루트 추가
    treemap_data.append({
        'labels': '전체 프로젝트',
        'parents': '',
        'values': 980181870,
        'type': '루트'
    })
    
    treemap_data.append({
        'labels': '기계 어셈블리',
        'parents': '전체 프로젝트',
        'values': 640181870,
        'type': '구성'
    })
    
    treemap_df = pd.DataFrame(treemap_data)
    
    fig = go.Figure(go.Treemap(
        labels=treemap_df['labels'],
        parents=treemap_df['parents'],
        values=treemap_df['values'],
        textinfo="label+value+percent parent",
        maxdepth=3,
        hovertemplate='<b>%{label}</b><br>금액: %{value:,}원<br>비율: %{percentParent}<extra></extra>'
    ))
    
    fig.update_layout(
        title="GANTY-LODER 프로젝트 구조",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. 제작 vs 구매 비교 분석
    st.markdown("### ⚖️ 제작 vs 구매 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 어셈블리별 제작 비율
        fig = px.bar(
            assembly_df,
            x='어셈블리',
            y='제작 비율 (%)',
            title="어셈블리별 제작 비율",
            color='제작 비율 (%)',
            color_continuous_scale='RdYlBu_r'
        )
        fig.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 전체 제작 vs 구매 도넛 차트
        labels = ['제작/서비스', '구매']
        values = [300063870, 680118000]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.3,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>%{value:,}원'
        )])
        
        fig.update_layout(
            title="전체 제작 vs 구매 비율",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3. 프로젝트 특성 분석
    st.markdown("### 🎯 프로젝트 특성 분석")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🏭 기술적 특성**
        - 고도 자동화 시스템
        - ABB 로봇 + LINCOLN 용접기
        - 다축 동시 제어
        - 갠트리 타입 구조
        """)
    
    with col2:
        st.success("""
        **💰 비용 구조 특성**
        - 장비 집약적 (65.3%)
        - 서비스 비중 높음 (25.5%)
        - 완성품 공급 방식
        - 턴키 프로젝트 성격
        """)
    
    with col3:
        st.warning("""
        **🛡️ 리스크 관리**
        - 브랜드 부품 사용
        - 전문 설치/시운전팀
        - 충분한 후처리 예산
        - 품질 보증 체계
        """)

if __name__ == "__main__":
    ganty_loader_analysis()
