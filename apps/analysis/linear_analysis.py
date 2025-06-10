import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import plotly.graph_objs as go
import streamlit as st

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, error_handler, success_message, info_message
from utils.data_processing import safe_operation, preprocess_excel_data

@safe_operation
def linearity_analysis():
    """
    3D 선형성 평가 도구
    진직도, 평행도, 수직도를 평가하고 PCA를 이용한 주성분 분석을 수행합니다.
    """
    # 도구 헤더 적용
    tool_header(
        "3D 선형성 평가 도구", 
        "3차원 데이터의 진직도, 평행도, 수직도를 평가하고 PCA 주성분 분석을 통해 시각화합니다. 제조업 품질관리 및 정밀 측정에 활용할 수 있습니다."
    )

    # 탭 구성: 입력, 평가방법, 결과 탭으로 구분
    input_tab, method_tab, result_tab = st.tabs(["📁 데이터 입력", "📊 평가 방법", "📈 분석 결과"])

    # 세션 상태 초기화
    if 'linearity_data' not in st.session_state:
        st.session_state.linearity_data = None
        st.session_state.analysis_results = None

    with input_tab:
        display_input_section()

    with method_tab:
        display_method_section()

    with result_tab:
        display_result_section()

def display_input_section():
    """데이터 입력 섹션 표시"""
    st.header("📁 데이터 입력")
    
    # 파일 업로드 영역
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📊 엑셀 파일을 업로드하세요", 
            type=["xlsx", "xls"],
            help="3D 좌표 데이터가 포함된 엑셀 파일을 업로드합니다."
        )
    
    with col2:
        if st.button("📋 템플릿 다운로드", help="데이터 입력 템플릿을 다운로드합니다."):
            create_template_download()

    # 데이터 전처리 옵션
    st.subheader("⚙️ 데이터 전처리 옵션")
    
    col1, col2 = st.columns(2)
    with col1:
        fill_strategy = st.selectbox(
            "NaN 값 처리 방법:",
            options=["평균으로 대체", "0으로 대체", "해당 행 제거"],
            index=0,
            help="누락된 데이터의 처리 방법을 선택합니다."
        )
    
    with col2:
        outlier_removal = st.checkbox(
            "이상치 제거 (3σ 기준)",
            value=False,
            help="3 시그마 기준을 벗어나는 이상치를 제거합니다."
        )

    # 파일 처리
    if uploaded_file:
        process_uploaded_file(uploaded_file, fill_strategy, outlier_removal)
    else:
        display_data_format_guide()

def process_uploaded_file(uploaded_file, fill_strategy, outlier_removal):
    """업로드된 파일 처리"""
    try:
        with st.spinner("📊 데이터를 분석하는 중..."):
            # 엑셀 파일 읽기
            data = pd.read_excel(uploaded_file, sheet_name=0)
            
            # 필수 컬럼 확인
            required_columns = ['X1_x', 'X1_y', 'X1_z', 'X2_x', 'X2_y', 'X2_z', 
                              'Y_x', 'Y_y', 'Y_z', 'Z_x', 'Z_y', 'Z_z']
            
            available_columns = [col for col in required_columns if col in data.columns]
            
            if len(available_columns) < 3:
                error_handler("최소 하나의 축에 대한 3D 좌표 데이터(x, y, z)가 필요합니다.")
                return
            
            # 데이터 전처리
            fill_strategy_map = {
                "평균으로 대체": "mean",
                "0으로 대체": "zero",
                "해당 행 제거": "drop"
            }
            
            data = preprocess_excel_data(data, fill_strategy=fill_strategy_map[fill_strategy])
            
            # 이상치 제거
            if outlier_removal:
                data = remove_outliers(data, available_columns)
            
            # 세션에 저장
            st.session_state.linearity_data = data
            
            success_message(f"데이터가 성공적으로 로드되었습니다. ({len(data)} 행, {len(available_columns)} 컬럼)")
            
            # 데이터 미리보기
            display_data_preview(data, available_columns)
            
            # 분석 실행
            perform_linearity_analysis(data, available_columns)
            
    except Exception as e:
        error_handler(f"파일 처리 중 오류가 발생했습니다: {str(e)}")

def remove_outliers(data, columns):
    """3σ 기준 이상치 제거"""
    original_len = len(data)
    
    for col in columns:
        if col in data.columns:
            mean = data[col].mean()
            std = data[col].std()
            data = data[abs(data[col] - mean) <= 3 * std]
    
    removed_count = original_len - len(data)
    if removed_count > 0:
        info_message(f"이상치 {removed_count}개 행이 제거되었습니다.")
    
    return data

def display_data_preview(data, available_columns):
    """데이터 미리보기 표시"""
    st.subheader("📋 데이터 미리보기")
    
    # 통계 정보
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 행 수", len(data))
    with col2:
        st.metric("사용 가능한 축", len(set([col.split('_')[0] for col in available_columns])))
    with col3:
        st.metric("총 컬럼 수", len(available_columns))
    with col4:
        st.metric("누락값", data[available_columns].isnull().sum().sum())
    
    # 데이터 테이블
    st.dataframe(data[available_columns].head(10), use_container_width=True)
    
    # 기본 통계 정보
    with st.expander("📊 기본 통계 정보"):
        st.dataframe(data[available_columns].describe(), use_container_width=True)

def perform_linearity_analysis(data, available_columns):
    """선형성 분석 수행"""
    try:
        # 데이터 점 추출
        data_points = extract_data_points(data, available_columns)
        
        # PCA 분석
        pca_results = perform_pca_analysis(data_points)
        
        # 선형성 지표 계산
        linearity_metrics = calculate_linearity_metrics(data_points, pca_results)
        
        # 결과 저장
        st.session_state.analysis_results = {
            'data_points': data_points,
            'pca_results': pca_results,
            'linearity_metrics': linearity_metrics
        }
        
        success_message("선형성 분석이 완료되었습니다. '분석 결과' 탭에서 확인하세요.")
        
    except Exception as e:
        error_handler(f"분석 중 오류가 발생했습니다: {str(e)}")

def extract_data_points(data, available_columns):
    """각 축별 데이터 점 추출"""
    data_points = {}
    
    # 축별로 그룹화
    axes = set([col.split('_')[0] for col in available_columns])
    
    for axis in axes:
        axis_columns = [f"{axis}_x", f"{axis}_y", f"{axis}_z"]
        if all(col in data.columns for col in axis_columns):
            points = data[axis_columns].dropna().values
            if len(points) > 0:
                data_points[axis] = points
    
    return data_points

def perform_pca_analysis(data_points):
    """PCA 분석 수행"""
    pca_results = {}
    
    for axis, points in data_points.items():
        if len(points) >= 2:  # PCA를 위해 최소 2개 점 필요
            pca = PCA(n_components=1)
            pca.fit(points)
            
            pca_results[axis] = {
                'direction_vector': pca.components_[0],
                'point_on_line': pca.mean_,
                'explained_variance_ratio': pca.explained_variance_ratio_[0],
                'singular_values': pca.singular_values_[0]
            }
    
    return pca_results

def calculate_linearity_metrics(data_points, pca_results):
    """선형성 지표 계산"""
    metrics = {
        'linearity': {},  # 진직도
        'parallelism': {},  # 평행도  
        'perpendicularity': {}  # 수직도
    }
    
    # 진직도 계산
    for axis, points in data_points.items():
        if axis in pca_results:
            pca_result = pca_results[axis]
            direction_vector = pca_result['direction_vector']
            point_on_line = pca_result['point_on_line']
            
            # 각 점에서 주성분 직선까지의 거리 계산
            distances = []
            for point in points:
                # 점에서 직선까지의 거리 계산
                proj = point_on_line + np.dot(point - point_on_line, direction_vector) * direction_vector
                distance = np.linalg.norm(point - proj)
                distances.append(distance)
            
            metrics['linearity'][axis] = {
                'mean_distance': np.mean(distances),
                'max_distance': np.max(distances),
                'std_distance': np.std(distances)
            }
    
    # 평행도 및 수직도 계산
    axes = list(pca_results.keys())
    for i in range(len(axes)):
        for j in range(i + 1, len(axes)):
            axis1, axis2 = axes[i], axes[j]
            vector1 = pca_results[axis1]['direction_vector']
            vector2 = pca_results[axis2]['direction_vector']
            
            # 두 벡터 사이의 각도 계산
            dot_product = np.clip(np.dot(vector1, vector2) / 
                                (np.linalg.norm(vector1) * np.linalg.norm(vector2)), -1.0, 1.0)
            angle_deg = np.degrees(np.arccos(np.abs(dot_product)))
            
            # 평행도 (0도에 가까울수록 평행)
            parallelism_score = 90 - min(angle_deg, 180 - angle_deg)
            metrics['parallelism'][f"{axis1}_{axis2}"] = {
                'angle_deg': min(angle_deg, 180 - angle_deg),
                'parallelism_score': parallelism_score
            }
            
            # 수직도 (90도에 가까울수록 수직)
            perpendicularity_score = 90 - abs(90 - angle_deg)
            metrics['perpendicularity'][f"{axis1}_{axis2}"] = {
                'angle_deg': angle_deg,
                'perpendicularity_score': perpendicularity_score
            }
    
    return metrics

def display_method_section():
    """평가 방법 섹션 표시"""
    st.header("📊 평가 방법")
    
    # 수식 설명
    st.subheader("🔬 분석 방법론")
    
    with st.expander("📐 진직도 (Linearity) 평가", expanded=True):
        st.markdown("""
        **진직도**는 데이터 점들이 주성분 직선에 얼마나 가까운지를 나타내는 척도입니다.
        
        **계산 방법:**
        1. PCA를 통해 데이터의 주성분 직선을 찾습니다.
        2. 각 데이터 점에서 주성분 직선까지의 거리를 계산합니다.
        3. 평균 거리를 진직도 값으로 사용합니다.
        
        **수식:**
        """)
        st.latex(r"L = \frac{1}{N} \sum_{i=1}^{N} d_i")
        st.markdown("여기서 $d_i$는 각 데이터 점에서 직선까지의 거리, $N$은 데이터 점의 개수입니다.")
    
    with st.expander("📏 평행도 (Parallelism) 평가"):
        st.markdown("""
        **평행도**는 두 축의 주성분 벡터가 얼마나 평행한지를 평가합니다.
        
        **계산 방법:**
        1. 각 축의 주성분 벡터를 구합니다.
        2. 두 벡터 사이의 각도를 계산합니다.
        3. 0도에 가까울수록 평행성이 높습니다.
        
        **수식:**
        """)
        st.latex(r"\\cos(\\theta) = \\frac{\\vec{a} \\cdot \\vec{b}}{|\\vec{a}| |\\vec{b}|}")
        st.markdown("여기서 $\\vec{a}$와 $\\vec{b}$는 두 주성분 벡터입니다.")
    
    with st.expander("⊥ 수직도 (Perpendicularity) 평가"):
        st.markdown("""
        **수직도**는 두 축의 주성분 벡터가 얼마나 수직한지를 평가합니다.
        
        **계산 방법:**
        1. 각 축의 주성분 벡터를 구합니다.
        2. 두 벡터 사이의 각도를 계산합니다.
        3. 90도에 가까울수록 수직성이 높습니다.
        
        **평가 기준:**
        - 85° ~ 95°: 우수한 수직도
        - 80° ~ 85°, 95° ~ 100°: 양호한 수직도
        - 그 외: 개선 필요
        """)
    
    with st.expander("🔍 PCA 주성분 분석"):
        st.markdown("""
        **PCA (Principal Component Analysis)**는 고차원 데이터를 저차원으로 축소하면서 
        데이터의 분산을 최대화하는 기법입니다.
        
        **계산 과정:**
        1. **데이터 중심화**: 평균을 빼서 원점으로 이동
        2. **공분산 행렬 계산**: 데이터의 분산-공분산 구조 파악
        3. **고유값 분해**: 공분산 행렬의 고유값과 고유벡터 계산
        4. **주성분 선택**: 가장 큰 고유값에 해당하는 고유벡터 선택
        
        **수식:**
        """)
        st.latex(r"C = \\frac{1}{N-1} X_{centered}^T X_{centered}")
        st.latex(r"C \\vec{v} = \\lambda \\vec{v}")
        st.markdown("여기서 $C$는 공분산 행렬, $\\vec{v}$는 고유벡터, $\\lambda$는 고유값입니다.")

def display_result_section():
    """분석 결과 섹션 표시"""
    st.header("📈 분석 결과")
    
    if st.session_state.analysis_results is None:
        info_message("먼저 '데이터 입력' 탭에서 데이터를 업로드하고 분석을 수행하세요.")
        return
    
    results = st.session_state.analysis_results
    
    # 3D 시각화
    display_3d_visualization(results)
    
    # 정량적 결과 표시
    display_quantitative_results(results)
    
    # 분석 리포트
    display_analysis_report(results)

def display_3d_visualization(results):
    """3D 시각화 표시"""
    st.subheader("🎯 3D 시각화")
    
    data_points = results['data_points']
    pca_results = results['pca_results']
    
    fig = go.Figure()
    
    # 색상 정의
    colors = {'X1': 'blue', 'X2': 'green', 'Y': 'orange', 'Z': 'purple'}
    line_colors = {'X1': 'red', 'X2': 'cyan', 'Y': 'yellow', 'Z': 'magenta'}
    
    # 데이터 점 시각화
    for axis, points in data_points.items():
        fig.add_trace(go.Scatter3d(
            x=points[:, 0], y=points[:, 1], z=points[:, 2],
            mode='markers',
            marker=dict(size=5, color=colors.get(axis, 'gray'), opacity=0.7),
            name=f'{axis} 데이터 점'
        ))
    
    # 주성분 직선 시각화
    if pca_results:
        # 전체 데이터 범위 계산
        all_points = np.vstack([points for points in data_points.values()])
        max_range = np.ptp(all_points, axis=0).max()
        max_range = max_range if max_range > 0 else 50
        
        t_vals = np.linspace(-0.5 * max_range, 0.5 * max_range, 100)
        
        for axis, pca_result in pca_results.items():
            point_on_line = pca_result['point_on_line']
            direction_vector = pca_result['direction_vector']
            
            line_points = point_on_line + t_vals[:, np.newaxis] * direction_vector
            
            fig.add_trace(go.Scatter3d(
                x=line_points[:, 0], y=line_points[:, 1], z=line_points[:, 2],
                mode='lines',
                line=dict(color=line_colors.get(axis, 'black'), width=4),
                name=f'{axis} 주성분 직선'
            ))
    
    # 레이아웃 설정
    fig.update_layout(
        scene=dict(
            xaxis_title='X 좌표',
            yaxis_title='Y 좌표',
            zaxis_title='Z 좌표',
            aspectmode='cube'
        ),
        title="3D 데이터 점과 주성분 분석 결과",
        showlegend=True,
        width=800,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_quantitative_results(results):
    """정량적 결과 표시"""
    st.subheader("📊 정량적 분석 결과")
    
    metrics = results['linearity_metrics']
    
    # 진직도 결과
    if metrics['linearity']:
        st.write("**🎯 진직도 (Linearity) 결과**")
        linearity_data = []
        for axis, values in metrics['linearity'].items():
            linearity_data.append({
                '축': axis,
                '평균 거리': f"{values['mean_distance']:.4f}",
                '최대 거리': f"{values['max_distance']:.4f}",
                '표준편차': f"{values['std_distance']:.4f}"
            })
        
        linearity_df = pd.DataFrame(linearity_data)
        st.dataframe(linearity_df, use_container_width=True)
    
    # 평행도 결과
    if metrics['parallelism']:
        st.write("**📏 평행도 (Parallelism) 결과**")
        parallelism_data = []
        for axes, values in metrics['parallelism'].items():
            axis1, axis2 = axes.split('_')
            parallelism_data.append({
                '기준 축': axis1,
                '측정 축': axis2,
                '각도 (도)': f"{values['angle_deg']:.2f}°",
                '평행도 점수': f"{values['parallelism_score']:.1f}/90"
            })
        
        parallelism_df = pd.DataFrame(parallelism_data)
        st.dataframe(parallelism_df, use_container_width=True)
    
    # 수직도 결과
    if metrics['perpendicularity']:
        st.write("**⊥ 수직도 (Perpendicularity) 결과**")
        perpendicularity_data = []
        for axes, values in metrics['perpendicularity'].items():
            axis1, axis2 = axes.split('_')
            perpendicularity_data.append({
                '기준 축': axis1,
                '측정 축': axis2,
                '각도 (도)': f"{values['angle_deg']:.2f}°",
                '수직도 점수': f"{values['perpendicularity_score']:.1f}/90"
            })
        
        perpendicularity_df = pd.DataFrame(perpendicularity_data)
        st.dataframe(perpendicularity_df, use_container_width=True)

def display_analysis_report(results):
    """분석 리포트 표시"""
    st.subheader("📋 분석 리포트")
    
    metrics = results['linearity_metrics']
    
    # 종합 평가
    st.write("**🎯 종합 평가**")
    
    # 진직도 평가
    if metrics['linearity']:
        best_linearity = min(metrics['linearity'].items(), 
                           key=lambda x: x[1]['mean_distance'])
        st.success(f"가장 우수한 진직도: {best_linearity[0]}축 "
                  f"(평균 거리: {best_linearity[1]['mean_distance']:.4f})")
    
    # 평행도 평가
    if metrics['parallelism']:
        best_parallelism = max(metrics['parallelism'].items(),
                             key=lambda x: x[1]['parallelism_score'])
        st.info(f"가장 우수한 평행도: {best_parallelism[0]} "
               f"(점수: {best_parallelism[1]['parallelism_score']:.1f}/90)")
    
    # 수직도 평가
    if metrics['perpendicularity']:
        best_perpendicularity = max(metrics['perpendicularity'].items(),
                                  key=lambda x: x[1]['perpendicularity_score'])
        st.info(f"가장 우수한 수직도: {best_perpendicularity[0]} "
               f"(점수: {best_perpendicularity[1]['perpendicularity_score']:.1f}/90)")
    
    # 개선 권장사항
    st.write("**💡 개선 권장사항**")
    recommendations = generate_recommendations(metrics)
    for rec in recommendations:
        st.write(f"• {rec}")

def generate_recommendations(metrics):
    """개선 권장사항 생성"""
    recommendations = []
    
    # 진직도 기반 권장사항
    if metrics['linearity']:
        poor_linearity = [axis for axis, values in metrics['linearity'].items()
                         if values['mean_distance'] > 0.1]
        if poor_linearity:
            recommendations.append(f"{', '.join(poor_linearity)}축의 진직도 개선이 필요합니다.")
    
    # 평행도 기반 권장사항
    if metrics['parallelism']:
        poor_parallelism = [axes for axes, values in metrics['parallelism'].items()
                          if values['parallelism_score'] < 60]
        if poor_parallelism:
            recommendations.append(f"{', '.join(poor_parallelism)} 축들의 평행도 조정이 필요합니다.")
    
    # 수직도 기반 권장사항
    if metrics['perpendicularity']:
        poor_perpendicularity = [axes for axes, values in metrics['perpendicularity'].items()
                               if values['perpendicularity_score'] < 60]
        if poor_perpendicularity:
            recommendations.append(f"{', '.join(poor_perpendicularity)} 축들의 수직도 조정이 필요합니다.")
    
    if not recommendations:
        recommendations.append("모든 지표가 양호한 수준입니다. 현재 상태를 유지하세요.")
    
    return recommendations

def display_data_format_guide():
    """데이터 형식 가이드 표시"""
    st.subheader("📋 데이터 형식 안내")
    
    st.markdown("""
    **필요한 데이터 형식:**
    
    엑셀 파일에는 다음과 같은 컬럼이 포함되어야 합니다:
    
    | 컬럼명 | 설명 | 예시 |
    |--------|------|------|
    | X1_x, X1_y, X1_z | X1축의 3D 좌표 | 10.1, 20.2, 30.3 |
    | X2_x, X2_y, X2_z | X2축의 3D 좌표 | 11.1, 21.2, 31.3 |
    | Y_x, Y_y, Y_z | Y축의 3D 좌표 | 12.1, 22.2, 32.3 |
    | Z_x, Z_y, Z_z | Z축의 3D 좌표 | 13.1, 23.2, 33.3 |
    
    **참고사항:**
    - 모든 축의 데이터가 필요하지 않습니다. 분석하고자 하는 축만 포함하면 됩니다.
    - 최소 하나의 축에 대한 3D 좌표 데이터가 필요합니다.
    - 각 축마다 최소 2개 이상의 데이터 점이 있어야 합니다.
    """)

def create_template_download():
    """템플릿 다운로드 생성"""
    # 샘플 데이터 생성
    np.random.seed(42)
    n_points = 20
    
    template_data = {
        'X1_x': np.random.normal(0, 1, n_points),
        'X1_y': np.random.normal(0, 0.1, n_points),
        'X1_z': np.random.normal(0, 0.1, n_points),
        'X2_x': np.random.normal(0, 0.1, n_points),
        'X2_y': np.random.normal(0, 1, n_points),
        'X2_z': np.random.normal(0, 0.1, n_points),
        'Y_x': np.random.normal(0, 0.1, n_points),
        'Y_y': np.random.normal(0, 0.1, n_points),
        'Y_z': np.random.normal(0, 1, n_points),
        'Z_x': np.random.normal(0, 0.1, n_points),
        'Z_y': np.random.normal(0, 0.1, n_points),
        'Z_z': np.random.normal(0, 0.1, n_points)
    }
    
    template_df = pd.DataFrame(template_data)
    
    # Excel 파일로 변환
    from io import BytesIO
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        template_df.to_excel(writer, index=False, sheet_name='Linearity Data')
    
    buffer.seek(0)
    
    st.download_button(
        label="📥 템플릿 다운로드",
        data=buffer,
        file_name='linearity_analysis_template.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        help="선형성 분석을 위한 데이터 템플릿을 다운로드합니다."
    )

# 메인 실행
if __name__ == "__main__":
    linearity_analysis()
