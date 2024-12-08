import pandas as pd
import plotly.express as px
import streamlit as st
from io import BytesIO


def gantt_chart():
    """
    Generate a Gantt chart using uploaded Excel data. Supports filtering and downloading results.
    """
    st.title("프로젝트 진행 간트 차트")

    # 파일 업로드 위젯
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요.", type=['xlsx'], key="gantt")

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
            # return

        # 진행률 확인
        if 'Progress' not in df.columns:
            df['Progress'] = 0  # 진행률이 없는 경우 기본값 0으로 설정

        # 사용자 설정 옵션
        st.sidebar.header("설정 옵션")
        order_by = st.radio(
            "정렬 기준을 선택하세요:",
            ('Start', 'End'),
            index=0,
            horizontal=True
        )

        # 그룹핑 열 선택 (예: 팀, 카테고리 등)
        group_column = None
        if 'Group' in df.columns:
            group_column = 'Group'
            st.sidebar.title("그룹별 필터링")
            unique_groups = df['Group'].unique()
            selected_groups = st.sidebar.multiselect("그룹을 선택하세요:", options=unique_groups, default=unique_groups)
            df = df[df['Group'].isin(selected_groups)]

        # 정렬 기준에 따라 데이터프레임 정렬
        sorted_df = df.sort_values(by=order_by)


        # 간트 차트 생성 (엑셀 순서 유지, 우하향으로 구성)
        fig = px.timeline(
            sorted_df, 
            x_start="Start", 
            x_end="End", 
            y="Task", 
            title='프로젝트 진행 간트 차트', 
            color=group_column if group_column else "Task",
            text='Task',
            labels={'Task': '작업', 'Start': '시작 날짜', 'End': '종료 날짜', 'Group': '그룹'}
        )
        fig.update_yaxes(categoryorder='array', categoryarray=sorted_df['Task'])  # 엑셀 파일의 순서를 유지
        fig.update_layout(yaxis_autorange='reversed', xaxis_showgrid=True, yaxis_showgrid=True)  # 우하향으로 구성 및 격자표 추가
        fig.update_xaxes(tickformat="%y-%m-%d")  # 날짜 형식을 yy-mm-%d로 변경

        # 진행률 추가 표시
        for i, row in sorted_df.iterrows():
            fig.add_shape(
                type='rect',
                x0=row['Start'],
                x1=row['Start'] + (row['End'] - row['Start']) * row['Progress'] / 100,
                y0=i - 0.1,
                y1=i + 0.1,
                fillcolor='rgba(0, 128, 0, 0.5)',
                line=dict(width=0)
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

