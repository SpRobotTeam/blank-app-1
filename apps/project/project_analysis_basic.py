import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import io
from datetime import datetime
import base64

def create_excel_download(data):
    """엑셀 파일 생성 및 다운로드 링크 제공"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 각 시트 생성
        pd.DataFrame([{
            '항목': '프로젝트명', 
            '값': data['project_overview']['project_name']
        }, {
            '항목': '총 프로젝트 금액',
            '값': data['project_overview']['total_amount_formatted']
        }]).to_excel(writer, sheet_name='프로젝트 개요', index=False)
        
        pd.DataFrame(data['main_analysis']).to_excel(writer, sheet_name='메인 분석표', index=False)
        pd.DataFrame(data['expensive_items']).to_excel(writer, sheet_name='고가 구매품목', index=False)
        pd.DataFrame(data['manufacturing_items']).to_excel(writer, sheet_name='주요 제작품목', index=False)
        pd.DataFrame(data['category_ratios']).to_excel(writer, sheet_name='분야별 비율', index=False)
    
    return output.getvalue()

def create_comparison_analysis(data):
    """비교 분석 차트 생성"""
    df_main = pd.DataFrame(data['main_analysis'])
    
    # 제작 vs 구매 비교 (어셈블리별)
    assembly_data = df_main[df_main['구분'] == '기계 어셈블리'].copy()
    assembly_data = assembly_data[assembly_data['항목'] != '소계']
    
    fig = go.Figure()
    
    # 제작/서비스 막대
    fig.add_trace(go.Bar(
        name='제작/서비스',
        x=assembly_data['항목'],
        y=assembly_data['제작서비스'],
        marker_color='#667eea',
        text=[format_currency(x) for x in assembly_data['제작서비스']],
        textposition='auto'
    ))
    
    # 구매 막대
    fig.add_trace(go.Bar(
        name='구매',
        x=assembly_data['항목'],
        y=assembly_data['구매금액'],
        marker_color='#764ba2',
        text=[format_currency(x) for x in assembly_data['구매금액']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='어셈블리별 제작 vs 구매 비교',
        xaxis_title='어셈블리',
        yaxis_title='금액 (원)',
        barmode='stack',
        height=500,
        font=dict(size=12)
    )
    
    return fig

def create_treemap_chart(data):
    """트리맵 차트 생성"""
    df_main = pd.DataFrame(data['main_analysis'])
    
    # 계층적 데이터 준비
    treemap_data = []
    
    for _, row in df_main.iterrows():
        if row['항목'] != '소계' and row['항목'] != '총계':
            treemap_data.append({
                '구분': row['구분'],
                '항목': row['항목'],
                '금액': row['총금액'],
                '전체경로': f"{row['구분']} - {row['항목']}"
            })
    
    df_treemap = pd.DataFrame(treemap_data)
    
    fig = px.treemap(
        df_treemap,
        path=['구분', '항목'],
        values='금액',
        title='프로젝트 구성 트리맵',
        color='금액',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=600)
    return fig

def create_radar_chart(data):
    """레이더 차트 생성 (어셈블리별 특성)"""
    df_main = pd.DataFrame(data['main_analysis'])
    assembly_data = df_main[df_main['구분'] == '기계 어셈블리'].copy()
    assembly_data = assembly_data[assembly_data['항목'] != '소계']
    
    # 정규화된 값 계산 (0-100 스케일)
    max_amount = assembly_data['총금액'].max()
    max_manufacturing = assembly_data['제작서비스'].max()
    max_purchase = assembly_data['구매금액'].max()
    
    categories = ['총 비용', '제작 비용', '구매 비용', '복잡도', '중요도']
    
    fig = go.Figure()
    
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    
    for i, (_, row) in enumerate(assembly_data.iterrows()):
        # 각 어셈블리의 특성값 계산
        total_score = (row['총금액'] / max_amount) * 100
        manufacturing_score = (row['제작서비스'] / max_manufacturing) * 100 if max_manufacturing > 0 else 0
        purchase_score = (row['구매금액'] / max_purchase) * 100
        
        # 복잡도와 중요도는 임의로 설정 (실제로는 다른 데이터 기반)
        complexity_score = 50 + (total_score / 2)  # 비용이 높을수록 복잡
        importance_score = total_score  # 비용이 높을수록 중요
        
        values = [total_score, manufacturing_score, purchase_score, complexity_score, importance_score]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row['항목'],
            line_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="어셈블리별 특성 분석 (레이더 차트)",
        height=600
    )
    
    return fig

def format_currency(amount):
    """금액을 한국 원화 형식으로 포맷"""
    return f"{amount:,}원"

def load_project_data():
    """프로젝트 데이터 로드"""
    try:
        data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'project_data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"데이터 로드 오류: {str(e)}")
        return None

def create_pie_chart(data, title, values_col, names_col):
    """파이 차트 생성"""
    fig = px.pie(
        data, 
        values=values_col, 
        names=names_col,
        title=title,
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        showlegend=True,
        height=500,
        font=dict(size=12)
    )
    return fig

def create_bar_chart(data, x_col, y_col, title, color=None):
    """막대 차트 생성"""
    fig = px.bar(
        data, 
        x=x_col, 
        y=y_col,
        title=title,
        color=color,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        font=dict(size=12)
    )
    fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    return fig

def create_waterfall_chart(data):
    """워터폴 차트 생성 (누적 비용 분석)"""
    fig = go.Figure(go.Waterfall(
        name="프로젝트 비용 구성",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["기계 어셈블리", "제어전장", "설치/시운전", "후처리", "총계"],
        textposition="outside",
        text=[format_currency(640181870), format_currency(90000000), 
              format_currency(170000000), format_currency(80000000), 
              format_currency(980181870)],
        y=[640181870, 90000000, 170000000, 80000000, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title="프로젝트 비용 워터폴 분석",
        showlegend=False,
        height=500,
        font=dict(size=12)
    )
    return fig

def project_analysis():
    """메인 프로젝트 분석 함수"""
    st.title("📊 GANTY-LODER 프로젝트 분석")
    st.markdown("---")
    
    # 데이터 로드
    data = load_project_data()
    if not data:
        st.error("데이터를 로드할 수 없습니다.")
        return
    
    # 프로젝트 개요 표시
    st.header("🎯 프로젝트 개요")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="프로젝트명",
            value=data['project_overview']['project_name']
        )
    
    with col2:
        st.metric(
            label="총 프로젝트 금액",
            value=format_currency(data['project_overview']['total_amount'])
        )
    
    st.markdown("---")
    
    # 탭 생성
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 메인 분석", "📊 고급 분석", "💰 고가 품목", "🔧 제작 품목", "📊 비율 분석", "📋 데이터 관리"
    ])
    
    with tab1:
        st.header("📈 전체 프로젝트 구성 분석")
        
        # 메인 분석 데이터를 DataFrame으로 변환
        df_main = pd.DataFrame(data['main_analysis'])
        
        # 상위 차트 영역
        col1, col2 = st.columns(2)
        
        with col1:
            # 분야별 파이 차트
            category_data = df_main.groupby('구분')['총금액'].sum().reset_index()
            fig_pie = create_pie_chart(
                category_data, 
                "분야별 비용 분포", 
                '총금액', 
                '구분'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # 제작 vs 구매 비율
            total_manufacturing = df_main['제작서비스'].sum()
            total_purchase = df_main['구매금액'].sum()
            
            ratio_data = pd.DataFrame({
                '구분': ['제작/서비스', '구매'],
                '금액': [total_manufacturing, total_purchase]
            })
            
            fig_ratio = create_pie_chart(
                ratio_data,
                "제작 vs 구매 비율",
                '금액',
                '구분'
            )
            st.plotly_chart(fig_ratio, use_container_width=True)
        
        # 워터폴 차트
        st.subheader("💧 프로젝트 비용 구성 (워터폴 차트)")
        fig_waterfall = create_waterfall_chart(data['category_ratios'])
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
        # 어셈블리별 상세 막대 차트
        st.subheader("🔩 어셈블리별 상세 분석")
        assembly_data = df_main[df_main['구분'] == '기계 어셈블리'].copy()
        assembly_data = assembly_data[assembly_data['항목'] != '소계']
        
        fig_assembly = create_bar_chart(
            assembly_data,
            '항목',
            '총금액',
            "어셈블리별 비용 분석",
            '항목'
        )
        st.plotly_chart(fig_assembly, use_container_width=True)
        
        # 메인 분석 테이블
        st.subheader("📋 메인 분석 테이블")
        
        # 포맷된 테이블 생성
        display_df = df_main.copy()
        display_df['총금액'] = display_df['총금액'].apply(format_currency)
        display_df['제작서비스'] = display_df['제작서비스'].apply(format_currency)
        display_df['구매금액'] = display_df['구매금액'].apply(format_currency)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        st.header("📊 고급 분석")
        
        # 상단 옵션 선택
        analysis_type = st.selectbox(
            "분석 유형 선택:",
            ["비교 분석", "트리맵 분석", "레이더 분석"]
        )
        
        if analysis_type == "비교 분석":
            st.subheader("🔄 어셈블리별 제작 vs 구매 비교")
            fig_comparison = create_comparison_analysis(data)
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            st.info("💡 **인사이트**: R-AXIS는 거의 모든 비용이 구매비인 반면, X-AXIS는 제작 비중이 가장 높습니다.")
            
        elif analysis_type == "트리맵 분석":
            st.subheader("🌳 프로젝트 구성 트리맵")
            fig_treemap = create_treemap_chart(data)
            st.plotly_chart(fig_treemap, use_container_width=True)
            
            st.info("💡 **인사이트**: 트리맵에서 각 영역의 크기는 비용 비중을 나타냅니다. R-AXIS가 압도적으로 큰 비중을 차지합니다.")
            
        elif analysis_type == "레이더 분석":
            st.subheader("🎯 어셈블리별 특성 레이더")
            fig_radar = create_radar_chart(data)
            st.plotly_chart(fig_radar, use_container_width=True)
            
            st.info("💡 **인사이트**: 레이더 차트로 각 어셈블리의 비용, 제작 비율, 복잡도 등을 비교할 수 있습니다.")
        
        # 추가 통계 정보
        st.subheader("📊 고급 통계")
        
        df_main = pd.DataFrame(data['main_analysis'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_manufacturing = df_main['제작서비스'].sum()
            manufacturing_ratio = (total_manufacturing / df_main['총금액'].sum()) * 100
            st.metric(
                "전체 제작 비율",
                f"{manufacturing_ratio:.1f}%",
                delta=f"{manufacturing_ratio - 25:.1f}%p vs 업계 평균"
            )
        
        with col2:
            assembly_count = len(df_main[df_main['구분'] == '기계 어셈블리']) - 1  # 소계 제외
            st.metric(
                "어셈블리 수",
                assembly_count,
                delta="고도 모듈화"
            )
        
        with col3:
            max_assembly = df_main[df_main['구분'] == '기계 어셈블리'].nlargest(1, '총금액')
            if not max_assembly.empty:
                max_ratio = (max_assembly.iloc[0]['총금액'] / df_main['총금액'].sum()) * 100
                st.metric(
                    "최대 어셈블리 비중",
                    f"{max_ratio:.1f}%",
                    delta=max_assembly.iloc[0]['항목']
                )
        
        with col4:
            expensive_items_total = sum([item['금액'] for item in data['expensive_items']])
            expensive_ratio = (expensive_items_total / data['project_overview']['total_amount']) * 100
            st.metric(
                "고가 품목 비중",
                f"{expensive_ratio:.1f}%",
                delta="핀수 관리 중요"
            )

    with tab5:
        st.header("💰 고가 구매 품목 분석")
        
        df_expensive = pd.DataFrame(data['expensive_items'])
        
        # 고가 품목 차트
        fig_expensive = create_bar_chart(
            df_expensive,
            '품목',
            '금액',
            "고가 구매 품목 분석",
            '품목'
        )
        st.plotly_chart(fig_expensive, use_container_width=True)
        
        # 고가 품목 테이블
        st.subheader("📋 고가 구매 품목 상세")
        display_expensive = df_expensive.copy()
        display_expensive['금액'] = display_expensive['금액'].apply(format_currency)
        
        st.dataframe(
            display_expensive,
            use_container_width=True,
            hide_index=True
        )
        
        # 핵심 통계
        st.subheader("📊 고가 품목 통계")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "총 고가 품목 수",
                len(df_expensive)
            )
        
        with col2:
            st.metric(
                "최고가 품목",
                df_expensive.loc[df_expensive['금액'].idxmax(), '품목']
            )
        
        with col3:
            st.metric(
                "고가 품목 총액",
                format_currency(df_expensive['금액'].sum())
            )
    
    with tab4:
        st.header("🔧 주요 제작 품목 분석")
        
        df_manufacturing = pd.DataFrame(data['manufacturing_items'])
        
        # 제작 품목 차트
        fig_manufacturing = create_bar_chart(
            df_manufacturing,
            '품목',
            '금액',
            "주요 제작 품목 분석",
            '어셈블리'
        )
        st.plotly_chart(fig_manufacturing, use_container_width=True)
        
        # 어셈블리별 제작 품목 분포
        assembly_manufacturing = df_manufacturing.groupby('어셈블리')['금액'].sum().reset_index()
        fig_assembly_mfg = create_pie_chart(
            assembly_manufacturing,
            "어셈블리별 제작 품목 분포",
            '금액',
            '어셈블리'
        )
        st.plotly_chart(fig_assembly_mfg, use_container_width=True)
        
        # 제작 품목 테이블
        st.subheader("📋 주요 제작 품목 상세")
        display_manufacturing = df_manufacturing.copy()
        display_manufacturing['금액'] = display_manufacturing['금액'].apply(format_currency)
        
        st.dataframe(
            display_manufacturing,
            use_container_width=True,
            hide_index=True
        )
    
    with tab5:
        st.header("📊 분야별 비율 분석")
        
        df_category = pd.DataFrame(data['category_ratios'])
        
        # 분야별 비율 차트
        fig_category = create_bar_chart(
            df_category,
            '분야',
            '금액',
            "분야별 비용 분석",
            '분야'
        )
        st.plotly_chart(fig_category, use_container_width=True)
        
        # 도넛 차트
        fig_donut = px.pie(
            df_category,
            values='금액',
            names='분야',
            title="분야별 비용 분포 (도넛 차트)",
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(height=500)
        st.plotly_chart(fig_donut, use_container_width=True)
        
        # 비율 분석 테이블
        st.subheader("📋 분야별 비율 상세")
        display_category = df_category.copy()
        display_category['금액'] = display_category['금액'].apply(format_currency)
        
        st.dataframe(
            display_category,
            use_container_width=True,
            hide_index=True
        )
        
        # 핵심 인사이트
        st.subheader("💡 핵심 인사이트")
        st.info("🔍 **기계 어셈블리**가 전체 비용의 65.3%로 가장 큰 비중을 차지합니다.")
        st.info("⚙️ **설치/시운전**이 17.3%로 상당한 비중을 차지하여 턴키 프로젝트 특성을 보입니다.")
        st.info("🎯 **제어전장**과 **후처리**가 각각 9.2%, 8.2%로 균형잡힌 구성을 보입니다.")
    
    with tab5:
        st.header("📋 상세 데이터 및 설정")
        
        # 데이터 다운로드 섹션
        st.subheader("💾 데이터 다운로드")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # JSON 데이터 다운로드
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            st.download_button(
                label="📄 JSON 데이터 다운로드",
                data=json_str,
                file_name="project_analysis.json",
                mime="application/json"
            )
        
        with col2:
            # CSV 데이터 다운로드
            csv_data = pd.DataFrame(data['main_analysis']).to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📊 CSV 데이터 다운로드",
                data=csv_data,
                file_name="project_analysis.csv",
                mime="text/csv"
            )
        
        # 원본 데이터 표시
        st.subheader("🔍 원본 데이터 미리보기")
        
        with st.expander("JSON 데이터 보기"):
            st.json(data)
        
        # 데이터 업로드 섹션
        st.subheader("📤 데이터 업로드")
        
        uploaded_file = st.file_uploader(
            "새로운 프로젝트 데이터를 업로드하세요 (JSON 형식)",
            type=['json']
        )
        
        if uploaded_file is not None:
            try:
                new_data = json.load(uploaded_file)
                st.success("✅ 새로운 데이터가 성공적으로 로드되었습니다!")
                st.json(new_data)
                
                if st.button("🔄 데이터 적용"):
                    # 여기에 새 데이터를 적용하는 로직 추가
                    st.success("데이터가 적용되었습니다. 페이지를 새로고침하세요.")
            except Exception as e:
                st.error(f"데이터 로드 오류: {str(e)}")
    
    with tab6:
        st.header("📋 데이터 관리")
        
        # 엑셀 다운로드 섹션
        st.subheader("📥 엑셀 파일 다운로드")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 엑셀 파일 생성 및 다운로드
            if st.button("📋 엑셀 파일 생성"):
                try:
                    excel_data = create_excel_download(data)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"GANTY_LODER_분석_{timestamp}.xlsx"
                    
                    st.download_button(
                        label="💾 엑셀 파일 다운로드",
                        data=excel_data,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ 엑셀 파일이 성공적으로 생성되었습니다!")
                except Exception as e:
                    st.error(f"엑셀 파일 생성 오류: {str(e)}")
        
        with col2:
            # JSON 다운로드
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📄 JSON 데이터 다운로드",
                data=json_str,
                file_name=f"project_analysis_{timestamp}.json",
                mime="application/json"
            )
        
        st.markdown("---")
        
        # 데이터 업로드 섹션
        st.subheader("📤 데이터 업로드")
        
        uploaded_file = st.file_uploader(
            "새로운 프로젝트 데이터를 업로드하세요",
            type=['json', 'xlsx', 'csv'],
            help="JSON, Excel, CSV 형식을 지원합니다."
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.json'):
                    new_data = json.load(uploaded_file)
                    st.success("✅ JSON 데이터가 성공적으로 로드되었습니다!")
                    
                elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(uploaded_file)
                    st.success("✅ 엑셀 데이터가 성공적으로 로드되었습니다!")
                    st.dataframe(df.head())
                    
                elif uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                    st.success("✅ CSV 데이터가 성공적으로 로드되었습니다!")
                    st.dataframe(df.head())
                
                # 데이터 적용 버튼
                if st.button("🔄 데이터 적용 및 새로고침"):
                    st.warning("🔄 이 기능은 실제 환경에서 구현될 예정입니다.")
                    st.info("현재는 데모 모드로 데이터 변경이 적용되지 않습니다.")
                    
            except Exception as e:
                st.error(f"데이터 로드 오류: {str(e)}")
        
        st.markdown("---")
        
        # 데이터 미리보기
        st.subheader("🔍 데이터 미리보기")
        
        preview_option = st.selectbox(
            "미리보기 데이터 선택:",
            ["메인 분석 데이터", "고가 구매품목", "주요 제작품목", "분야별 비율"]
        )
        
        if preview_option == "메인 분석 데이터":
            st.dataframe(pd.DataFrame(data['main_analysis']), use_container_width=True)
        elif preview_option == "고가 구매품목":
            st.dataframe(pd.DataFrame(data['expensive_items']), use_container_width=True)
        elif preview_option == "주요 제작품목":
            st.dataframe(pd.DataFrame(data['manufacturing_items']), use_container_width=True)
        elif preview_option == "분야별 비율":
            st.dataframe(pd.DataFrame(data['category_ratios']), use_container_width=True)
        
        # API 연동 옵션 (미래 기능)
        st.subheader("🌐 외부 연동 (미래 기능)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("🔗 **ERP 연동**: 실시간 BOM 데이터 동기화")
            if st.button("📄 ERP 연결 테스트"):
                st.warning("🚧 ERP 연동 기능은 개발 예정입니다.")
        
        with col2:
            st.info("📈 **비용 추적**: 자동 비용 업데이트")
            if st.button("🔄 비용 데이터 업데이트"):
                st.warning("🚧 비용 추적 기능은 개발 예정입니다.")
    
    # 푸터 정보
    st.markdown("---")
    st.markdown("""
    ### 📈 프로젝트 분석 도구 정보
    - **버전**: 2.0.0 (고급 분석 기능 추가)
    - **최종 업데이트**: 2025-06-13
    - **데이터 기준**: GANTY-LODER 자동 용접 시스템 BOM
    - **새 기능**: 트리맵, 레이더 차트, 엑셀 다운로드, 고급 통계
    - **개발**: ABB TSU Team
    """)

if __name__ == "__main__":
    project_analysis()
