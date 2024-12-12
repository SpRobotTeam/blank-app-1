import random
import pandas as pd
import plotly.express as px
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

        # 정렬 기준에 따라 데이터프레임 정렬
        sorted_df = df.sort_values(by=order_by)

        # 랜덤 색상 생성 (카테고리별)
        unique_categories = sorted_df['Category'].unique()
        color_map = {cat: f"#{''.join([random.choice('0123456789ABCDEF') for _ in range(6)])}" for cat in unique_categories}

        # 간트 차트 생성
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
            progress_duration = timedelta(
                seconds=(row['End'] - row['Start']).total_seconds() * row['Progress'] / 100
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

        # Streamlit 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

        # 진행 상황 요약 표시
        st.subheader("진행 상황 요약")
        total_tasks = len(sorted_df)
        completed_tasks = len(sorted_df[sorted_df['Progress'] == 100])
        avg_progress = sorted_df['Progress'].mean()

        st.metric("총 작업 수", total_tasks)
        st.metric("완료된 작업 수", completed_tasks)
        st.metric("평균 진행률", f"{avg_progress:.2f}%")

        # 정렬 확인용 로그 출력 (Streamlit 앱에서 확인 가능)
        st.write("정렬된 데이터프레임:", sorted_df)

        # 작업을 엑셀로 내보내기
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            sorted_df.to_excel(writer, index=False, sheet_name='Gantt Chart')
            processed_data = output.getvalue()

        st.download_button(
            label="엑셀로 내보내기",
            data=processed_data,
            file_name='project_schedule_export.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # 드래그로 수정 기능 (현재 Streamlit과 Plotly만으로는 지원되지 않음)
        st.info("작업을 드래그로 수정하는 기능은 현재 지원되지 않습니다. 대신 엑셀에서 직접 수정하거나 입력된 데이터를 수정해 주세요.")
    else:
        st.info("엑셀 파일을 업로드해 주세요.")
