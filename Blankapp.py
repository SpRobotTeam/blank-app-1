# pip install matplotlib PCA plotly

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import plotly.graph_objs as go

# Streamlit UI 생성
st.set_page_config(page_title="3D 및 속도 분석 도구", layout="wide")

# 사이드바에서 분석 유형 선택
st.sidebar.title("분석 도구 선택")
analysis_type = st.sidebar.radio("분석 유형을 선택하세요:", ("3D 선형성 평가", "속도 및 가속도 분석"))

if analysis_type == "3D 선형성 평가":
    st.title("3D 선형성 평가 도구")

    # 탭 구성: 입력, 평가방법, 결과 탭으로 구분
    input_tab, method_tab, result_tab = st.tabs(["입력", "평가방법", "결과"])

    with input_tab:
        st.header("엑셀 파일 업로드")
        # 엑셀 파일 업로드
        uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

        # 변수 초기화
        data_points_x1 = None
        data_points_x2 = None
        data_points_y = None
        data_points_z = None
        direction_vector_x1 = None
        direction_vector_x2 = None
        direction_vector_y = None
        direction_vector_z = None
        point_on_line_x1 = None
        point_on_line_x2 = None
        point_on_line_y = None
        point_on_line_z = None
        L_x1 = None
        P_x1_x2 = None
        V_x1_y = None
        V_x1_z = None
        V_y_z = None
        results_table = []

        if uploaded_file:
            # 엑셀 파일에서 'Data' 시트를 읽어옵니다.
            data = pd.read_excel(uploaded_file, sheet_name=0)

            # NaN 값 처리 (평균으로 대체)
            data = data.fillna(data.mean())

            # 업로드된 데이터 표시
            st.subheader("업로드된 데이터")
            st.write(data)

            # 데이터 추출 (각 축에 대한 x, y, z 좌표 사용)
            required_columns = [['X1_x', 'X1_y', 'X1_z'], ['X2_x', 'X2_y', 'X2_z'], ['Y_x', 'Y_y', 'Y_z'], ['Z_x', 'Z_y', 'Z_z']]
            data_points = {}
            for cols in required_columns:
                if all(col in data.columns for col in cols):
                    data_points[cols[0].split('_')[0]] = data[cols].dropna().values
                else:
                    st.warning(f"열 {cols}이(가) 누락되었습니다. 해당 데이터를 건너뜁니다.")

            if not data_points:
                st.error("필요한 데이터가 충분하지 않습니다. 올바른 데이터를 포함하고 있는지 확인하세요.")
                st.stop()

            data_points_x1 = data_points.get('X1', None)
            data_points_x2 = data_points.get('X2', None)
            data_points_y = data_points.get('Y', None)
            data_points_z = data_points.get('Z', None)

            # PCA를 사용하여 각 축에 대한 주성분 찾기
            def fit_pca(data_points):
                if data_points is not None:
                    pca = PCA(n_components=1)
                    pca.fit(data_points)
                    return pca.components_[0], pca.mean_
                return None, None

            direction_vector_x1, point_on_line_x1 = fit_pca(data_points_x1) if data_points_x1 is not None else (None, None)
            direction_vector_x2, point_on_line_x2 = fit_pca(data_points_x2) if data_points_x2 is not None else (None, None)
            direction_vector_y, point_on_line_y = fit_pca(data_points_y) if data_points_y is not None else (None, None)
            direction_vector_z, point_on_line_z = fit_pca(data_points_z) if data_points_z is not None else (None, None)

            # 진직도, 평행도, 수직도 정량 값 계산
            L_x1 = np.mean([np.linalg.norm(point - (point_on_line_x1 + np.dot(point - point_on_line_x1, direction_vector_x1) * direction_vector_x1)) for point in data_points_x1]) if data_points_x1 is not None and point_on_line_x1 is not None else None
            L_x2 = np.mean([np.linalg.norm(point - (point_on_line_x2 + np.dot(point - point_on_line_x2, direction_vector_x2) * direction_vector_x2)) for point in data_points_x2]) if data_points_x2 is not None and point_on_line_x2 is not None else None
            L_y = np.mean([np.linalg.norm(point - (point_on_line_y + np.dot(point - point_on_line_y, direction_vector_y) * direction_vector_y)) for point in data_points_y]) if data_points_y is not None and point_on_line_y is not None else None
            L_z = np.mean([np.linalg.norm(point - (point_on_line_z + np.dot(point - point_on_line_z, direction_vector_z) * direction_vector_z)) for point in data_points_z]) if data_points_z is not None and point_on_line_z is not None else None
            P_x1_x2 = np.degrees(np.arccos(np.clip(np.dot(direction_vector_x1, direction_vector_x2) / (np.linalg.norm(direction_vector_x1) * np.linalg.norm(direction_vector_x2)), -1.0, 1.0))) if direction_vector_x1 is not None and direction_vector_x2 is not None else None
            V_x1_y = np.degrees(np.arccos(np.clip(np.abs(np.dot(direction_vector_x1, direction_vector_y)) / (np.linalg.norm(direction_vector_x1) * np.linalg.norm(direction_vector_y)), -1.0, 1.0))) if direction_vector_x1 is not None and direction_vector_y is not None else None
            V_x1_z = np.degrees(np.arccos(np.clip(np.abs(np.dot(direction_vector_x1, direction_vector_z)) / (np.linalg.norm(direction_vector_x1) * np.linalg.norm(direction_vector_z)), -1.0, 1.0))) if direction_vector_x1 is not None and direction_vector_z is not None else None
            V_y_z = np.degrees(np.arccos(np.clip(np.abs(np.dot(direction_vector_y, direction_vector_z)) / (np.linalg.norm(direction_vector_y) * np.linalg.norm(direction_vector_z)), -1.0, 1.0))) if direction_vector_y is not None and direction_vector_z is not None else None

            # 결과 테이블에 추가
            if L_x1 is not None:
                results_table.append(["진직도 (L)", "기준: X1", "측정 대상: X1", f"{L_x1:.4f}"])
            if L_x2 is not None:
                results_table.append(["진직도 (L)", "기준: X2", "측정 대상: X2", f"{L_x2:.4f}"])
            if L_y is not None:
                results_table.append(["진직도 (L)", "기준: Y", "측정 대상: Y", f"{L_y:.4f}"])
            if L_z is not None:
                results_table.append(["진직도 (L)", "기준: Z", "측정 대상: Z", f"{L_z:.4f}"])
            if P_x1_x2 is not None:
                results_table.append(["평행도 (P)", "기준: X1", "측정 대상: X2", f"{P_x1_x2:.2f}°"])
            if V_x1_y is not None:
                results_table.append(["수직도 (V)", "기준: X1", "측정 대상: Y", f"{V_x1_y:.2f}°"])
            if V_x1_z is not None:
                results_table.append(["수직도 (V)", "기준: X1", "측정 대상: Z", f"{V_x1_z:.2f}°"])
            if V_y_z is not None:
                results_table.append(["수직도 (V)", "기준: Y", "측정 대상: Z", f"{V_y_z:.2f}°"])

    with result_tab:
        st.header("평가 결과")
        # 3차원 그래프 시각화
        st.subheader("3D 시각화 결과")
        fig = go.Figure()

        # 각 데이터 점들 시각화
        if data_points_x1 is not None:
            fig.add_trace(go.Scatter3d(x=data_points_x1[:, 0], y=data_points_x1[:, 1], z=data_points_x1[:, 2],
                                       mode='markers', marker=dict(size=5, color='blue'), name='X1 Data Points'))
        if data_points_x2 is not None:
            fig.add_trace(go.Scatter3d(x=data_points_x2[:, 0], y=data_points_x2[:, 1], z=data_points_x2[:, 2],
                                       mode='markers', marker=dict(size=5, color='green'), name='X2 Data Points'))
        if data_points_y is not None:
            fig.add_trace(go.Scatter3d(x=data_points_y[:, 0], y=data_points_y[:, 1], z=data_points_y[:, 2],
                                       mode='markers', marker=dict(size=5, color='orange'), name='Y Data Points'))
        if data_points_z is not None:
            fig.add_trace(go.Scatter3d(x=data_points_z[:, 0], y=data_points_z[:, 1], z=data_points_z[:, 2],
                                       mode='markers', marker=dict(size=5, color='purple'), name='Z Data Points'))

        # 적합된 직선 시각화 (각 주성분)
        max_range = max(np.ptp(data_points_x1) if data_points_x1 is not None else 0,
                        np.ptp(data_points_x2) if data_points_x2 is not None else 0,
                        np.ptp(data_points_y) if data_points_y is not None else 0,
                        np.ptp(data_points_z) if data_points_z is not None else 0)
        max_range = max_range if max_range > 0 else 50
        t_vals = np.linspace(-0.5 * max_range, 0.5 * max_range, 100)

        if data_points_x1 is not None:
            line_points_x1 = point_on_line_x1 + t_vals[:, np.newaxis] * direction_vector_x1
            fig.add_trace(go.Scatter3d(x=line_points_x1[:, 0], y=line_points_x1[:, 1], z=line_points_x1[:, 2],
                                       mode='lines', line=dict(color='red', width=3), name='X1 Principal Component'))
        if data_points_x2 is not None:
            line_points_x2 = point_on_line_x2 + t_vals[:, np.newaxis] * direction_vector_x2
            fig.add_trace(go.Scatter3d(x=line_points_x2[:, 0], y=line_points_x2[:, 1], z=line_points_x2[:, 2],
                                       mode='lines', line=dict(color='cyan', width=3), name='X2 Principal Component'))
        if data_points_y is not None:
            line_points_y = point_on_line_y + t_vals[:, np.newaxis] * direction_vector_y
            fig.add_trace(go.Scatter3d(x=line_points_y[:, 0], y=line_points_y[:, 1], z=line_points_y[:, 2],
                                       mode='lines', line=dict(color='yellow', width=3), name='Y Principal Component'))
        if data_points_z is not None:
            line_points_z = point_on_line_z + t_vals[:, np.newaxis] * direction_vector_z
            fig.add_trace(go.Scatter3d(x=line_points_z[:, 0], y=line_points_z[:, 1], z=line_points_z[:, 2],
                                       mode='lines', line=dict(color='magenta', width=3), name='Z Principal Component'))

        # 레이아웃 설정
        fig.update_layout(scene=dict(
            xaxis_title='X axis',
            yaxis_title='Y axis',
            zaxis_title='Z axis'
        ))

        # 시각화 결과를 Streamlit에 표시
        st.plotly_chart(fig, use_container_width=True)

        if results_table:
            results_df = pd.DataFrame(results_table, columns=["평가 항목", "기준", "측정 대상", "결과"])
            st.table(results_df)

    with method_tab:
        st.header("평가 방법")
        # 결과 설명 및 평가 방법 소개
        st.subheader("진직도, 평행도, 수직도 평가 방법")
        st.markdown(r"""
        - **진직도 (Linearity, L)**: 데이터 점들이 주성분 직선에 얼마나 가까운지를 나타내는 척도입니다. 이는 각 데이터 점에서 직선까지의 평균 거리를 통해 평가합니다. 수식으로 표현하면:
          
          $$
          L = \frac{1}{N} \sum_{i=1}^{N} d_i
          $$
          
          여기서 $d_i$는 각 데이터 점에서 직선까지의 거리이며, $N$은 데이터 점의 개수입니다.
        
        - **평행도 (Parallelism, P)**: 특정 축에 대한 데이터의 평행성을 평가합니다. 주성분 방향 벡터와 데이터 점들이 해당 축에 대해 얼마나 평행한지를 확인합니다. 수식으로 표현하면:
          
          $$
          P = \cos(\theta) = \frac{a \cdot b}{\|a\| \|b\|}
          $$
          
          여기서 $a$와 $b$는 두 벡터이며, $\theta$는 이들 사이의 각도입니다.
        
        - **수직도 (Perpendicularity, V)**: 특정 축에 대해 데이터 점들이 수직으로 잘 분포되어 있는지를 평가합니다. 이는 주성분 벡터와의 수직도를 통해 계산합니다.
        
        - **PCA 주성분 분석 (Principal Component Analysis, PCA)**: PCA는 고차원의 데이터를 저차원으로 축소하면서도 데이터의 분산을 최대화하는 기법입니다. 데이터의 주요 방향을 찾기 위해 사용됩니다. 주성분 벡터는 데이터의 최대 분산 방향을 나타내며, 이는 공분산 행렬의 고유벡터를 통해 계산됩니다. PCA의 계산 과정은 다음과 같습니다:
          
          1. **데이터 중심화**: 각 데이터에서 평균을 빼서 데이터의 중심을 원점으로 이동시킵니다.
             $$
             X_{centered} = X - \text{mean}(X)
             $$
          
          2. **공분산 행렬 계산**: 중심화된 데이터의 공분산 행렬을 계산합니다.
             $$
             C = \frac{1}{N-1} X_{centered}^T X_{centered}
             $$
          
          3. **고유값 분해**: 공분산 행렬 $C$의 고유값과 고유벡터를 계산합니다. 고유벡터는 데이터의 주성분을 나타내며, 고유값은 해당 주성분의 중요도를 나타냅니다.
             $$
             C v = \lambda v
             $$
             여기서 $v$는 고유벡터, $\lambda$는 고유값입니다.
          
          4. **주성분 선택**: 가장 큰 고유값에 해당하는 고유벡터를 선택하여 데이터의 주요 분산 방향을 나타내는 주성분으로 사용합니다.
        
        PCA는 데이터의 차원을 축소하면서도 원래 데이터의 분산을 최대한 보존하려고 합니다. 이를 통해 데이터의 구조를 간단하게 표현하고, 시각화나 분석을 더 쉽게 할 수 있습니다.
        """)

elif analysis_type == "속도 및 가속도 분석":
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
