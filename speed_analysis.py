import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def speed_analysis():
    """
    Perform speed and acceleration analysis. Streamlit UI allows users to upload Excel files,
    visualize the results, and download the analysis.
    """
    
    st.title("속도 및 가속도 분석 도구")

    # 탭 구성: 입력, 결과 탭으로 구분
    input_tab, result_tab = st.tabs(["입력", "결과"])

    with input_tab:
        st.header("엑셀 파일 업로드")
        # 엑셀 파일 업로드
        uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"], key="speed")

        # 변수 초기화
        time = None
        velocity = None
        acceleration = None
        distance = None

        if uploaded_file:
            # 엑셀 파일에서 'Data' 시트를 읽어옵니다.
            data = pd.read_excel(uploaded_file, sheet_name=0)

            # NaN 값 처리 (제거)
            data = data.dropna()

            # 업로드된 데이터 표시
            st.subheader("업로드된 데이터")
            st.write(data)

            # 시간과 속도 데이터를 추출합니다.
            if 'Time_sec' in data.columns and 'Velocity_m/s' in data.columns:
                time = data['Time_sec'].values
                velocity = data['Velocity_m/s'].values

                # 속도 데이터를 이용해 가속도와 이동거리 계산
                acceleration = np.gradient(velocity, time)
                distance = np.cumsum(velocity * np.gradient(time))
            else:
                st.error("'Time_sec'과 'Velocity_m/s' 열이 필요합니다. 엑셀 파일을 확인해주세요.")

    with result_tab:
        if time is not None and velocity is not None:
            st.header("분석 결과")

            # 속도, 가속도, 이동거리 결과 출력
            st.subheader("속도, 가속도, 이동거리 결과")
            results_df = pd.DataFrame({
                'Time': time,
                'Velocity': velocity,
                'Acceleration': acceleration,
                'Distance': distance
            })
            st.write(results_df)

            # 시각화 생성
            st.subheader("시각화 결과")

            # 속도 그래프
            fig, ax = plt.subplots()
            ax.plot(time, velocity, label='Velocity', color='b')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Velocity (m/s)', color='b')
            ax.tick_params(axis='y', labelcolor='b')
            ax.legend(loc='upper left')
            st.pyplot(fig)

            # 가속도 그래프
            fig, ax = plt.subplots()
            ax.plot(time, acceleration, label='Acceleration', color='r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Acceleration (m/s^2)', color='r')
            ax.tick_params(axis='y', labelcolor='r')
            ax.legend(loc='upper left')
            st.pyplot(fig)

            # 이동거리 그래프
            fig, ax = plt.subplots()
            ax.plot(time, distance, label='Distance', color='g')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Distance (m)', color='g')
            ax.tick_params(axis='y', labelcolor='g')
            ax.legend(loc='upper left')
            st.pyplot(fig)
        else:
            st.write("엑셀 파일을 업로드하고 데이터를 확인해주세요.")
