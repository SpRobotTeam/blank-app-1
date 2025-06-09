import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from io import BytesIO
from datetime import datetime, timedelta

def gantt_chart():
    """
    Generate a Gantt chart using uploaded Excel data. Supports filtering and downloading results.
    """
    st.title("프로젝트 진행 간트 차트")

    # 파일 업로드 위젯
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요.", type=['xlsx'], key="gantt")

    # 날짜 마커 입력 위젯 추가
    marker_date = st.date_input("특정 날짜 마커 추가 (선택사항)", value=None, key="marker_date")

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
            
            # 실제 시작/종료 날짜 열이 있으면 변환
            if 'Actual_Start' in df.columns:
                df['Actual_Start'] = pd.to_datetime(df['Actual_Start'])
            if 'Actual_End' in df.columns:
                df['Actual_End'] = pd.to_datetime(df['Actual_End'])
        except KeyError:
            st.error("엑셀 파일에 'Start' 또는 'End' 열이 없습니다. 데이터를 확인하세요.")
            st.stop()

        # 진행률 확인
        if 'Progress' not in df.columns:
            df['Progress'] = 0  # 진행률이 없는 경우 기본값 0으로 설정

        # 작업 종류 구분: Task에서 '_' 앞쪽을 추출
        df['Category'] = df['Task'].apply(lambda x: x.split('_')[0] if '_' in x else 'Unknown')

        # 사용자 설정 옵션
        st.sidebar.header("설정 옵션")
        order_by = st.radio(
            "정렬 기준을 선택하세요:",
            ('Start', 'End'),
            index=0,
            horizontal=True
        )

        # 실제 진행 일정 입력 기능 추가
        st.sidebar.subheader("실제 진행 일정 입력")
        
        # 선택한 작업에 실제 시작/종료 날짜 입력 가능
        selected_task = st.sidebar.selectbox("작업 선택", options=df['Task'].tolist())
        
        # 선택한 작업의 인덱스 찾기
        task_idx = df[df['Task'] == selected_task].index[0]
        
        # 실제 시작일과 종료일 설정 (기존 값이 있으면 사용)
        if 'Actual_Start' not in df.columns:
            df['Actual_Start'] = None
        if 'Actual_End' not in df.columns:
            df['Actual_End'] = None
            
        actual_start_date = st.sidebar.date_input(
            "실제 시작일",
            value=df.at[task_idx, 'Actual_Start'] if pd.notna(df.at[task_idx, 'Actual_Start']) else df.at[task_idx, 'Start'],
            key="actual_start"
        )
        
        actual_end_date = st.sidebar.date_input(
            "실제 종료일 (또는 예상 종료일)",
            value=df.at[task_idx, 'Actual_End'] if pd.notna(df.at[task_idx, 'Actual_End']) else df.at[task_idx, 'End'],
            key="actual_end"
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
            df.at[task_idx, 'Actual_End'] = actual_end_date
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

        # 실제 일정 추가 (실제 시작/종료 날짜가 있는 경우)
        if 'Actual_Start' in df.columns and 'Actual_End' in df.columns:
            for i, row in sorted_df.iterrows():
                if pd.notna(row['Actual_Start']) and pd.notna(row['Actual_End']):
                    # 실제 일정을 파선으로 표시 (계획 일정 위에 겹쳐서)
                    fig.add_trace(go.Scatter(
                        x=[row['Actual_Start'], row['Actual_End']],
                        y=[i, i],
                        mode='lines',
                        line=dict(color='black', width=4, dash='dash'),
                        name='실제 일정',
                        showlegend=False
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
            fig.add_shape(
                type='rect',
                x0=row['Start'],
                x1=row['Start'] + progress_duration,  # 진행률에 따라 진행된 구간 표시
                y0=i - 0.3,  # Bar 크기와 간격 조정
                y1=i + 0.3,
                fillcolor='rgba(0, 128, 0, 0.5)',
                line=dict(width=0)
            )

        # 특정 날짜 마커 추가
        if marker_date:
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
                text=f"기준 날짜: {marker_date}",
                showarrow=True,
                arrowhead=1,
                ax=50,
                ay=-30
            )

        # 실제 진행 일정에 대한 범례 추가
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(color='black', width=4, dash='dash'),
            name='실제 일정'
        ))

        # Streamlit 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

        # 진행 상황 요약 표시
        st.subheader("진행 상황 요약")
        total_tasks = len(sorted_df)
        completed_tasks = len(sorted_df[sorted_df['Progress'] == 100])
        avg_progress = sorted_df['Progress'].mean()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 작업 수", total_tasks)
        with col2:
            st.metric("완료된 작업 수", completed_tasks)
        with col3:
            st.metric("평균 진행률", f"{avg_progress:.2f}%")

        # 계획 대비 실제 일정 분석
        if 'Actual_Start' in df.columns and 'Actual_End' in df.columns:
            st.subheader("계획 대비 실제 일정 분석")
            
            # 실제 일정이 입력된 작업만 필터링
            actual_df = sorted_df[(pd.notna(sorted_df['Actual_Start'])) & (pd.notna(sorted_df['Actual_End']))]
            
            if not actual_df.empty:
                # 시작 일정 지연/앞당김 계산
                actual_df['Start_Diff'] = (actual_df['Actual_Start'] - actual_df['Start']).dt.days
                
                # 종료 일정 지연/앞당김 계산
                actual_df['End_Diff'] = (actual_df['Actual_End'] - actual_df['End']).dt.days
                
                # 일정 분석 표시
                analysis_df = actual_df[['Task', 'Start', 'Actual_Start', 'Start_Diff', 'End', 'Actual_End', 'End_Diff', 'Progress']]
                analysis_df.columns = ['작업', '계획 시작', '실제 시작', '시작 차이(일)', '계획 종료', '실제/예상 종료', '종료 차이(일)', '진행률(%)']
                
                # 지연된 작업 강조
                def highlight_delays(val):
                    if isinstance(val, (int, float)):
                        if val > 0:
                            return 'color: red'
                        elif val < 0:
                            return 'color: green'
                    return ''
                
                # 스타일이 적용된 DataFrame 표시
                st.dataframe(analysis_df.style.applymap(highlight_delays, subset=['시작 차이(일)', '종료 차이(일)']))
                
                # 전체 프로젝트 지연 여부 분석
                critical_tasks = sorted_df[sorted_df['End'] == sorted_df['End'].max()]
                critical_task = critical_tasks.iloc[0]
                
                if '실제/예상 종료' in analysis_df.columns and critical_task['Task'] in analysis_df['작업'].values:
                    critical_actual = analysis_df[analysis_df['작업'] == critical_task['Task']]['실제/예상 종료'].iloc[0]
                    critical_planned = critical_task['End']
                    delay = (critical_actual - critical_planned).days
                    
                    if delay > 0:
                        st.warning(f"⚠️ 프로젝트가 전체적으로 {delay}일 지연될 것으로 예상됩니다.")
                    elif delay < 0:
                        st.success(f"✅ 프로젝트가 전체적으로 {abs(delay)}일 앞당겨질 것으로 예상됩니다.")
                    else:
                        st.info("🟢 프로젝트가 예정대로 진행 중입니다.")
            else:
                st.info("실제 일정이 입력된 작업이 없습니다. 사이드바에서 작업을 선택하고 실제 시작/종료 날짜를 입력해주세요.")

        # 정렬된 데이터프레임 표시
        with st.expander("정렬된 데이터프레임 보기"):
            st.dataframe(sorted_df)

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
                
                # 실제 시작/종료 날짜가 있으면 변환
                if 'Actual_Start' in export_df.columns:
                    export_df['Actual_Start'] = export_df['Actual_Start'].apply(
                        lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else None
                    )
                if 'Actual_End' in export_df.columns:
                    export_df['Actual_End'] = export_df['Actual_End'].apply(
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
        st.info("""
        ## 사용 방법
        1. 사이드바에서 작업을 선택하고 실제 시작일, 종료일 및 진행률을 설정한 후 '변경사항 적용' 버튼을 클릭하세요.
        2. 계획 일정은 막대 그래프로, 실제 일정은 검은색 점선으로 표시됩니다.
        3. 진행률은 녹색 막대로 표시됩니다.
        4. 수정한 데이터는 '엑셀로 내보내기' 버튼을 클릭하여 저장할 수 있습니다.
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
        - **Actual_End**: 실제 종료 날짜 또는 예상 종료 날짜 (YYYY-MM-DD 형식)
        
        #### 작업 분류 팁:
        - 작업명을 `카테고리_작업명` 형식으로 입력하면 동일한 카테고리의 작업이 같은 색으로 표시됩니다.
        """)
        
        # 샘플 데이터 표시
        st.markdown("""
        #### 샘플 데이터:
        ```
        | Task              | Start      | End        | Progress | Actual_Start | Actual_End  |
        |-------------------|------------|------------|----------|--------------|-------------|
        | 기획_요구사항 분석   | 2025-01-01 | 2025-01-15 | 100      | 2025-01-02   | 2025-01-14  |
        | 기획_프로젝트 범위   | 2025-01-10 | 2025-01-20 | 80       | 2025-01-11   | 2025-01-22  |
        | 설계_시스템 설계    | 2025-01-18 | 2025-02-05 | 60       | 2025-01-20   |             |
        | 개발_백엔드 구현    | 2025-02-01 | 2025-03-01 | 30       |              |             |
        ```
        """)
