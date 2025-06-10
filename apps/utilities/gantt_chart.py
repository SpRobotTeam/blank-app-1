import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from io import BytesIO
from datetime import datetime, timedelta, date
import os

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, error_handler, success_message, info_message
from utils.data_processing import safe_operation, create_download_link

@safe_operation
def gantt_chart():
    """
    프로젝트 일정 간트 차트 생성 도구
    Version: 3.0 - 공통 유틸리티 적용 및 UI/UX 개선
    """
    # 도구 헤더 적용
    tool_header(
        "프로젝트 진행 간트 차트", 
        "프로젝트 일정을 시각적으로 관리하고 진행 상황을 추적합니다. 엑셀 파일 업로드를 통해 간트 차트를 생성하고 실시간으로 진행률을 업데이트할 수 있습니다."
    )
    
    # 버전 정보 표시
    st.caption("🔄 Version 3.0 - 공통 유틸리티 적용 및 UI/UX 개선 (2025-06-10)")

    # 세션 상태 초기화
    if 'df_data' not in st.session_state:
        st.session_state.df_data = None
        st.session_state.file_uploaded = False

    # 컨트롤 패널
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # 파일 업로드 위젯
        uploaded_file = st.file_uploader(
            "📁 엑셀 파일을 업로드하세요", 
            type=['xlsx'], 
            key="gantt",
            help="간트 차트 생성을 위한 엑셀 파일을 업로드합니다."
        )
    
    with col2:
        # 날짜 마커 입력 위젯
        today = date.today()
        marker_date = st.date_input(
            "📅 기준 날짜 설정", 
            value=today, 
            key="marker_date",
            help="간트 차트에 표시할 기준 날짜를 선택합니다."
        )
    
    with col3:
        # 새로고침 버튼
        if st.button("🔄 새로고침", key="refresh_page", help="페이지를 새로고침합니다."):
            st.session_state.clear()
            st.experimental_rerun()

    # 파일 처리
    if uploaded_file is not None:
        df = process_uploaded_file(uploaded_file)
        if df is not None:
            display_gantt_chart(df, marker_date)
    else:
        display_template_info()

def process_uploaded_file(uploaded_file):
    """업로드된 파일 처리"""
    try:
        # 이미 처리된 파일인지 확인
        if not st.session_state.file_uploaded or st.session_state.df_data is None:
            with st.spinner("📊 엑셀 파일을 분석하는 중..."):
                # 엑셀 파일 읽기
                df = pd.read_excel(uploaded_file, engine='openpyxl')
                
                # 필수 컬럼 확인
                required_columns = ['Task', 'Start', 'End']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    error_handler(f"필수 컬럼이 누락되었습니다: {', '.join(missing_columns)}")
                    return None
                
                # 날짜 변환
                df = convert_date_columns(df)
                
                # 기본값 설정
                df = set_default_values(df)
                
                # 원본 순서 보존
                df['Original_Order'] = df.index
                
                # 세션 상태에 저장
                st.session_state.df_data = df
                st.session_state.file_uploaded = True
                
                success_message("파일이 성공적으로 업로드되었습니다. 엑셀 입력 순서로 정렬됩니다.")
        
        return st.session_state.df_data
        
    except Exception as e:
        error_handler(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {str(e)}")
        return None

def convert_date_columns(df):
    """날짜 컬럼 변환"""
    try:
        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])
        
        # 실제 시작일이 있으면 변환
        if 'Actual_Start' in df.columns:
            df['Actual_Start'] = pd.to_datetime(df['Actual_Start'])
        
        return df
    except Exception as e:
        raise ValueError(f"날짜 형식 변환 중 오류: {str(e)}")

def set_default_values(df):
    """기본값 설정"""
    # 진행률 기본값
    if 'Progress' not in df.columns:
        df['Progress'] = 0
    
    # 카테고리 자동 설정
    if 'Category' not in df.columns:
        df['Category'] = df['Task'].apply(lambda x: x.split('_')[0] if '_' in x else 'Unknown')
    
    return df

def display_gantt_chart(df, marker_date):
    """간트 차트 표시"""
    # 사이드바 설정
    display_sidebar_controls(df)
    
    # 데이터 정렬 (원본 순서 유지)
    sorted_df = df.sort_values(by='Original_Order') if 'Original_Order' in df.columns else df.copy()
    
    # 간트 차트 생성
    fig = create_gantt_chart(sorted_df, marker_date)
    
    # 차트 표시
    st.plotly_chart(fig, use_container_width=True)
    
    # 프로젝트 상태 분석
    display_project_analysis(sorted_df, marker_date)
    
    # 데이터 내보내기
    display_export_options(sorted_df)

def display_sidebar_controls(df):
    """사이드바 컨트롤 표시"""
    st.sidebar.header("⚙️ 설정 옵션")
    st.sidebar.info("💡 차트는 엑셀 파일에 입력된 순서대로 표시됩니다.")

    # 진행 상황 업데이트
    st.sidebar.subheader("📈 진행 상황 업데이트")
    
    # 작업 선택
    selected_task = st.sidebar.selectbox(
        "작업 선택", 
        options=df['Task'].tolist(),
        help="진행률을 업데이트할 작업을 선택하세요."
    )
    
    # 선택한 작업의 정보 가져오기
    task_idx = df[df['Task'] == selected_task].index[0]
    
    # 실제 시작일 설정
    actual_start_date = st.sidebar.date_input(
        "실제 시작일",
        value=df.at[task_idx, 'Actual_Start'] if pd.notna(df.at[task_idx, 'Actual_Start']) else df.at[task_idx, 'Start'],
        key="actual_start",
        help="작업의 실제 시작 날짜를 설정합니다."
    )
    
    # 진행률 설정
    progress = st.sidebar.slider(
        "진행률 (%)",
        min_value=0,
        max_value=100,
        value=int(df.at[task_idx, 'Progress']),
        key="progress_slider",
        help="작업의 현재 진행률을 설정합니다."
    )
    
    # 변경사항 적용
    if st.sidebar.button("✅ 변경사항 적용"):
        st.session_state.df_data.at[task_idx, 'Actual_Start'] = actual_start_date
        st.session_state.df_data.at[task_idx, 'Progress'] = progress
        st.sidebar.success(f"'{selected_task}'의 정보가 업데이트되었습니다.")
        st.experimental_rerun()

def create_gantt_chart(sorted_df, marker_date):
    """간트 차트 생성"""
    # 카테고리별 색상 지정
    category_colors = get_category_colors(sorted_df)
    
    # 기본 간트 차트 생성
    fig = px.timeline(
        sorted_df,
        x_start="Start",
        x_end="End",
        y="Task",
        color="Category",
        color_discrete_map=category_colors,
        labels={'Task': '작업', 'Start': '시작 날짜', 'End': '종료 날짜', 'Category': '카테고리'}
    )
    
    # 계획 일정을 연하게 표시
    fig.update_traces(opacity=0.4)
    
    # 레이아웃 설정
    fig = update_chart_layout(fig, sorted_df)
    
    # 실제 진행 상황 추가
    fig = add_actual_progress(fig, sorted_df, category_colors)
    
    # 날짜 마커 추가
    fig = add_date_marker(fig, marker_date)
    
    return fig

def get_category_colors(df):
    """카테고리별 색상 정의"""
    predefined_colors = {
        '기획': '#4e73df', '설계': '#1cc88a', '개발': '#f6c23e', '테스트': '#e74a3b',
        '운영': '#36b9cc', '제작': '#6f42c1', '조립': '#fd7e14', '양산': '#6610f2',
        '이설': '#e83e8c', '설치': '#20c997', '설치(거제)': '#ffc107', '거제(거제)': '#dc3545',
        '양산(거제)': '#28a745'
    }
    
    # 없는 카테고리는 랜덤 색상 생성
    for category in df['Category'].unique():
        if category not in predefined_colors:
            predefined_colors[category] = f"#{''.join([random.choice('0123456789ABCDEF') for _ in range(6)])}"
    
    return predefined_colors

def update_chart_layout(fig, sorted_df):
    """차트 레이아웃 업데이트"""
    fig.update_layout(
        yaxis=dict(
            autorange='reversed',
            showgrid=True,
            gridcolor="lightgrey",
            gridwidth=0.5,
            categoryorder='array',
            categoryarray=sorted_df['Task'].tolist(),
            fixedrange=False,
            type='category'
        ),
        xaxis=dict(
            type="date", 
            tickformat="%Y-%m-%d", 
            showline=True, 
            linecolor="lightgrey", 
            showgrid=True,
            gridcolor="lightgrey",
            gridwidth=0.5,
            side="top",  # 날짜 축을 위쪽으로 이동
            title=dict(
                text="날짜",
                standoff=10
            )
        ),
        title=dict(
            text='📊 프로젝트 진행 간트 차트',
            font=dict(size=18),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        font=dict(size=11),
        bargap=0.3,
        height=650,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,  # 범례를 차트 아래쪽으로 이동
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="lightgrey",
            borderwidth=1
        ),
        margin=dict(l=150, r=50, t=120, b=80)  # 아래쪽 마진 증가
    )
    
    # 범례 설명 추가 (차트 아래쪽, 범례 위에 위치)
    fig.add_annotation(
        text="■ 연한색: 계획 일정 | ■ 진한색: 실제 진행",
        xref="paper", yref="paper",
        x=0.5, y=-0.02,
        showarrow=False,
        font=dict(size=10, color="gray"),
        xanchor="center"
    )
    
    return fig

def add_actual_progress(fig, sorted_df, category_colors):
    """실제 진행 상황 추가"""
    for i, row in sorted_df.iterrows():
        if pd.notna(row.get('Actual_Start')) and row['Progress'] > 0:
            # 진행률에 따른 종료 시점 계산
            actual_duration = (row['End'] - row['Start']).total_seconds() * (row['Progress'] / 100)
            actual_end = row['Actual_Start'] + timedelta(seconds=actual_duration)
            
            # 실제 진행 막대 추가
            fig.add_shape(
                type='rect',
                x0=row['Actual_Start'],
                x1=actual_end,
                y0=i - 0.15,
                y1=i + 0.15,
                fillcolor=category_colors.get(row['Category'], '#808080'),
                opacity=1.0,
                line=dict(width=1, color='darkgray'),
                layer="above"
            )
    
    return fig

def add_date_marker(fig, marker_date):
    """날짜 마커 추가"""
    marker_datetime = datetime.combine(marker_date, datetime.min.time())
    
    fig.add_shape(
        type="line",
        x0=marker_datetime,
        x1=marker_datetime,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="red", width=3, dash="dot")
    )
    
    fig.add_annotation(
        x=marker_datetime,
        y=1,
        yref="paper",
        text=f"📅 {marker_date.strftime('%Y-%m-%d')}",
        showarrow=True,
        arrowhead=1,
        ax=50,
        ay=-30,
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="red",
        borderwidth=1
    )
    
    return fig

def display_project_analysis(sorted_df, marker_date):
    """프로젝트 상태 분석 표시"""
    st.subheader("📊 프로젝트 상태 분석")
    
    # 데이터 분석
    analysis_data = analyze_project_status(sorted_df, marker_date)
    
    # 요약 지표 표시
    display_summary_metrics(analysis_data)
    
    # 상태별 분포 차트
    display_status_chart(analysis_data['status_counts'])
    
    # 작업별 상세 테이블
    display_task_table(analysis_data['display_df'])

def analyze_project_status(sorted_df, marker_date):
    """프로젝트 상태 분석"""
    today_date = pd.Timestamp(marker_date)
    
    # 작업 상태 분류
    sorted_df = classify_task_status(sorted_df, today_date)
    
    # 예상 진행률 계산
    sorted_df = calculate_expected_progress(sorted_df, today_date)
    
    # 진행률 차이 계산
    sorted_df['Progress_Diff'] = sorted_df['Progress'] - sorted_df['Expected_Progress']
    
    # 요약 지표 계산
    summary_metrics = calculate_summary_metrics(sorted_df)
    
    # 상태별 개수
    status_counts = sorted_df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    # 표시용 데이터프레임 생성
    display_df = create_display_dataframe(sorted_df)
    
    return {
        'summary_metrics': summary_metrics,
        'status_counts': status_counts,
        'display_df': display_df
    }

def classify_task_status(df, today_date):
    """작업 상태 분류"""
    df['Status'] = 'Not Started'
    
    for i, row in df.iterrows():
        if row['Progress'] == 100:
            df.at[i, 'Status'] = '완료'
        elif row['Progress'] > 0:
            df.at[i, 'Status'] = '진행 중'
        elif today_date.date() < row['Start'].date():
            df.at[i, 'Status'] = '예정'
        elif today_date.date() >= row['Start'].date() and row['Progress'] == 0:
            df.at[i, 'Status'] = '지연'
    
    return df

def calculate_expected_progress(df, today_date):
    """예상 진행률 계산"""
    df['Expected_Progress'] = 0.0
    
    for i, row in df.iterrows():
        if today_date.date() > row['End'].date():
            df.at[i, 'Expected_Progress'] = 100.0
        elif today_date.date() < row['Start'].date():
            df.at[i, 'Expected_Progress'] = 0.0
        else:
            total_days = (row['End'] - row['Start']).days
            if total_days > 0:
                days_passed = (today_date - row['Start']).days
                expected = min(100.0, max(0.0, (days_passed / total_days) * 100.0))
                df.at[i, 'Expected_Progress'] = round(expected, 1)
    
    return df

def calculate_summary_metrics(df):
    """요약 지표 계산"""
    total_tasks = len(df)
    completed_tasks = len(df[df['Status'] == '완료'])
    in_progress_tasks = len(df[df['Status'] == '진행 중'])
    delayed_tasks = len(df[df['Status'] == '지연'])
    
    planned_progress = df['Expected_Progress'].mean()
    actual_progress = df['Progress'].mean()
    progress_diff = actual_progress - planned_progress
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'delayed_tasks': delayed_tasks,
        'planned_progress': planned_progress,
        'actual_progress': actual_progress,
        'progress_diff': progress_diff
    }

def display_summary_metrics(metrics):
    """요약 지표 표시"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 작업 수", metrics['total_tasks'])
    with col2:
        st.metric("완료된 작업", metrics['completed_tasks'])
    with col3:
        st.metric("진행 중인 작업", metrics['in_progress_tasks'])
    with col4:
        st.metric("지연된 작업", metrics['delayed_tasks'])
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("계획 진행률", f"{metrics['planned_progress']:.1f}%")
    with col2:
        st.metric("실제 진행률", f"{metrics['actual_progress']:.1f}%")
    with col3:
        st.metric(
            "진행률 차이", 
            f"{metrics['progress_diff']:+.1f}%", 
            delta_color="normal" if metrics['progress_diff'] >= 0 else "inverse"
        )

def display_status_chart(status_counts):
    """상태별 분포 차트 표시"""
    st.subheader("📈 작업 상태 분포")
    
    # 색상 정의
    status_colors = {
        '완료': 'green',
        '진행 중': 'blue',
        '예정': 'gray',
        '지연': 'red'
    }
    
    # 정해진 순서로 정렬
    status_order = ['완료', '진행 중', '예정', '지연']
    status_counts['Status'] = pd.Categorical(status_counts['Status'], categories=status_order, ordered=True)
    status_counts = status_counts.sort_values('Status')
    
    # 차트 생성
    fig_status = px.bar(
        status_counts, 
        x='Status', 
        y='Count',
        color='Status',
        color_discrete_map=status_colors,
        text='Count'
    )
    
    fig_status.update_traces(textposition='outside')
    fig_status.update_layout(
        title='작업 상태별 분포',
        xaxis_title=None,
        yaxis_title='작업 수',
        showlegend=False
    )
    
    st.plotly_chart(fig_status, use_container_width=True)

def create_display_dataframe(df):
    """표시용 데이터프레임 생성"""
    display_df = df[['Task', 'Category', 'Start', 'End', 'Actual_Start', 
                    'Progress', 'Expected_Progress', 'Progress_Diff', 'Status']].copy()
    
    # 열 이름 변경
    display_df.columns = ['작업', '카테고리', '계획 시작', '계획 종료', '실제 시작', 
                         '실제 진행률(%)', '예상 진행률(%)', '진행률 차이(%)', '상태']
    
    # 날짜 형식 변환
    display_df['계획 시작'] = display_df['계획 시작'].dt.strftime('%Y-%m-%d')
    display_df['계획 종료'] = display_df['계획 종료'].dt.strftime('%Y-%m-%d')
    display_df['실제 시작'] = display_df['실제 시작'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else '')
    
    # 상태에 이모지 추가
    emoji_map = {
        '완료': '🟩 완료',
        '진행 중': '🟦 진행 중',
        '예정': '⬜ 예정',
        '지연': '🟥 지연'
    }
    display_df['상태'] = display_df['상태'].map(emoji_map)
    
    # 진행률 차이 포맷팅
    def format_progress_diff(diff):
        if diff > 0:
            return f"✅ +{diff:.1f}%"
        elif diff < 0:
            return f"⚠️ {diff:.1f}%"
        return f"{diff:.1f}%"
    
    display_df['진행률 차이(%)'] = display_df['진행률 차이(%)'].apply(format_progress_diff)
    
    return display_df

def display_task_table(display_df):
    """작업별 상세 테이블 표시"""
    st.subheader("📋 작업별 진행 상황 (엑셀 입력 순서)")
    
    st.write("색상 코드: 🟩 완료  🟦 진행 중  ⬜ 예정  🟥 지연")
    
    st.dataframe(display_df, use_container_width=True)

def display_export_options(df):
    """데이터 내보내기 옵션 표시"""
    st.subheader("📥 데이터 내보내기")
    
    try:
        # 내보내기용 데이터 준비
        export_df = prepare_export_data(df)
        
        # Excel 파일 생성 및 다운로드
        buffer = create_excel_buffer(export_df)
        
        st.download_button(
            label="📥 엑셀로 내보내기",
            data=buffer,
            file_name='project_schedule_export.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            help="현재 프로젝트 일정을 엑셀 파일로 다운로드합니다."
        )
        
    except Exception as e:
        error_handler(f"엑셀 파일 생성 중 오류가 발생했습니다: {str(e)}")

def prepare_export_data(df):
    """내보내기용 데이터 준비"""
    export_df = df.copy()
    
    # 날짜 형식 변환
    export_df['Start'] = export_df['Start'].dt.strftime('%Y-%m-%d')
    export_df['End'] = export_df['End'].dt.strftime('%Y-%m-%d')
    
    if 'Actual_Start' in export_df.columns:
        export_df['Actual_Start'] = export_df['Actual_Start'].apply(
            lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else None
        )
    
    # 불필요한 컬럼 제거
    columns_to_remove = ['Original_Order']
    export_df = export_df.drop(columns=[col for col in columns_to_remove if col in export_df.columns])
    
    return export_df

def create_excel_buffer(df):
    """엑셀 버퍼 생성"""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Gantt Chart')
    
    buffer.seek(0)
    return buffer

def display_template_info():
    """템플릿 정보 표시"""
    info_message("엑셀 파일을 업로드해 주세요.")
    
    # 탭 구성
    template_tab, guide_tab = st.tabs(["📋 템플릿 다운로드", "📖 사용 가이드"])
    
    with template_tab:
        display_template_download()
    
    with guide_tab:
        display_usage_guide()

def display_template_download():
    """템플릿 다운로드 섹션"""
    st.markdown("### 📋 엑셀 파일 양식 안내")
    
    st.markdown("""
    간트 차트를 사용하기 위한 엑셀 파일에는 다음 열이 포함되어야 합니다:
    
    #### 필수 열:
    - **Task**: 작업 이름
    - **Start**: 계획 시작 날짜 (YYYY-MM-DD 형식)
    - **End**: 계획 종료 날짜 (YYYY-MM-DD 형식)
    
    #### 선택 열:
    - **Progress**: 작업 진행률 (0-100 사이의 숫자)
    - **Actual_Start**: 실제 시작 날짜 (YYYY-MM-DD 형식)
    - **Category**: 작업 카테고리 (없으면 Task에서 '_'로 자동 추출)
    
    ⭐ **정렬 기준**: 엑셀 파일에 입력된 순서대로 차트가 표시됩니다.
    """)
    
    # 샘플 데이터 표시
    st.markdown("#### 📊 샘플 데이터:")
    
    sample_data = {
        'Task': ['기획_요구사항 분석', '기획_프로젝트 범위', '설계_시스템 설계', '개발_백엔드 구현'],
        'Start': ['2025-01-01', '2025-01-10', '2025-01-18', '2025-02-01'],
        'End': ['2025-01-15', '2025-01-20', '2025-02-05', '2025-03-01'],
        'Progress': [100, 80, 60, 30],
        'Actual_Start': ['2025-01-02', '2025-01-11', '2025-01-20', ''],
        'Category': ['기획', '기획', '설계', '개발']
    }
    
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)
    
    # 템플릿 다운로드 버튼
    template_buffer = create_template_buffer(sample_df)
    
    st.download_button(
        label="📥 간트 차트 템플릿 다운로드",
        data=template_buffer,
        file_name='gantt_chart_template.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        help="간트 차트 기능을 사용하기 위한 기본 템플릿을 다운로드합니다."
    )

def create_template_buffer(template_df):
    """템플릿 엑셀 버퍼 생성"""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        template_df.to_excel(writer, index=False, sheet_name='Gantt Chart Template')
        
        # 워크시트 서식 지정
        workbook = writer.book
        worksheet = writer.sheets['Gantt Chart Template']
        
        # 헤더 서식
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # 헤더 적용
        for col_num, value in enumerate(template_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # 열 너비 조정
        column_widths = {'A:A': 25, 'B:C': 12, 'D:D': 10, 'E:E': 12, 'F:F': 15}
        for col_range, width in column_widths.items():
            worksheet.set_column(col_range, width)
    
    buffer.seek(0)
    return buffer

def display_usage_guide():
    """사용 가이드 표시"""
    st.markdown("""
    ### 🔧 Version 3.0 주요 개선사항
    
    1. **✅ 공통 유틸리티 적용**:
       - 일관된 UI/UX 컴포넌트 사용
       - 향상된 에러 처리 및 사용자 피드백
       - 성능 최적화 및 코드 구조 개선
    
    2. **✅ 향상된 사용자 경험**:
       - 직관적인 파일 업로드 인터페이스
       - 명확한 도움말 및 툴팁 제공
       - 개선된 시각적 피드백
    
    3. **✅ 강화된 기능**:
       - 실시간 진행률 업데이트
       - 상세한 프로젝트 분석
       - 향상된 데이터 내보내기
    
    ### 📋 사용 방법
    
    1. **파일 업로드**: 템플릿에 맞는 엑셀 파일을 업로드합니다.
    2. **기준 날짜 설정**: 진행 상황을 확인할 기준 날짜를 선택합니다.
    3. **진행률 업데이트**: 사이드바에서 작업별 진행률을 업데이트합니다.
    4. **분석 확인**: 프로젝트 상태 분석 결과를 확인합니다.
    5. **데이터 내보내기**: 업데이트된 일정을 엑셀로 내보냅니다.
    
    ### 📊 간트 차트 해석
    
    - **연한색 막대**: 계획된 일정
    - **진한색 막대**: 실제 진행 상황
    - **빨간 점선**: 기준 날짜
    - **색상별 구분**: 작업 카테고리
    - **상태 표시**: 🟩 완료 🟦 진행중 ⬜ 예정 🟥 지연
    """)

# 메인 실행
if __name__ == "__main__":
    gantt_chart()
