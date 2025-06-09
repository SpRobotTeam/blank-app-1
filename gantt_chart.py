import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from io import BytesIO
from datetime import datetime, timedelta, date
import os

def gantt_chart():
    """
    Generate a Gantt chart using uploaded Excel data. Supports filtering and downloading results.
    """
    st.title("프로젝트 진행 간트 차트")

    # 파일 업로드 위젯
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요.", type=['xlsx'], key="gantt")

    # 날짜 마커 입력 위젯 추가 (오늘 날짜 기본값)
    today = date.today()
    marker_date = st.date_input("특정 날짜 마커 추가 (기본: 오늘)", value=today, key="marker_date")

    if uploaded_file is not None:
        try:
            # 엑셀 파일 읽기
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        except Exception as e:
            st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
            return

        # 날짜 변환
        try:
            df['Start'] = pd.to_datetime(df['Start'])
            df['End'] = pd.to_datetime(df['End'])
            
            # 실제 시작일이 있으면 변환
            if 'Actual_Start' in df.columns:
                df['Actual_Start'] = pd.to_datetime(df['Actual_Start'])
        except KeyError:
            st.error("엑셀 파일에 'Start' 또는 'End' 열이 없습니다. 데이터를 확인하세요.")
            st.stop()

        # 진행률 확인
        if 'Progress' not in df.columns:
            df['Progress'] = 0  # 진행률이 없는 경우 기본값 0으로 설정

        # 작업 종류 구분: Category 열이 없는 경우 Task에서 '_' 앞쪽을 추출
        if 'Category' not in df.columns:
            df['Category'] = df['Task'].apply(lambda x: x.split('_')[0] if '_' in x else 'Unknown')

        # 사용자 설정 옵션
        st.sidebar.header("설정 옵션")
        order_by = st.radio(
            "정렬 기준을 선택하세요:",
            ('Start', 'End', 'Category'),
            index=0,
            horizontal=True
        )

        # 실제 진행 일정 입력 기능 추가 (간소화)
        st.sidebar.subheader("진행 상황 업데이트")
        
        # 선택한 작업에 실제 시작/종료 날짜 입력 가능
        selected_task = st.sidebar.selectbox("작업 선택", options=df['Task'].tolist())
        
        # 선택한 작업의 인덱스 찾기
        task_idx = df[df['Task'] == selected_task].index[0]
        
        # 실제 시작일 설정
        if 'Actual_Start' not in df.columns:
            df['Actual_Start'] = None
            
        actual_start_date = st.sidebar.date_input(
            "실제 시작일",
            value=df.at[task_idx, 'Actual_Start'] if pd.notna(df.at[task_idx, 'Actual_Start']) else df.at[task_idx, 'Start'],
            key="actual_start"
        )
        
        # 진행률 설정
        progress = st.sidebar.slider(
            "진행률 (%)",
            min_value=0,
            max_value=100,
            value=int(df.at[task_idx, 'Progress']),
            key="progress_slider"
        )
        
        # 변경사항 적용 버튼
        if st.sidebar.button("변경사항 적용"):
            df.at[task_idx, 'Actual_Start'] = actual_start_date
            df.at[task_idx, 'Progress'] = progress
            st.sidebar.success(f"'{selected_task}'의 정보가 업데이트되었습니다.")

        # 정렬 기준에 따라 데이터프레임 정렬
        sorted_df = df.sort_values(by=order_by)

        # 랜덤 색상 생성 (카테고리별)
        unique_categories = sorted_df['Category'].unique()
        color_map = {cat: f"#{''.join([random.choice('0123456789ABCDEF') for _ in range(6)])}" for cat in unique_categories}

        # 간트 차트 생성 (계획 일정)
        fig = px.timeline(
            sorted_df, 
            x_start="Start", 
            x_end="End", 
            y="Task", 
            title='프로젝트 진행 간트 차트', 
            color='Category',  # 카테고리를 기준으로 색상 지정
            text='Task',
            labels={'Task': '작업', 'Start': '시작 날짜', 'End': '종료 날짜', 'Category': '카테고리'}
        )

        # 사용자 정의 색상 적용
        fig.update_traces(marker=dict(colorscale=list(color_map.values())))

        # 실제 시작일 마커 추가 (실제 시작일이 있는 경우)
        if 'Actual_Start' in df.columns:
            for i, row in sorted_df.iterrows():
                if pd.notna(row['Actual_Start']):
                    # 실제 시작일을 다이아몬드 마커로 표시
                    fig.add_trace(go.Scatter(
                        x=[row['Actual_Start']],
                        y=[i],
                        mode='markers',
                        marker=dict(symbol='diamond', size=12, color='black'),
                        name='실제 시작일',
                        showlegend=(i == 0)  # 첫 번째 항목만 범례에 표시
                    ))

        fig.update_yaxes(categoryorder='array', categoryarray=sorted_df['Task'])  # 엑셀 파일의 순서를 유지

        # 차트 레이아웃 조정 (가로 및 세로 격자 추가)
        fig.update_layout(
            yaxis=dict(
                autorange='reversed',  # Task가 위에서 아래로 나열되도록 설정
                showgrid=True,  # 가로 격자 추가
                gridcolor="lightgrey",  # 격자 색상 설정
                gridwidth=0.5  # 격자 두께 설정
            ),
            xaxis=dict(
                type="date", 
                tickformat="%Y-%m-%d", 
                showline=True, 
                linecolor="lightgrey", 
                showgrid=True,  # 세로 격자 추가
                gridcolor="lightgrey",  # 격자 색상 설정
                gridwidth=0.5  # 격자 두께 설정
            ),
            title=dict(font=dict(size=20)),  # 차트 제목 크기 조정
            font=dict(size=14),  # 차트 전체 텍스트 크기 조정
            bargap=0.3,  # Bar 간격 조정
            height=800  # 차트 높이 조정
        )

        # 진행률 추가 표시
        for i, row in sorted_df.iterrows():
            # 진행률 계산을 명시적으로 timedelta로 변환
            duration = row['End'] - row['Start']
            progress_duration = timedelta(
                seconds=duration.total_seconds() * row['Progress'] / 100
            )
            
            # 시작점 설정 (실제 시작일이 있으면 실제 시작일, 없으면 계획 시작일)
            start_point = row['Actual_Start'] if pd.notna(row['Actual_Start']) else row['Start']
            
            fig.add_shape(
                type='rect',
                x0=start_point,
                x1=start_point + progress_duration,  # 진행률에 따라 진행된 구간 표시
                y0=i - 0.3,  # Bar 크기와 간격 조정
                y1=i + 0.3,
                fillcolor='rgba(0, 128, 0, 0.5)',
                line=dict(width=0)
            )

        # 특정 날짜 마커 추가 (오늘 또는 선택한 날짜)
        marker_datetime = datetime.combine(marker_date, datetime.min.time())
        fig.add_shape(
            type="line",
            x0=marker_datetime,
            x1=marker_datetime,
            y0=0,
            y1=1,
            yref="paper",
            line=dict(
                color="red",
                width=3,
                dash="dot"
            )
        )
        fig.add_annotation(
            x=marker_datetime,
            y=1,
            yref="paper",
            text=f"기준 날짜: {marker_date.strftime('%Y-%m-%d')}",
            showarrow=True,
            arrowhead=1,
            ax=50,
            ay=-30
        )

        # Streamlit 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

        # 프로젝트 상태 분석 (시작 일정과 진행률 기반)
        st.subheader("프로젝트 상태 분석")
        
        # 현재 날짜 기준 진행 상황 분석 - Timestamp로 변환
        today_date = pd.Timestamp(marker_date)
        
        # 작업 상태 분류
        sorted_df['Status'] = 'Not Started'  # 기본 상태
        
        for i, row in sorted_df.iterrows():
            # 완료된 작업
            if row['Progress'] == 100:
                sorted_df.at[i, 'Status'] = '완료'
            # 진행 중인 작업
            elif row['Progress'] > 0:
                sorted_df.at[i, 'Status'] = '진행 중'
            # 시작 예정 작업 - 날짜 비교 수정
            elif today_date.date() < row['Start'].date():
                sorted_df.at[i, 'Status'] = '예정'
            # 지연 시작 작업
            elif today_date.date() >= row['Start'].date() and row['Progress'] == 0:
                sorted_df.at[i, 'Status'] = '지연'
        
        # 작업 상태별 색상 정의
        status_colors = {
            '완료': 'green',
            '진행 중': 'blue',
            '예정': 'gray',
            '지연': 'red'
        }
        
        # 계획 대비 진행률 분석
        sorted_df['Expected_Progress'] = 0.0
        
        for i, row in sorted_df.iterrows():
            # 이미 끝난 작업은 100%
            if today_date.date() > row['End'].date():
                sorted_df.at[i, 'Expected_Progress'] = 100.0
            # 아직 시작 안한 작업은 0%
            elif today_date.date() < row['Start'].date():
                sorted_df.at[i, 'Expected_Progress'] = 0.0
            # 진행 중인 작업은 비율 계산
            else:
                total_days = (row['End'] - row['Start']).days
                if total_days > 0:
                    days_passed = (today_date - row['Start']).days
                    expected = min(100.0, max(0.0, (days_passed / total_days) * 100.0))
                    sorted_df.at[i, 'Expected_Progress'] = round(expected, 1)
        
        # 진행률 차이 계산
        sorted_df['Progress_Diff'] = sorted_df['Progress'] - sorted_df['Expected_Progress']
        
        # 요약 지표
        total_tasks = len(sorted_df)
        completed_tasks = len(sorted_df[sorted_df['Status'] == '완료'])
        in_progress_tasks = len(sorted_df[sorted_df['Status'] == '진행 중'])
        delayed_tasks = len(sorted_df[sorted_df['Status'] == '지연'])
        
        # 전체 프로젝트 진행률
        planned_progress = sorted_df['Expected_Progress'].mean()
        actual_progress = sorted_df['Progress'].mean()
        progress_diff = actual_progress - planned_progress
        
        # 진행률 상태에 따른 색상
        progress_color = 'green' if progress_diff >= 0 else 'red'
        
        # 요약 지표 표시
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 작업 수", total_tasks)
        with col2:
            st.metric("완료된 작업", completed_tasks)
        with col3:
            st.metric("진행 중인 작업", in_progress_tasks)
        with col4:
            st.metric("지연된 작업", delayed_tasks)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("계획 진행률", f"{planned_progress:.1f}%")
        with col2:
            st.metric("실제 진행률", f"{actual_progress:.1f}%")
        with col3:
            st.metric("진행률 차이", f"{progress_diff:+.1f}%", delta_color="normal" if progress_diff >= 0 else "inverse")
        
        # 작업 상태별 시각화
        st.subheader("작업 상태 분포")
        status_counts = sorted_df['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        # 정해진 순서로 상태 정렬
        status_order = ['완료', '진행 중', '예정', '지연']
        status_counts['Status'] = pd.Categorical(status_counts['Status'], categories=status_order, ordered=True)
        status_counts = status_counts.sort_values('Status')
        
        # 작업 상태 차트
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
        
        # 작업 상태 테이블
        st.subheader("작업별 진행 상황")
        
        # 표시할 열 선택
        display_df = sorted_df[['Task', 'Category', 'Start', 'End', 'Actual_Start', 
                               'Progress', 'Expected_Progress', 'Progress_Diff', 'Status']].copy()
        
        # 열 이름 변경
        display_df.columns = ['작업', '카테고리', '계획 시작', '계획 종료', '실제 시작', 
                             '실제 진행률(%)', '예상 진행률(%)', '진행률 차이(%)', '상태']
        
        # 날짜 형식 변환 (스트림릿에서 표시용)
        display_df['계획 시작'] = display_df['계획 시작'].dt.strftime('%Y-%m-%d')
        display_df['계획 종료'] = display_df['계획 종료'].dt.strftime('%Y-%m-%d')
        display_df['실제 시작'] = display_df['실제 시작'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else '')
        
        # 스타일링 대신 색상으로 상태 구분
        st.write("색상 코드: 🟩 완료  🟦 진행 중  ⬜ 예정  🟥 지연")
        
        # 상태에 따라 이모지 추가
        def add_status_emoji(status):
            if status == '완료':
                return '🟩 완료'
            elif status == '진행 중':
                return '🟦 진행 중'
            elif status == '예정':
                return '⬜ 예정'
            elif status == '지연':
                return '🟥 지연'
            return status
        
        display_df['상태'] = display_df['상태'].apply(add_status_emoji)
        
        # 진행률 차이 표시 개선
        def format_progress_diff(diff):
            if diff > 0:
                return f"✅ +{diff:.1f}%"
            elif diff < 0:
                return f"⚠️ {diff:.1f}%"
            return f"{diff:.1f}%"
            
        display_df['진행률 차이(%)'] = display_df['진행률 차이(%)'].apply(format_progress_diff)
        
        # 데이터프레임 표시
        st.dataframe(display_df, use_container_width=True)
        
        # 작업을 엑셀로 내보내기
        try:
            # BytesIO 객체 처리와 엑셀 저장
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # 날짜 포맷 문제 해결을 위해 복사본 생성 및 처리
                export_df = sorted_df.copy()
                
                # 날짜 열을 문자열로 변환하여 포맷 문제 방지
                export_df['Start'] = export_df['Start'].dt.strftime('%Y-%m-%d')
                export_df['End'] = export_df['End'].dt.strftime('%Y-%m-%d')
                
                # 실제 시작 날짜가 있으면 변환
                if 'Actual_Start' in export_df.columns:
                    export_df['Actual_Start'] = export_df['Actual_Start'].apply(
                        lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else None
                    )
                
                # 파일에 저장
                export_df.to_excel(writer, index=False, sheet_name='Gantt Chart')
            
            # 버퍼 위치를 처음으로 되돌림
            buffer.seek(0)
            
            # 다운로드 버튼 표시
            st.download_button(
                label="엑셀로 내보내기",
                data=buffer,
                file_name='project_schedule_export.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except Exception as e:
            st.error(f"엑셀 파일 생성 중 오류가 발생했습니다: {e}")

        # 사용 방법 안내
        with st.expander("사용 방법"):
            st.markdown("""
            ### 사용 방법
            
            1. **진행 상황 업데이트**:
               - 사이드바에서 작업을 선택합니다.
               - 실제 시작일과 진행률을 설정합니다.
               - '변경사항 적용' 버튼을 클릭합니다.
            
            2. **상태 확인**:
               - 각 작업의 진행 상태는 '작업별 진행 상황' 테이블에서 확인할 수 있습니다.
               - 완료된 작업은 녹색, 지연된 작업은 빨간색으로 표시됩니다.
               - 계획 대비 진행률 차이를 통해 작업이 일정보다 앞서가는지 또는 지연되는지 확인할 수 있습니다.
            
            3. **파일 저장**:
               - '엑셀로 내보내기' 버튼을 클릭하여 현재 작업 상태를 저장할 수 있습니다.
               - 저장된 파일은 다음에 업로드하여 계속 진행 상황을 업데이트할 수 있습니다.
            """)
    else:
        st.info("엑셀 파일을 업로드해 주세요.")
        
        # 엑셀 양식 안내
        st.markdown("""
        ### 엑셀 파일 양식 안내
        간트 차트를 사용하기 위한 엑셀 파일에는 다음 열이 포함되어야 합니다:
        
        #### 필수 열:
        - **Task**: 작업 이름
        - **Start**: 계획 시작 날짜 (YYYY-MM-DD 형식)
        - **End**: 계획 종료 날짜 (YYYY-MM-DD 형식)
        
        #### 선택 열:
        - **Progress**: 작업 진행률 (0-100 사이의 숫자)
        - **Actual_Start**: 실제 시작 날짜 (YYYY-MM-DD 형식)
        - **Category**: 작업 카테고리 (없으면 Task에서 '_'로 자동 추출)
        """)
        
        # 샘플 데이터 표시
        st.markdown("""
        #### 샘플 데이터:
        
        | Task | Start | End | Progress | Actual_Start | Category |
        |------|-------|-----|----------|--------------|----------|
        | 기획_요구사항 분석 | 2025-01-01 | 2025-01-15 | 100 | 2025-01-02 | 기획 |
        | 기획_프로젝트 범위 | 2025-01-10 | 2025-01-20 | 80 | 2025-01-11 | 기획 |
        | 설계_시스템 설계 | 2025-01-18 | 2025-02-05 | 60 | 2025-01-20 | 설계 |
        | 개발_백엔드 구현 | 2025-02-01 | 2025-03-01 | 30 |  | 개발 |
        """)
        
        # 템플릿 다운로드 옵션 제공
        st.markdown("### 템플릿 다운로드")
        
        # 템플릿 데이터 생성
        template_data = {
            'Task': ['기획_요구사항 분석', '기획_프로젝트 범위', '설계_시스템 설계', '개발_백엔드 구현'],
            'Start': ['2025-01-01', '2025-01-10', '2025-01-18', '2025-02-01'],
            'End': ['2025-01-15', '2025-01-20', '2025-02-05', '2025-03-01'],
            'Progress': [100, 80, 60, 30],
            'Actual_Start': ['2025-01-02', '2025-01-11', '2025-01-20', ''],
            'Category': ['기획', '기획', '설계', '개발']
        }
        
        template_df = pd.DataFrame(template_data)
        
        # Excel로 템플릿 변환
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
            worksheet.set_column('A:A', 25)  # Task
            worksheet.set_column('B:C', 12)  # Start, End
            worksheet.set_column('D:D', 10)  # Progress
            worksheet.set_column('E:E', 12)  # Actual_Start
            worksheet.set_column('F:F', 15)  # Category
        
        buffer.seek(0)
        
        st.download_button(
            label="간트 차트 템플릿 다운로드",
            data=buffer,
            file_name='gantt_chart_template.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            help="간트 차트 기능을 사용하기 위한 기본 템플릿을 다운로드합니다."
        )
