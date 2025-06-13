import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import io

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

def load_excel_data(uploaded_file):
    """업로드된 엑셀 파일에서 데이터 로드"""
    try:
        # 엑셀 파일의 모든 시트 읽기
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        
        # 시트명 확인
        sheet_names = list(excel_data.keys())
        st.success(f"✅ 엑셀 파일을 성공적으로 로드했습니다! 시트: {sheet_names}")
        
        # 메인 분석 데이터 찾기
        main_data = None
        for sheet_name, df in excel_data.items():
            if '메인' in sheet_name or 'main' in sheet_name.lower() or '분석' in sheet_name:
                main_data = df
                break
        
        # 메인 데이터가 없으면 첫 번째 시트 사용
        if main_data is None:
            main_data = list(excel_data.values())[0]
        
        return excel_data, main_data
        
    except Exception as e:
        st.error(f"엑셀 파일 로드 오류: {str(e)}")
        return None, None

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

def analyze_uploaded_data(df):
    """업로드된 데이터 분석"""
    try:
        # 필수 컬럼 확인
        required_cols = ['구분', '항목', '총금액']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.warning(f"⚠️ 필수 컬럼이 누락되었습니다: {missing_cols}")
            st.info("💡 컬럼명을 다음과 같이 설정해주세요: 구분, 항목, 총금액, 제작서비스, 구매금액")
            return None
        
        # 데이터 정리
        df = df.dropna(subset=['총금액'])
        df['총금액'] = pd.to_numeric(df['총금액'], errors='coerce')
        
        # 제작서비스, 구매금액 컬럼이 없으면 생성
        if '제작서비스' not in df.columns:
            df['제작서비스'] = 0
        if '구매금액' not in df.columns:
            df['구매금액'] = df['총금액']
        
        # 숫자형 변환
        df['제작서비스'] = pd.to_numeric(df['제작서비스'], errors='coerce').fillna(0)
        df['구매금액'] = pd.to_numeric(df['구매금액'], errors='coerce').fillna(0)
        
        # 제작비율 계산
        df['제작비율_계산'] = (df['제작서비스'] / df['총금액'] * 100).round(1)
        df['제작비율_계산'] = df['제작비율_계산'].astype(str) + '%'
        
        return df
        
    except Exception as e:
        st.error(f"데이터 분석 오류: {str(e)}")
        return None

def project_analysis():
    """메인 프로젝트 분석 함수"""
    st.title("📊 GANTY-LODER 프로젝트 분석")
    st.markdown("---")
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs([
        "📁 기본 데이터 분석", "📤 파일 업로드 분석", "📋 도구 및 템플릿"
    ])
    
    with tab1:
        st.header("📈 기본 프로젝트 데이터 분석")
        
        # 기본 데이터 로드
        data = load_project_data()
        if not data:
            st.error("기본 데이터를 로드할 수 없습니다.")
            return
        
        # 프로젝트 개요 표시
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
        st.header("📤 엑셀 파일 업로드 분석")
        st.markdown("### 📄 BOM 데이터 파일을 업로드하여 분석해보세요")
        
        # 파일 업로드
        uploaded_file = st.file_uploader(
            "엑셀 파일을 선택하세요 (.xlsx, .xls)",
            type=['xlsx', 'xls'],
            help="BOM 데이터가 포함된 엑셀 파일을 업로드하세요"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ 파일 '{uploaded_file.name}'이 업로드되었습니다!")
            
            # 엑셀 데이터 로드
            excel_data, main_data = load_excel_data(uploaded_file)
            
            if excel_data is not None and main_data is not None:
                # 시트 선택
                sheet_names = list(excel_data.keys())
                if len(sheet_names) > 1:
                    selected_sheet = st.selectbox(
                        "분석할 시트를 선택하세요:",
                        sheet_names,
                        help="여러 시트가 있는 경우 분석할 시트를 선택하세요"
                    )
                    selected_data = excel_data[selected_sheet]
                else:
                    selected_data = main_data
                    selected_sheet = sheet_names[0]
                
                st.info(f"📊 선택된 시트: '{selected_sheet}' (행: {len(selected_data)}, 열: {len(selected_data.columns)})")
                
                # 데이터 미리보기
                st.subheader("🔍 데이터 미리보기")
                st.dataframe(selected_data.head(10))
                
                # 컬럼 정보
                st.subheader("📋 컬럼 정보")
                col_info = pd.DataFrame({
                    '컬럼명': selected_data.columns,
                    '데이터 타입': selected_data.dtypes,
                    '비어있지 않은 값': selected_data.count()
                })
                st.dataframe(col_info)
                
                # 데이터 분석
                st.subheader("📈 업로드 데이터 분석")
                
                analyzed_df = analyze_uploaded_data(selected_data)
                
                if analyzed_df is not None:
                    # 분석 결과 요약
                    total_amount = analyzed_df['총금액'].sum()
                    total_manufacturing = analyzed_df['제작서비스'].sum()
                    total_purchase = analyzed_df['구매금액'].sum()
                    
                    # 메트릭 표시
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "총 금액",
                            format_currency(total_amount)
                        )
                    
                    with col2:
                        st.metric(
                            "제작/서비스",
                            format_currency(total_manufacturing)
                        )
                    
                    with col3:
                        st.metric(
                            "구매 금액",
                            format_currency(total_purchase)
                        )
                    
                    with col4:
                        manufacturing_ratio = (total_manufacturing / total_amount * 100) if total_amount > 0 else 0
                        st.metric(
                            "제작 비율",
                            f"{manufacturing_ratio:.1f}%"
                        )
                    
                    # 차트 생성
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 구분별 파이 차트
                        if '구분' in analyzed_df.columns:
                            category_data = analyzed_df.groupby('구분')['총금액'].sum().reset_index()
                            fig_category = create_pie_chart(
                                category_data,
                                "구분별 비용 분포",
                                '총금액',
                                '구분'
                            )
                            st.plotly_chart(fig_category, use_container_width=True)
                    
                    with col2:
                        # 제작 vs 구매 비율
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
                    
                    # 항목별 막대 차트 (상위 10개)
                    st.subheader("📊 주요 항목별 분석 (상위 10개)")
                    top_items = analyzed_df.nlargest(10, '총금액')
                    
                    fig_bar = create_bar_chart(
                        top_items,
                        '항목',
                        '총금액',
                        "주요 항목별 비용 분석",
                        '구분' if '구분' in top_items.columns else None
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # 분석 결과 테이블
                    st.subheader("📋 분석 결과 테이블")
                    
                    # 표시용 데이터프레임 생성
                    display_analyzed = analyzed_df.copy()
                    for col in ['총금액', '제작서비스', '구매금액']:
                        if col in display_analyzed.columns:
                            display_analyzed[col] = display_analyzed[col].apply(format_currency)
                    
                    st.dataframe(
                        display_analyzed,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # 다운로드 버튼
                    st.subheader("💾 분석 결과 다운로드")
                    
                    # CSV 다운로드
                    csv_data = analyzed_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📊 분석 결과 CSV 다운로드",
                        data=csv_data,
                        file_name=f"analyzed_{uploaded_file.name.split('.')[0]}.csv",
                        mime="text/csv"
                    )
                    
                    # 엑셀 다운로드
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        analyzed_df.to_excel(writer, sheet_name='분석결과', index=False)
                        
                        # 요약 정보도 추가
                        summary_df = pd.DataFrame({
                            '항목': ['총 금액', '제작/서비스', '구매 금액', '제작 비율'],
                            '값': [
                                format_currency(total_amount),
                                format_currency(total_manufacturing),
                                format_currency(total_purchase),
                                f"{manufacturing_ratio:.1f}%"
                            ]
                        })
                        summary_df.to_excel(writer, sheet_name='요약', index=False)
                    
                    output.seek(0)
                    st.download_button(
                        label="📁 분석 결과 엑셀 다운로드",
                        data=output.getvalue(),
                        file_name=f"analyzed_{uploaded_file.name.split('.')[0]}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    with tab3:
        st.header("📋 도구 및 템플릿")
        
        # 템플릿 다운로드 섹션
        st.subheader("📄 BOM 분석 템플릿")
        st.markdown("""
        ### 📝 템플릿 사용 방법:
        1. **템플릿 다운로드**: 아래 버튼으로 빈 템플릿을 다운로드하세요
        2. **데이터 입력**: 엑셀에서 BOM 데이터를 입력하세요
        3. **파일 업로드**: '파일 업로드 분석' 탭에서 완성된 파일을 업로드하세요
        4. **분석 확인**: 자동으로 생성된 차트와 분석 결과를 확인하세요
        
        ### 📋 필수 컬럼:
        - **구분**: 기계 어셈블리, 전장 시스템, 설치/시운전 등
        - **항목**: SADDLE, CARRIAGE, Y-AXIS 등 구체적인 항목명
        - **총금액**: 해당 항목의 총 금액 (숫자만 입력)
        - **제작서비스**: 제작 또는 서비스 금액 (선택사항)
        - **구매금액**: 구매 금액 (선택사항)
        """)
        
        # 템플릿 생성 및 다운로드
        template_data = {
            '구분': ['기계 어셈블리', '전장 시스템', '설치/시운전', '후처리', ''],
            '항목': ['SADDLE', '제어전장 구매품', '기계설치시운전', '후처리 작업', ''],
            '총금액': [53070336, 90000000, 120000000, 80000000, 0],
            '제작서비스': [4977336, 0, 120000000, 80000000, 0],
            '구매금액': [48093000, 90000000, 0, 0, 0],
            '비고': ['예시 데이터', '예시 데이터', '예시 데이터', '예시 데이터', '']
        }
        
        template_df = pd.DataFrame(template_data)
        
        # 가이드 데이터
        guide_data = {
            '컬럼명': ['구분', '항목', '총금액', '제작서비스', '구매금액', '비고'],
            '설명': [
                '기계 어셈블리, 전장 시스템, 설치/시운전, 후처리 등',
                'SADDLE, CARRIAGE, Y-AXIS 등 구체적인 항목명',
                '해당 항목의 총 금액 (숫자만 입력)',
                '제작 또는 서비스 금액 (숫자만 입력, 선택사항)',
                '구매 금액 (숫자만 입력, 선택사항)',
                '추가 설명이나 메모 (선택사항)'
            ],
            '예시': [
                '기계 어셈블리',
                'SADDLE',
                '53070336',
                '4977336',
                '48093000',
                '새들 어셈블리'
            ]
        }
        guide_df = pd.DataFrame(guide_data)
        
        # 템플릿 미리보기
        st.subheader("👀 템플릿 미리보기")
        st.dataframe(template_df, use_container_width=True)
        
        # 가이드 표시
        st.subheader("📖 입력 가이드")
        st.dataframe(guide_df, use_container_width=True)
        
        # 템플릿 다운로드 버튼
        col1, col2 = st.columns(2)
        
        with col1:
            # 예시 데이터 포함 템플릿
            output_with_example = io.BytesIO()
            with pd.ExcelWriter(output_with_example, engine='openpyxl') as writer:
                template_df.to_excel(writer, sheet_name='BOM_데이터', index=False)
                guide_df.to_excel(writer, sheet_name='입력_가이드', index=False)
            
            output_with_example.seek(0)
            st.download_button(
                label="📊 예시 데이터 포함 템플릿 다운로드",
                data=output_with_example.getvalue(),
                file_name="bom_template_with_example.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="예시 데이터가 포함된 템플릿을 다운로드합니다"
            )
        
        with col2:
            # 빈 템플릿
            empty_template = template_df.copy()
            empty_template.loc[:, ['구분', '항목', '비고']] = ''
            empty_template.loc[:, ['총금액', '제작서비스', '구매금액']] = 0
            
            output_empty = io.BytesIO()
            with pd.ExcelWriter(output_empty, engine='openpyxl') as writer:
                empty_template.to_excel(writer, sheet_name='BOM_데이터', index=False)
                guide_df.to_excel(writer, sheet_name='입력_가이드', index=False)
            
            output_empty.seek(0)
            st.download_button(
                label="📄 빈 템플릿 다운로드",
                data=output_empty.getvalue(),
                file_name="bom_template_empty.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="빈 템플릿을 다운로드하여 직접 데이터를 입력하세요"
            )
        
        # 추가 도구
        st.subheader("🔧 추가 도구")
        
        with st.expander("💡 분석 팁"):
            st.markdown("""
            ### 📈 효과적인 BOM 분석을 위한 팁:
            
            1. **데이터 정확성**: 금액 데이터는 숫자만 입력하세요 (쉼표나 원화 기호 제외)
            2. **구분 통일**: 같은 카테고리는 동일한 이름으로 입력하세요
            3. **항목명 명확화**: 항목명은 구체적이고 이해하기 쉽게 작성하세요
            4. **제작/구매 구분**: 제작서비스와 구매금액을 명확히 구분하여 입력하세요
            5. **데이터 검증**: 총금액 = 제작서비스 + 구매금액이 되도록 확인하세요
            
            ### 🎯 분석 활용 방법:
            - **비용 구조 파악**: 전체 프로젝트에서 각 분야가 차지하는 비중 확인
            - **제작/구매 최적화**: 제작과 구매의 비율을 분석하여 비용 효율성 검토
            - **핵심 품목 식별**: 고가 품목들을 파악하여 리스크 관리 및 협상 포인트 도출
            - **프로젝트 계획**: 분석 결과를 바탕으로 향후 프로젝트 계획 수립
            """)
        
        with st.expander("❓ 자주 묻는 질문"):
            st.markdown("""
            ### ❓ FAQ:
            
            **Q: 어떤 파일 형식을 지원하나요?**
            A: .xlsx, .xls 엑셀 파일을 지원합니다.
            
            **Q: 여러 시트가 있는 파일도 분석 가능한가요?**
            A: 네, 가능합니다. 업로드 후 분석할 시트를 선택할 수 있습니다.
            
            **Q: 필수 컬럼이 없으면 어떻게 되나요?**
            A: '구분', '항목', '총금액' 컬럼은 필수입니다. 없으면 경고 메시지가 표시됩니다.
            
            **Q: 제작서비스나 구매금액 컬럼이 없어도 되나요?**
            A: 네, 선택사항입니다. 없으면 자동으로 0 또는 총금액으로 설정됩니다.
            
            **Q: 분석 결과를 저장할 수 있나요?**
            A: 네, CSV 또는 엑셀 형식으로 다운로드할 수 있습니다.
            """)
    
    # 푸터 정보
    st.markdown("---")
    st.markdown("""
    ### 📈 프로젝트 분석 도구 정보
    - **버전**: 2.0.0
    - **최종 업데이트**: 2025-06-13
    - **기능**: BOM 분석, 비용 구조 분석, 제작/구매 비율 분석
    - **개발**: ABB TSU Team
    """)

if __name__ == "__main__":
    project_analysis()
