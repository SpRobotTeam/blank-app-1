import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from io import BytesIO

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, error_handler, success_message, info_message
from utils.data_processing import safe_operation, preprocess_excel_data, create_download_link

@safe_operation
def speed_analysis():
    """
    속도 및 가속도 분석 도구
    시간-속도 데이터를 바탕으로 가속도, 이동거리, 통계 분석을 수행합니다.
    """
    # 도구 헤더 적용
    tool_header(
        "속도 및 가속도 분석 도구", 
        "시간-속도 데이터를 분석하여 가속도, 이동거리를 계산하고 운동 특성을 시각화합니다. 자동차, 로봇, 기계 등의 운동 분석에 활용할 수 있습니다."
    )

    # 탭 구성
    input_tab, analysis_tab, visualization_tab, report_tab = st.tabs([
        "📁 데이터 입력", "📊 분석 설정", "📈 시각화", "📋 분석 리포트"
    ])

    # 세션 상태 초기화
    if 'speed_data' not in st.session_state:
        st.session_state.speed_data = None
        st.session_state.analysis_results = None

    with input_tab:
        display_input_section()

    with analysis_tab:
        display_analysis_section()

    with visualization_tab:
        display_visualization_section()

    with report_tab:
        display_report_section()

def display_input_section():
    """데이터 입력 섹션"""
    st.header("📁 데이터 입력")
    
    # 파일 업로드 영역
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📊 엑셀 파일을 업로드하세요", 
            type=["xlsx", "xls"],
            key="speed_analysis",
            help="시간과 속도 데이터가 포함된 엑셀 파일을 업로드합니다."
        )
    
    with col2:
        if st.button("📋 템플릿 다운로드", help="데이터 입력 템플릿을 다운로드합니다."):
            create_template_download()

    # 데이터 전처리 옵션
    st.subheader("⚙️ 데이터 전처리 옵션")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fill_strategy = st.selectbox(
            "누락값 처리:",
            options=["해당 행 제거", "선형 보간", "0으로 대체"],
            index=0,
            help="누락된 데이터의 처리 방법을 선택합니다."
        )
    
    with col2:
        smooth_data = st.checkbox(
            "데이터 스무딩",
            value=False,
            help="노이즈 제거를 위한 데이터 스무딩을 적용합니다."
        )
    
    with col3:
        if smooth_data:
            smooth_window = st.slider(
                "스무딩 윈도우 크기:",
                min_value=3,
                max_value=21,
                value=5,
                step=2,
                help="스무딩에 사용할 윈도우 크기를 설정합니다."
            )
        else:
            smooth_window = 5

    # 파일 처리
    if uploaded_file:
        process_uploaded_file(uploaded_file, fill_strategy, smooth_data, smooth_window)
    else:
        display_data_format_guide()

def process_uploaded_file(uploaded_file, fill_strategy, smooth_data, smooth_window):
    """업로드된 파일 처리"""
    try:
        with st.spinner("📊 데이터를 분석하는 중..."):
            # 엑셀 파일 읽기
            data = pd.read_excel(uploaded_file, sheet_name=0)
            
            # 필수 컬럼 확인
            required_columns = ['Time_sec', 'Velocity_m/s']
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                error_handler(f"필수 컬럼이 누락되었습니다: {', '.join(missing_columns)}")
                st.info("💡 필수 컬럼: Time_sec (시간, 초), Velocity_m/s (속도, m/s)")
                return
            
            # 데이터 전처리
            data = preprocess_speed_data(data, fill_strategy, smooth_data, smooth_window)
            
            # 세션에 저장
            st.session_state.speed_data = data
            
            success_message(f"데이터가 성공적으로 로드되었습니다. ({len(data)} 개 데이터 포인트)")
            
            # 데이터 미리보기
            display_data_preview(data)
            
            # 기본 분석 수행
            perform_speed_analysis(data)
            
    except Exception as e:
        error_handler(f"파일 처리 중 오류가 발생했습니다: {str(e)}")

def preprocess_speed_data(data, fill_strategy, smooth_data, smooth_window):
    """속도 데이터 전처리"""
    # 기본 정렬 (시간 순)
    data = data.sort_values('Time_sec').reset_index(drop=True)
    
    # 누락값 처리
    if fill_strategy == "해당 행 제거":
        data = data.dropna(subset=['Time_sec', 'Velocity_m/s'])
    elif fill_strategy == "선형 보간":
        data['Velocity_m/s'] = data['Velocity_m/s'].interpolate(method='linear')
        data = data.dropna(subset=['Time_sec', 'Velocity_m/s'])
    elif fill_strategy == "0으로 대체":
        data[['Time_sec', 'Velocity_m/s']] = data[['Time_sec', 'Velocity_m/s']].fillna(0)
    
    # 데이터 스무딩
    if smooth_data and len(data) > smooth_window:
        data['Velocity_m/s'] = data['Velocity_m/s'].rolling(
            window=smooth_window, center=True, min_periods=1
        ).mean()
    
    return data

def display_data_preview(data):
    """데이터 미리보기"""
    st.subheader("📋 데이터 미리보기")
    
    # 통계 정보
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 데이터 포인트", len(data))
    with col2:
        st.metric("시간 범위", f"{data['Time_sec'].iloc[-1] - data['Time_sec'].iloc[0]:.2f}초")
    with col3:
        st.metric("최대 속도", f"{data['Velocity_m/s'].max():.2f} m/s")
    with col4:
        st.metric("평균 속도", f"{data['Velocity_m/s'].mean():.2f} m/s")
    
    # 데이터 테이블
    st.dataframe(data.head(10), use_container_width=True)
    
    # 기본 통계
    with st.expander("📊 기본 통계 정보"):
        st.dataframe(data.describe(), use_container_width=True)

def perform_speed_analysis(data):
    """속도 분석 수행"""
    try:
        time = data['Time_sec'].values
        velocity = data['Velocity_m/s'].values
        
        # 가속도 계산 (속도의 시간 미분)
        acceleration = np.gradient(velocity, time)
        
        # 이동거리 계산 (속도의 시간 적분)
        # 사다리꼴 공식 사용
        distance = np.zeros_like(time)
        for i in range(1, len(time)):
            dt = time[i] - time[i-1]
            distance[i] = distance[i-1] + (velocity[i-1] + velocity[i]) * dt / 2
        
        # 저크(Jerk) 계산 (가속도의 시간 미분)
        jerk = np.gradient(acceleration, time)
        
        # 결과 데이터프레임 생성
        results_df = pd.DataFrame({
            'Time_sec': time,
            'Velocity_m/s': velocity,
            'Acceleration_m/s2': acceleration,
            'Distance_m': distance,
            'Jerk_m/s3': jerk
        })
        
        # 통계 분석
        statistics = calculate_statistics(results_df)
        
        # 세션에 저장
        st.session_state.analysis_results = {
            'data': results_df,
            'statistics': statistics
        }
        
        success_message("속도 분석이 완료되었습니다. 다른 탭에서 결과를 확인하세요.")
        
    except Exception as e:
        error_handler(f"분석 중 오류가 발생했습니다: {str(e)}")

def calculate_statistics(df):
    """통계 분석 계산"""
    statistics = {}
    
    # 기본 통계
    statistics['basic'] = {
        'total_time': df['Time_sec'].iloc[-1] - df['Time_sec'].iloc[0],
        'total_distance': df['Distance_m'].iloc[-1],
        'max_velocity': df['Velocity_m/s'].max(),
        'min_velocity': df['Velocity_m/s'].min(),
        'avg_velocity': df['Velocity_m/s'].mean(),
        'max_acceleration': df['Acceleration_m/s2'].max(),
        'min_acceleration': df['Acceleration_m/s2'].min(),
        'avg_acceleration': df['Acceleration_m/s2'].mean(),
        'max_jerk': df['Jerk_m/s3'].max(),
        'min_jerk': df['Jerk_m/s3'].min()
    }
    
    # 운동 상태 분석
    statistics['motion_states'] = analyze_motion_states(df)
    
    # 성능 지표
    statistics['performance'] = calculate_performance_metrics(df)
    
    return statistics

def analyze_motion_states(df):
    """운동 상태 분석"""
    velocity = df['Velocity_m/s'].values
    acceleration = df['Acceleration_m/s2'].values
    time = df['Time_sec'].values
    
    # 가속, 감속, 등속 구간 식별
    acc_threshold = 0.1  # m/s²
    
    accelerating = acceleration > acc_threshold
    decelerating = acceleration < -acc_threshold
    constant_speed = np.abs(acceleration) <= acc_threshold
    
    # 각 상태의 시간 계산
    dt = np.gradient(time)
    
    motion_states = {
        'accelerating_time': np.sum(dt[accelerating]),
        'decelerating_time': np.sum(dt[decelerating]),
        'constant_speed_time': np.sum(dt[constant_speed]),
        'accelerating_ratio': np.sum(accelerating) / len(acceleration) * 100,
        'decelerating_ratio': np.sum(decelerating) / len(acceleration) * 100,
        'constant_speed_ratio': np.sum(constant_speed) / len(acceleration) * 100
    }
    
    return motion_states

def calculate_performance_metrics(df):
    """성능 지표 계산"""
    velocity = df['Velocity_m/s'].values
    acceleration = df['Acceleration_m/s2'].values
    time = df['Time_sec'].values
    
    # 0-60 가속 시간 (0에서 60 km/h = 16.67 m/s)
    target_speed = 16.67  # m/s (60 km/h)
    zero_to_target_time = None
    
    if velocity.max() >= target_speed:
        target_idx = np.where(velocity >= target_speed)[0]
        if len(target_idx) > 0:
            zero_to_target_time = time[target_idx[0]]
    
    # RMS (Root Mean Square) 값들
    rms_acceleration = np.sqrt(np.mean(acceleration**2))
    rms_velocity = np.sqrt(np.mean(velocity**2))
    
    # 효율성 지표 (평균 속도 / 최대 속도)
    efficiency = df['Velocity_m/s'].mean() / df['Velocity_m/s'].max() * 100
    
    performance = {
        'zero_to_60kmh_time': zero_to_target_time,
        'rms_acceleration': rms_acceleration,
        'rms_velocity': rms_velocity,
        'efficiency_ratio': efficiency,
        'velocity_std': df['Velocity_m/s'].std(),
        'acceleration_std': df['Acceleration_m/s2'].std()
    }
    
    return performance

def display_analysis_section():
    """분석 설정 섹션"""
    st.header("📊 분석 설정 및 요약")
    
    if st.session_state.analysis_results is None:
        info_message("먼저 '데이터 입력' 탭에서 데이터를 업로드하세요.")
        return
    
    results = st.session_state.analysis_results
    stats = results['statistics']
    
    # 기본 통계 표시
    display_basic_statistics(stats['basic'])
    
    # 운동 상태 분석
    display_motion_analysis(stats['motion_states'])
    
    # 성능 지표
    display_performance_metrics(stats['performance'])
    
    # 분석 설정
    display_analysis_settings()

def display_basic_statistics(basic_stats):
    """기본 통계 표시"""
    st.subheader("📈 기본 분석 결과")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**⏱️ 시간 정보**")
        st.metric("총 소요 시간", f"{basic_stats['total_time']:.2f} 초")
        st.metric("총 이동 거리", f"{basic_stats['total_distance']:.2f} m")
    
    with col2:
        st.markdown("**🏃 속도 정보**")
        st.metric("최대 속도", f"{basic_stats['max_velocity']:.2f} m/s")
        st.metric("평균 속도", f"{basic_stats['avg_velocity']:.2f} m/s")
        st.metric("최소 속도", f"{basic_stats['min_velocity']:.2f} m/s")
    
    with col3:
        st.markdown("**⚡ 가속도 정보**")
        st.metric("최대 가속도", f"{basic_stats['max_acceleration']:.2f} m/s²")
        st.metric("평균 가속도", f"{basic_stats['avg_acceleration']:.2f} m/s²")
        st.metric("최대 저크", f"{basic_stats['max_jerk']:.2f} m/s³")

def display_motion_analysis(motion_states):
    """운동 상태 분석 표시"""
    st.subheader("🔄 운동 상태 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 운동 상태 시간 분포
        st.markdown("**시간 분포**")
        st.metric("가속 시간", f"{motion_states['accelerating_time']:.2f} 초")
        st.metric("감속 시간", f"{motion_states['decelerating_time']:.2f} 초")
        st.metric("등속 시간", f"{motion_states['constant_speed_time']:.2f} 초")
    
    with col2:
        # 운동 상태 비율
        st.markdown("**비율 분포**")
        motion_data = {
            'State': ['가속', '감속', '등속'],
            'Ratio': [
                motion_states['accelerating_ratio'],
                motion_states['decelerating_ratio'],
                motion_states['constant_speed_ratio']
            ]
        }
        
        fig = px.pie(
            values=motion_data['Ratio'],
            names=motion_data['State'],
            title="운동 상태 분포"
        )
        st.plotly_chart(fig, use_container_width=True)

def display_performance_metrics(performance):
    """성능 지표 표시"""
    st.subheader("🏆 성능 지표")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if performance['zero_to_60kmh_time']:
            st.metric("0-60km/h", f"{performance['zero_to_60kmh_time']:.2f} 초")
        else:
            st.metric("0-60km/h", "N/A")
    
    with col2:
        st.metric("RMS 가속도", f"{performance['rms_acceleration']:.2f} m/s²")
    
    with col3:
        st.metric("효율성", f"{performance['efficiency_ratio']:.1f}%")
    
    with col4:
        st.metric("속도 안정성", f"{100 - performance['velocity_std']:.1f}%")

def display_analysis_settings():
    """분석 설정"""
    st.subheader("⚙️ 고급 분석 설정")
    
    with st.expander("필터 및 분석 옵션"):
        col1, col2 = st.columns(2)
        
        with col1:
            time_range = st.slider(
                "분석 시간 범위 (초)",
                min_value=0.0,
                max_value=float(st.session_state.analysis_results['data']['Time_sec'].max()),
                value=(0.0, float(st.session_state.analysis_results['data']['Time_sec'].max())),
                help="분석할 시간 범위를 선택합니다."
            )
        
        with col2:
            analysis_type = st.multiselect(
                "분석 항목 선택",
                options=["속도", "가속도", "이동거리", "저크"],
                default=["속도", "가속도", "이동거리"],
                help="시각화할 분석 항목을 선택합니다."
            )
        
        if st.button("🔄 분석 업데이트"):
            update_analysis_with_filters(time_range, analysis_type)

def update_analysis_with_filters(time_range, analysis_type):
    """필터가 적용된 분석 업데이트"""
    if st.session_state.analysis_results:
        df = st.session_state.analysis_results['data']
        
        # 시간 범위 필터링
        mask = (df['Time_sec'] >= time_range[0]) & (df['Time_sec'] <= time_range[1])
        filtered_df = df[mask]
        
        st.session_state.filtered_data = filtered_df
        st.session_state.selected_analysis = analysis_type
        
        success_message("분석이 업데이트되었습니다.")

def display_visualization_section():
    """시각화 섹션"""
    st.header("📈 시각화")
    
    if st.session_state.analysis_results is None:
        info_message("먼저 '데이터 입력' 탭에서 데이터를 업로드하세요.")
        return
    
    df = st.session_state.analysis_results['data']
    
    # 시각화 옵션
    viz_options = display_visualization_options()
    
    # 통합 시각화
    if viz_options['show_combined']:
        display_combined_visualization(df)
    
    # 개별 시각화
    if viz_options['show_individual']:
        display_individual_visualizations(df)
    
    # 3D 시각화
    if viz_options['show_3d']:
        display_3d_visualization(df)

def display_visualization_options():
    """시각화 옵션"""
    st.subheader("🎨 시각화 옵션")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_combined = st.checkbox("통합 차트", value=True)
    with col2:
        show_individual = st.checkbox("개별 차트", value=True)
    with col3:
        show_3d = st.checkbox("3D 궤적", value=False)
    
    return {
        'show_combined': show_combined,
        'show_individual': show_individual,
        'show_3d': show_3d
    }

def display_combined_visualization(df):
    """통합 시각화"""
    st.subheader("📊 통합 시각화")
    
    # 서브플롯 생성
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=('속도 (m/s)', '가속도 (m/s²)', '이동거리 (m)', '저크 (m/s³)'),
        vertical_spacing=0.08
    )
    
    # 속도
    fig.add_trace(
        go.Scatter(x=df['Time_sec'], y=df['Velocity_m/s'], 
                  name='속도', line=dict(color='blue')),
        row=1, col=1
    )
    
    # 가속도
    fig.add_trace(
        go.Scatter(x=df['Time_sec'], y=df['Acceleration_m/s2'], 
                  name='가속도', line=dict(color='red')),
        row=2, col=1
    )
    
    # 이동거리
    fig.add_trace(
        go.Scatter(x=df['Time_sec'], y=df['Distance_m'], 
                  name='이동거리', line=dict(color='green')),
        row=3, col=1
    )
    
    # 저크
    fig.add_trace(
        go.Scatter(x=df['Time_sec'], y=df['Jerk_m/s3'], 
                  name='저크', line=dict(color='orange')),
        row=4, col=1
    )
    
    fig.update_layout(
        height=800,
        title_text="속도, 가속도, 이동거리, 저크 분석 결과",
        showlegend=False
    )
    
    fig.update_xaxes(title_text="시간 (초)", row=4, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

def display_individual_visualizations(df):
    """개별 시각화"""
    st.subheader("📈 개별 분석 차트")
    
    # 속도-시간 그래프
    fig_velocity = px.line(df, x='Time_sec', y='Velocity_m/s', 
                          title='속도-시간 그래프',
                          labels={'Time_sec': '시간 (초)', 'Velocity_m/s': '속도 (m/s)'})
    fig_velocity.update_traces(line=dict(color='blue', width=2))
    st.plotly_chart(fig_velocity, use_container_width=True)
    
    # 가속도-시간 그래프
    fig_acceleration = px.line(df, x='Time_sec', y='Acceleration_m/s2',
                              title='가속도-시간 그래프',
                              labels={'Time_sec': '시간 (초)', 'Acceleration_m/s2': '가속도 (m/s²)'})
    fig_acceleration.update_traces(line=dict(color='red', width=2))
    
    # 0선 추가
    fig_acceleration.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    st.plotly_chart(fig_acceleration, use_container_width=True)
    
    # 속도-가속도 상관관계
    fig_correlation = px.scatter(df, x='Velocity_m/s', y='Acceleration_m/s2',
                                title='속도-가속도 상관관계',
                                labels={'Velocity_m/s': '속도 (m/s)', 'Acceleration_m/s2': '가속도 (m/s²)'},
                                color='Time_sec',
                                color_continuous_scale='viridis')
    st.plotly_chart(fig_correlation, use_container_width=True)

def display_3d_visualization(df):
    """3D 시각화"""
    st.subheader("🌐 3D 궤적 시각화")
    
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=df['Time_sec'],
        y=df['Velocity_m/s'],
        z=df['Acceleration_m/s2'],
        mode='markers+lines',
        marker=dict(
            size=4,
            color=df['Distance_m'],
            colorscale='viridis',
            colorbar=dict(title="이동거리 (m)"),
            showscale=True
        ),
        line=dict(color='blue', width=2),
        text=[f"시간: {t:.2f}s<br>속도: {v:.2f}m/s<br>가속도: {a:.2f}m/s²" 
              for t, v, a in zip(df['Time_sec'], df['Velocity_m/s'], df['Acceleration_m/s2'])],
        hovertemplate='%{text}<extra></extra>',
        name='운동 궤적'
    )])
    
    fig_3d.update_layout(
        title='3D 운동 궤적 (시간-속도-가속도)',
        scene=dict(
            xaxis_title='시간 (초)',
            yaxis_title='속도 (m/s)',
            zaxis_title='가속도 (m/s²)'
        ),
        width=800,
        height=600
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)

def display_report_section():
    """분석 리포트 섹션"""
    st.header("📋 분석 리포트")
    
    if st.session_state.analysis_results is None:
        info_message("먼저 '데이터 입력' 탭에서 데이터를 업로드하세요.")
        return
    
    results = st.session_state.analysis_results
    
    # 종합 분석 리포트
    display_comprehensive_report(results)
    
    # 데이터 내보내기
    display_export_options(results['data'])

def display_comprehensive_report(results):
    """종합 분석 리포트"""
    st.subheader("📊 종합 분석 리포트")
    
    df = results['data']
    stats = results['statistics']
    
    # 요약 정보
    st.markdown("### 🎯 분석 요약")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **📈 주요 지표:**
        - 총 분석 시간: {stats['basic']['total_time']:.2f} 초
        - 총 이동 거리: {stats['basic']['total_distance']:.2f} m
        - 최대 속도: {stats['basic']['max_velocity']:.2f} m/s ({stats['basic']['max_velocity']*3.6:.1f} km/h)
        - 평균 속도: {stats['basic']['avg_velocity']:.2f} m/s ({stats['basic']['avg_velocity']*3.6:.1f} km/h)
        """)
    
    with col2:
        st.markdown(f"""
        **⚡ 가속도 특성:**
        - 최대 가속도: {stats['basic']['max_acceleration']:.2f} m/s²
        - 최대 감속도: {stats['basic']['min_acceleration']:.2f} m/s²
        - RMS 가속도: {stats['performance']['rms_acceleration']:.2f} m/s²
        - 최대 저크: {stats['basic']['max_jerk']:.2f} m/s³
        """)
    
    # 운동 특성 분석
    st.markdown("### 🔄 운동 특성 분석")
    
    motion = stats['motion_states']
    st.markdown(f"""
    **운동 상태 분포:**
    - 가속 구간: {motion['accelerating_ratio']:.1f}% ({motion['accelerating_time']:.2f}초)
    - 감속 구간: {motion['decelerating_ratio']:.1f}% ({motion['decelerating_time']:.2f}초)
    - 등속 구간: {motion['constant_speed_ratio']:.1f}% ({motion['constant_speed_time']:.2f}초)
    """)
    
    # 성능 평가
    st.markdown("### 🏆 성능 평가")
    
    performance = stats['performance']
    
    # 효율성 평가
    if performance['efficiency_ratio'] > 80:
        efficiency_grade = "우수"
        efficiency_color = "🟢"
    elif performance['efficiency_ratio'] > 60:
        efficiency_grade = "양호"
        efficiency_color = "🟡"
    else:
        efficiency_grade = "개선 필요"
        efficiency_color = "🔴"
    
    st.markdown(f"""
    **성능 지표:**
    - 효율성: {efficiency_color} {performance['efficiency_ratio']:.1f}% ({efficiency_grade})
    - 속도 안정성: {100 - performance['velocity_std']:.1f}%
    - 가속도 변동성: {performance['acceleration_std']:.3f} m/s²
    """)
    
    if performance['zero_to_60kmh_time']:
        st.markdown(f"- 0-60km/h 가속 시간: {performance['zero_to_60kmh_time']:.2f} 초")
    
    # 개선 권장사항
    st.markdown("### 💡 개선 권장사항")
    recommendations = generate_recommendations(stats)
    for rec in recommendations:
        st.write(f"• {rec}")

def generate_recommendations(stats):
    """개선 권장사항 생성"""
    recommendations = []
    
    performance = stats['performance']
    motion = stats['motion_states']
    basic = stats['basic']
    
    # 효율성 기반 권장사항
    if performance['efficiency_ratio'] < 60:
        recommendations.append("전체적인 운행 효율성이 낮습니다. 불필요한 가속/감속을 줄여보세요.")
    
    # 가속도 변동성 기반 권장사항
    if performance['acceleration_std'] > 2.0:
        recommendations.append("가속도 변동이 큽니다. 더 부드러운 가속/감속 패턴을 고려해보세요.")
    
    # 운동 상태 기반 권장사항
    if motion['accelerating_ratio'] > 50:
        recommendations.append("가속 구간이 많습니다. 적절한 속도 유지로 에너지 효율을 개선할 수 있습니다.")
    
    if motion['constant_speed_ratio'] < 20:
        recommendations.append("등속 구간이 부족합니다. 일정한 속도 유지로 안정성을 높여보세요.")
    
    # 속도 기반 권장사항
    if basic['max_velocity'] > basic['avg_velocity'] * 3:
        recommendations.append("최대 속도와 평균 속도의 차이가 큽니다. 속도 변화를 완만하게 해보세요.")
    
    if not recommendations:
        recommendations.append("전반적으로 양호한 운동 특성을 보입니다. 현재 패턴을 유지하세요.")
    
    return recommendations

def display_export_options(df):
    """데이터 내보내기 옵션"""
    st.subheader("📥 데이터 내보내기")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Excel 내보내기
        excel_buffer = create_excel_export(df)
        st.download_button(
            label="📊 Excel로 내보내기",
            data=excel_buffer,
            file_name='speed_analysis_results.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            help="분석 결과를 Excel 파일로 다운로드합니다."
        )
    
    with col2:
        # CSV 내보내기
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 CSV로 내보내기",
            data=csv_data,
            file_name='speed_analysis_results.csv',
            mime='text/csv',
            help="분석 결과를 CSV 파일로 다운로드합니다."
        )

def create_excel_export(df):
    """Excel 내보내기 파일 생성"""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Analysis Results', index=False)
        
        # 워크시트 서식 지정
        workbook = writer.book
        worksheet = writer.sheets['Analysis Results']
        
        # 헤더 서식
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        # 헤더 적용
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # 열 너비 조정
        worksheet.set_column('A:E', 15)
    
    buffer.seek(0)
    return buffer

def display_data_format_guide():
    """데이터 형식 가이드"""
    st.subheader("📋 데이터 형식 안내")
    
    st.markdown("""
    **필요한 데이터 형식:**
    
    엑셀 파일에는 다음 컬럼이 포함되어야 합니다:
    
    | 컬럼명 | 설명 | 단위 | 예시 |
    |--------|------|------|------|
    | Time_sec | 시간 | 초 | 0.0, 0.1, 0.2, ... |
    | Velocity_m/s | 속도 | m/s | 0.0, 2.5, 5.0, ... |
    
    **참고사항:**
    - 시간 데이터는 오름차순으로 정렬되어야 합니다.
    - 가속도, 이동거리, 저크는 자동으로 계산됩니다.
    - 최소 10개 이상의 데이터 포인트를 권장합니다.
    """)

def create_template_download():
    """템플릿 다운로드 생성"""
    # 샘플 데이터 생성 (가속 → 등속 → 감속 패턴)
    time_data = np.linspace(0, 10, 101)  # 0-10초, 0.1초 간격
    velocity_data = np.zeros_like(time_data)
    
    # 가속 구간 (0-3초): 0 → 15 m/s
    acc_mask = time_data <= 3
    velocity_data[acc_mask] = 2.5 * time_data[acc_mask]**2
    
    # 등속 구간 (3-7초): 15 m/s 유지
    const_mask = (time_data > 3) & (time_data <= 7)
    velocity_data[const_mask] = 15
    
    # 감속 구간 (7-10초): 15 → 0 m/s
    dec_mask = time_data > 7
    t_dec = time_data[dec_mask] - 7
    velocity_data[dec_mask] = 15 * (1 - (t_dec/3)**2)
    
    # 음수 속도 방지
    velocity_data = np.maximum(velocity_data, 0)
    
    template_data = pd.DataFrame({
        'Time_sec': time_data,
        'Velocity_m/s': velocity_data
    })
    
    # Excel 파일로 변환
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        template_data.to_excel(writer, index=False, sheet_name='Speed Data')
        
        # 워크시트 서식
        workbook = writer.book
        worksheet = writer.sheets['Speed Data']
        
        # 헤더 서식
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        for col_num, value in enumerate(template_data.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        worksheet.set_column('A:B', 15)
    
    buffer.seek(0)
    
    st.download_button(
        label="📥 템플릿 다운로드",
        data=buffer,
        file_name='speed_analysis_template.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        help="속도 분석을 위한 데이터 템플릿을 다운로드합니다."
    )

# 메인 실행
if __name__ == "__main__":
    speed_analysis()
