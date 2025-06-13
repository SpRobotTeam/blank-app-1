import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Tuple, Dict, List
from io import BytesIO

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, error_handler, success_message, info_message, sidebar_info
from utils.data_processing import safe_operation, create_download_link

@safe_operation
def motor_calc():
    """
    고급 로봇 그리퍼 모터 토크 계산기
    다양한 계산 모드와 시각화, 분석 기능을 제공하는 종합 모터 계산 도구입니다.
    """
    # 도구 헤더 적용
    tool_header(
        "고급 로봇 그리퍼 모터 토크 계산기", 
        "로봇 그리퍼의 모터 토크를 정밀하게 계산하고 분석합니다. 단일 계산, 배치 분석, 최적화, 그리고 시각화 기능을 제공합니다."
    )

    # 사이드바에 정보 표시
    with st.sidebar:
        sidebar_info(version="2.0", update_date="2025-06-10")
        
        st.markdown("### 🔧 계산 모드")
        calc_mode = st.radio(
            "모드 선택:",
            ["단일 계산", "배치 분석", "매개변수 최적화", "비교 분석"],
            help="다양한 계산 모드를 선택할 수 있습니다."
        )
        
        st.markdown("### ⚙️ 고급 설정")
        include_safety_factor = st.checkbox("안전 계수 적용", value=True)
        safety_factor = st.slider("안전 계수", 1.0, 5.0, 2.0, 0.1) if include_safety_factor else 1.0
        
        include_efficiency = st.checkbox("효율성 고려", value=True)
        efficiency = st.slider("시스템 효율성", 0.5, 1.0, 0.85, 0.05) if include_efficiency else 1.0

    # 탭 구성
    if calc_mode == "단일 계산":
        display_single_calculation(safety_factor, efficiency)
    elif calc_mode == "배치 분석":
        display_batch_analysis(safety_factor, efficiency)
    elif calc_mode == "매개변수 최적화":
        display_parameter_optimization(safety_factor, efficiency)
    elif calc_mode == "비교 분석":
        display_comparison_analysis(safety_factor, efficiency)

def display_single_calculation(safety_factor, efficiency):
    """단일 계산 모드"""
    st.header("🔢 단일 계산 모드")
    
    # 입력 탭과 결과 탭
    input_tab, result_tab, analysis_tab = st.tabs(["📝 입력", "📊 결과", "📈 분석"])
    
    with input_tab:
        display_input_parameters()
    
    with result_tab:
        if 'motor_inputs' in st.session_state:
            results = calculate_gripper_forces_advanced(
                st.session_state.motor_inputs, safety_factor, efficiency
            )
            display_calculation_results(results)
            display_force_diagram(st.session_state.motor_inputs, results)
    
    with analysis_tab:
        if 'motor_inputs' in st.session_state:
            display_sensitivity_analysis(st.session_state.motor_inputs, safety_factor, efficiency)

def display_input_parameters():
    """입력 매개변수 섹션"""
    st.subheader("🔧 그리퍼 사양 입력")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📦 워크피스 정보**")
        W = st.number_input(
            "워크피스 무게 (kg)", 
            value=112.0, step=0.1, min_value=0.1,
            help="잡을 물체의 무게를 입력하세요."
        )
        
        material_type = st.selectbox(
            "재질 타입",
            ["Steel", "Aluminum", "Plastic", "Ceramic", "Other"],
            help="재질에 따라 마찰 계수가 달라집니다."
        )
        
        friction_coeff = get_friction_coefficient(material_type)
        st.write(f"마찰 계수: {friction_coeff}")
        
        theta_deg = st.number_input(
            "핑거 각도 (도)", 
            value=11.0, step=0.1, min_value=0.1, max_value=89.9,
            help="그리퍼 핑거의 경사각을 입력하세요."
        )
    
    with col2:
        st.markdown("**📐 기구학적 매개변수**")
        L_pivot = st.number_input(
            "핑거 회전 중심 거리 (mm)", 
            value=173.13, step=0.1, min_value=1.0,
            help="핑거 회전축으로부터의 거리입니다."
        )
        
        L_100mm = st.number_input(
            "작동 지점 거리 (mm)", 
            value=100.0, step=0.1, min_value=1.0,
            help="힘이 작용하는 지점까지의 거리입니다."
        )
        
        R_g = st.number_input(
            "감속비", 
            value=40, step=1, min_value=1,
            help="모터와 출력축 사이의 감속비입니다."
        )
        
        grip_force_req = st.number_input(
            "요구 그립력 (N)",
            value=500.0, step=10.0, min_value=0.0,
            help="안전한 파지를 위해 필요한 최소 그립력입니다."
        )
    
    # 고급 매개변수
    with st.expander("🔬 고급 매개변수"):
        col1, col2 = st.columns(2)
        
        with col1:
            operating_temp = st.slider("동작 온도 (°C)", -20, 100, 25)
            max_speed = st.number_input("최대 동작 속도 (rpm)", value=100.0, min_value=1.0)
            
        with col2:
            backlash = st.number_input("백래시 (도)", value=0.5, min_value=0.0)
            stiffness = st.number_input("시스템 강성 (Nm/rad)", value=1000.0, min_value=1.0)
    
    # 입력값 저장
    st.session_state.motor_inputs = {
        'W': W,
        'theta_deg': theta_deg,
        'L_pivot': L_pivot,
        'L_100mm': L_100mm,
        'R_g': R_g,
        'grip_force_req': grip_force_req,
        'friction_coeff': friction_coeff,
        'material_type': material_type,
        'operating_temp': operating_temp,
        'max_speed': max_speed,
        'backlash': backlash,
        'stiffness': stiffness
    }
    
    if st.button("🔄 계산 실행", type="primary"):
        success_message("계산이 완료되었습니다. '결과' 탭에서 확인하세요.")

def get_friction_coefficient(material_type):
    """재질별 마찰 계수 반환"""
    friction_coeffs = {
        'Steel': 0.6,
        'Aluminum': 0.4,
        'Plastic': 0.3,
        'Ceramic': 0.8,
        'Other': 0.5
    }
    return friction_coeffs.get(material_type, 0.5)

def calculate_gripper_forces_advanced(inputs: Dict, safety_factor: float, efficiency: float) -> Dict:
    """고급 그리퍼 힘 계산"""
    # 기본 변수
    W = inputs['W']
    theta_deg = inputs['theta_deg']
    L_pivot = inputs['L_pivot']
    L_100mm = inputs['L_100mm']
    R_g = inputs['R_g']
    grip_force_req = inputs['grip_force_req']
    friction_coeff = inputs['friction_coeff']
    
    # 단위 변환
    theta_rad = math.radians(theta_deg)
    L_pivot_m = L_pivot / 1000
    L_100mm_m = L_100mm / 1000
    g = 9.81
    
    # 기본 계산
    weight_force = W * g
    F_push = math.tan(theta_rad) * weight_force
    T_finger_pivot = F_push * L_pivot_m
    F_100mm = T_finger_pivot / L_100mm_m
    T_gear_output = F_100mm * L_100mm_m
    T_motor_basic = T_gear_output / R_g
    
    # 안전 계수 및 효율성 적용
    T_motor_safe = T_motor_basic * safety_factor / efficiency
    
    # 추가 계산
    normal_force = weight_force / math.cos(theta_rad)
    max_grip_force = normal_force * friction_coeff
    grip_safety_margin = max_grip_force / grip_force_req if grip_force_req > 0 else float('inf')
    
    # 동력 계산
    max_power = T_motor_safe * (inputs['max_speed'] * 2 * math.pi / 60)  # Watts
    
    # 온도 보정 (간단한 모델)
    temp_factor = 1 - (inputs['operating_temp'] - 25) * 0.001
    T_motor_corrected = T_motor_safe * temp_factor
    
    return {
        'weight_force': weight_force,
        'F_push': F_push,
        'T_finger_pivot': T_finger_pivot,
        'F_100mm': F_100mm,
        'T_gear_output': T_gear_output,
        'T_motor_basic': T_motor_basic,
        'T_motor_safe': T_motor_safe,
        'T_motor_corrected': T_motor_corrected,
        'normal_force': normal_force,
        'max_grip_force': max_grip_force,
        'grip_safety_margin': grip_safety_margin,
        'max_power': max_power,
        'safety_factor': safety_factor,
        'efficiency': efficiency
    }

def display_calculation_results(results: Dict):
    """계산 결과 표시"""
    st.subheader("📊 계산 결과")
    
    # 주요 결과
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "최종 모터 토크", 
            f"{results['T_motor_corrected']:.3f} Nm",
            help="온도 보정 및 안전계수가 적용된 최종 모터 토크"
        )
        
        st.metric(
            "최대 그립력", 
            f"{results['max_grip_force']:.1f} N",
            help="마찰을 고려한 최대 가능 그립력"
        )
    
    with col2:
        st.metric(
            "감속기 출력 토크", 
            f"{results['T_gear_output']:.3f} Nm",
            help="감속기에서 출력되는 토크"
        )
        
        st.metric(
            "최대 소비 전력", 
            f"{results['max_power']:.1f} W",
            help="최대 속도에서의 소비 전력"
        )
    
    with col3:
        st.metric(
            "그립 안전 여유", 
            f"{results['grip_safety_margin']:.2f}",
            help="요구 그립력 대비 안전 여유도"
        )
        
        color = "green" if results['grip_safety_margin'] > 2 else "orange" if results['grip_safety_margin'] > 1.5 else "red"
        safety_status = "안전" if results['grip_safety_margin'] > 2 else "주의" if results['grip_safety_margin'] > 1.5 else "위험"
        st.markdown(f"**안전성 평가:** :{color}[{safety_status}]")
    
    # 상세 결과 테이블
    st.subheader("📋 상세 계산 결과")
    
    detailed_results = {
        '계산 항목': [
            '물체 중량력 (N)',
            '핑거 밀어내는 힘 (N)',
            '핑거 회전축 토크 (Nm)',
            '100mm 지점 힘 (N)',
            '기본 모터 토크 (Nm)',
            '안전계수 적용 토크 (Nm)',
            '온도 보정 토크 (Nm)',
            '법선력 (N)',
            '최대 전력 (W)'
        ],
        '계산값': [
            f"{results['weight_force']:.2f}",
            f"{results['F_push']:.2f}",
            f"{results['T_finger_pivot']:.4f}",
            f"{results['F_100mm']:.2f}",
            f"{results['T_motor_basic']:.4f}",
            f"{results['T_motor_safe']:.4f}",
            f"{results['T_motor_corrected']:.4f}",
            f"{results['normal_force']:.2f}",
            f"{results['max_power']:.1f}"
        ],
        '단위': [
            'N', 'N', 'Nm', 'N', 'Nm', 'Nm', 'Nm', 'N', 'W'
        ]
    }
    
    results_df = pd.DataFrame(detailed_results)
    st.dataframe(results_df, use_container_width=True)
    
    # 수식 설명
    with st.expander("📐 계산 수식 및 설명"):
        st.markdown("""
        ### 🔢 기본 계산 수식
        
        1. **물체 중량력**: $F_w = W \cdot g$
        2. **핑거 밀어내는 힘**: $F_{push} = \tan(\theta) \cdot F_w$
        3. **핑거 회전축 토크**: $T_{pivot} = F_{push} \cdot L_{pivot}$
        4. **100mm 지점 힘**: $F_{100} = T_{pivot} / L_{100}$
        5. **감속기 출력 토크**: $T_{gear} = F_{100} \cdot L_{100}$
        6. **기본 모터 토크**: $T_{motor} = T_{gear} / R_g$
        
        ### ⚡ 보정 및 안전 계수
        
        - **안전계수 적용**: $T_{safe} = T_{motor} \cdot S_f / \eta$
        - **온도 보정**: $T_{final} = T_{safe} \cdot (1 - (T - 25) \cdot 0.001)$
        - **최대 그립력**: $F_{grip} = F_w \cdot \mu / \cos(\theta)$
        
        ### 📊 설계 고려사항
        
        - 안전 여유도는 2.0 이상 권장
        - 온도가 높을수록 모터 성능 저하
        - 마찰계수는 재질과 표면 조건에 따라 변함
        """)

def display_force_diagram(inputs: Dict, results: Dict):
    """힘 다이어그램 표시"""
    st.subheader("📐 힘 분석 다이어그램")
    
    # 힘 벡터 다이어그램
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('힘 분포', '토크 분포', '안전성 분석', '효율성 분석'),
        specs=[[{'type': 'scatter'}, {'type': 'bar'}],
               [{'type': 'scatter'}, {'type': 'bar'}]]
    )
    
    # 힘 분포 (극좌표)
    theta_rad = math.radians(inputs['theta_deg'])
    angles = [0, theta_rad, theta_rad + math.pi/2, math.pi]
    forces = [results['weight_force'], results['F_push'], results['normal_force'], 0]
    force_names = ['Weight', 'Push', 'Normal', 'Reference']
    
    fig.add_trace(
        go.Scatterpolar(
            r=forces,
            theta=[math.degrees(a) for a in angles],
            mode='markers+lines',
            name='Forces',
            marker=dict(size=10)
        ),
        row=1, col=1
    )
    
    # 토크 분포
    torque_names = ['Finger Pivot', 'Gear Output', 'Motor Required', 'Motor Safe']
    torque_values = [
        results['T_finger_pivot'],
        results['T_gear_output'], 
        results['T_motor_basic'],
        results['T_motor_safe']
    ]
    
    fig.add_trace(
        go.Bar(
            x=torque_names,
            y=torque_values,
            name='Torques',
            marker_color='lightblue'
        ),
        row=1, col=2
    )
    
    # 안전성 분석 (방사형 차트)
    safety_categories = ['Grip Safety', 'Torque Margin', 'Power Margin', 'Temperature']
    safety_scores = [
        min(100, results['grip_safety_margin'] * 30),
        min(100, (results['T_motor_safe'] / results['T_motor_basic'] - 1) * 100),
        min(100, 100 - results['max_power'] / 1000 * 100),
        min(100, 100 - abs(inputs['operating_temp'] - 25))
    ]
    
    fig.add_trace(
        go.Scatterpolar(
            r=safety_scores,
            theta=safety_categories,
            fill='toself',
            name='Safety Analysis'
        ),
        row=2, col=1
    )
    
    # 효율성 분석
    efficiency_factors = ['System Eff.', 'Friction Loss', 'Backlash', 'Stiffness']
    efficiency_values = [
        results['efficiency'] * 100,
        (1 - inputs['friction_coeff']) * 100,
        100 - inputs['backlash'] * 10,
        min(100, inputs['stiffness'] / 50)
    ]
    
    fig.add_trace(
        go.Bar(
            x=efficiency_factors,
            y=efficiency_values,
            name='Efficiency',
            marker_color='lightgreen'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=700, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

def display_sensitivity_analysis(inputs: Dict, safety_factor: float, efficiency: float):
    """민감도 분석"""
    st.subheader("📈 민감도 분석")
    
    # 매개변수 변화에 따른 토크 변화 분석
    param_ranges = {
        'theta_deg': np.linspace(5, 25, 20),
        'L_pivot': np.linspace(100, 250, 20),
        'R_g': np.linspace(20, 80, 20),
        'W': np.linspace(50, 200, 20)
    }
    
    sensitivity_results = {}
    
    for param, values in param_ranges.items():
        torques = []
        for value in values:
            test_inputs = inputs.copy()
            test_inputs[param] = value
            
            try:
                results = calculate_gripper_forces_advanced(test_inputs, safety_factor, efficiency)
                torques.append(results['T_motor_corrected'])
            except:
                torques.append(0)
        
        sensitivity_results[param] = (values, torques)
    
    # 시각화
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('핑거 각도 vs 토크', '피벗 거리 vs 토크', '감속비 vs 토크', '무게 vs 토크')
    )
    
    positions = [(1,1), (1,2), (2,1), (2,2)]
    param_labels = {
        'theta_deg': ('핑거 각도 (도)', '토크 (Nm)'),
        'L_pivot': ('피벗 거리 (mm)', '토크 (Nm)'),
        'R_g': ('감속비', '토크 (Nm)'),
        'W': ('무게 (kg)', '토크 (Nm)')
    }
    
    for i, (param, (values, torques)) in enumerate(sensitivity_results.items()):
        row, col = positions[i]
        xlabel, ylabel = param_labels[param]
        
        fig.add_trace(
            go.Scatter(
                x=values,
                y=torques,
                mode='lines+markers',
                name=param,
                line=dict(width=3)
            ),
            row=row, col=col
        )
        
        # 현재 값 표시
        current_value = inputs[param]
        current_torque = next((t for v, t in zip(values, torques) if abs(v - current_value) < (values[1] - values[0])), None)
        
        if current_torque:
            fig.add_trace(
                go.Scatter(
                    x=[current_value],
                    y=[current_torque],
                    mode='markers',
                    marker=dict(size=12, color='red', symbol='star'),
                    name=f'Current {param}',
                    showlegend=False
                ),
                row=row, col=col
            )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # 민감도 순위
    st.subheader("📊 매개변수 민감도 순위")
    
    sensitivities = {}
    for param, (values, torques) in sensitivity_results.items():
        # 정규화된 민감도 계산
        torque_range = max(torques) - min(torques)
        value_range = max(values) - min(values)
        normalized_sensitivity = (torque_range / np.mean(torques)) / (value_range / np.mean(values))
        sensitivities[param] = normalized_sensitivity
    
    sensitivity_df = pd.DataFrame([
        {'매개변수': param, '민감도 지수': sens, '영향도': '높음' if sens > 1 else '보통' if sens > 0.5 else '낮음'}
        for param, sens in sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)
    ])
    
    st.dataframe(sensitivity_df, use_container_width=True)

def display_batch_analysis(safety_factor: float, efficiency: float):
    """배치 분석 모드"""
    st.header("📊 배치 분석 모드")
    
    st.markdown("여러 설계 조건을 한 번에 분석하여 최적의 설계를 찾을 수 있습니다.")
    
    # 배치 입력 방법 선택
    input_method = st.radio(
        "입력 방법 선택:",
        ["수동 입력", "CSV 파일 업로드", "매개변수 범위 설정"]
    )
    
    if input_method == "수동 입력":
        display_manual_batch_input(safety_factor, efficiency)
    elif input_method == "CSV 파일 업로드":
        display_csv_batch_input(safety_factor, efficiency)
    elif input_method == "매개변수 범위 설정":
        display_range_batch_input(safety_factor, efficiency)

def display_manual_batch_input(safety_factor: float, efficiency: float):
    """수동 배치 입력"""
    st.subheader("✏️ 수동 배치 입력")
    
    # 배치 데이터 입력을 위한 테이블 형태 인터페이스
    if 'batch_data' not in st.session_state:
        st.session_state.batch_data = pd.DataFrame({
            'Case': [f'Case {i+1}' for i in range(3)],
            'Weight (kg)': [100.0, 150.0, 200.0],
            'Angle (deg)': [10.0, 15.0, 20.0],
            'Pivot Distance (mm)': [170.0, 180.0, 190.0],
            'Action Distance (mm)': [100.0, 120.0, 140.0],
            'Gear Ratio': [40, 50, 60]
        })
    
    # 데이터 편집
    edited_data = st.data_editor(
        st.session_state.batch_data,
        num_rows="dynamic",
        use_container_width=True
    )
    
    if st.button("🔄 배치 계산 실행"):
        results = perform_batch_calculation(edited_data, safety_factor, efficiency)
        display_batch_results(results)

def display_csv_batch_input(safety_factor: float, efficiency: float):
    """CSV 배치 입력"""
    st.subheader("📁 CSV 파일 업로드")
    
    # 템플릿 다운로드
    template_data = {
        'Case': [f'Case {i+1}' for i in range(3)],
        'Weight (kg)': [100.0, 150.0, 200.0],
        'Angle (deg)': [10.0, 15.0, 20.0],
        'Pivot Distance (mm)': [170.0, 180.0, 190.0],
        'Action Distance (mm)': [100.0, 120.0, 140.0],
        'Gear Ratio': [40, 50, 60]
    }
    
    template_df = pd.DataFrame(template_data)
    csv_template = template_df.to_csv(index=False)
    
    st.download_button(
        label="📥 CSV 템플릿 다운로드",
        data=csv_template,
        file_name="motor_calc_template.csv",
        mime="text/csv"
    )
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "CSV 파일 업로드",
        type=['csv'],
        help="템플릿과 동일한 형식의 CSV 파일을 업로드하세요."
    )
    
    if uploaded_file:
        try:
            batch_data = pd.read_csv(uploaded_file)
            st.dataframe(batch_data, use_container_width=True)
            
            if st.button("🔄 CSV 배치 계산 실행"):
                results = perform_batch_calculation(batch_data, safety_factor, efficiency)
                display_batch_results(results)
                
        except Exception as e:
            error_handler(f"CSV 파일 읽기 오류: {str(e)}")

def display_range_batch_input(safety_factor: float, efficiency: float):
    """범위 배치 입력"""
    st.subheader("📏 매개변수 범위 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**무게 범위 (kg)**")
        weight_min = st.number_input("최소 무게", value=50.0, min_value=0.1)
        weight_max = st.number_input("최대 무게", value=200.0, min_value=weight_min)
        weight_steps = st.slider("무게 스텝 수", 3, 20, 10)
        
        st.markdown("**각도 범위 (도)**")
        angle_min = st.number_input("최소 각도", value=5.0, min_value=0.1)
        angle_max = st.number_input("최대 각도", value=25.0, min_value=angle_min)
        angle_steps = st.slider("각도 스텝 수", 3, 20, 10)
    
    with col2:
        st.markdown("**피벗 거리 범위 (mm)**")
        pivot_min = st.number_input("최소 피벗 거리", value=150.0, min_value=1.0)
        pivot_max = st.number_input("최대 피벗 거리", value=200.0, min_value=pivot_min)
        
        st.markdown("**감속비 범위**")
        gear_min = st.number_input("최소 감속비", value=20, min_value=1)
        gear_max = st.number_input("최대 감속비", value=80, min_value=gear_min)
    
    if st.button("🎯 범위 기반 배치 계산"):
        # 매개변수 조합 생성
        weights = np.linspace(weight_min, weight_max, weight_steps)
        angles = np.linspace(angle_min, angle_max, angle_steps)
        
        batch_data = []
        case_num = 1
        
        for weight in weights:
            for angle in angles:
                batch_data.append({
                    'Case': f'Case {case_num}',
                    'Weight (kg)': weight,
                    'Angle (deg)': angle,
                    'Pivot Distance (mm)': (pivot_min + pivot_max) / 2,
                    'Action Distance (mm)': 100.0,
                    'Gear Ratio': int((gear_min + gear_max) / 2)
                })
                case_num += 1
        
        batch_df = pd.DataFrame(batch_data)
        results = perform_batch_calculation(batch_df, safety_factor, efficiency)
        display_batch_results(results)

def perform_batch_calculation(batch_data: pd.DataFrame, safety_factor: float, efficiency: float) -> pd.DataFrame:
    """배치 계산 수행"""
    results = []
    
    for _, row in batch_data.iterrows():
        inputs = {
            'W': row['Weight (kg)'],
            'theta_deg': row['Angle (deg)'],
            'L_pivot': row['Pivot Distance (mm)'],
            'L_100mm': row['Action Distance (mm)'],
            'R_g': int(row['Gear Ratio']),
            'grip_force_req': 500.0,
            'friction_coeff': 0.5,
            'material_type': 'Steel',
            'operating_temp': 25,
            'max_speed': 100.0,
            'backlash': 0.5,
            'stiffness': 1000.0
        }
        
        try:
            calc_results = calculate_gripper_forces_advanced(inputs, safety_factor, efficiency)
            
            results.append({
                'Case': row['Case'],
                'Weight (kg)': row['Weight (kg)'],
                'Angle (deg)': row['Angle (deg)'],
                'Motor Torque (Nm)': calc_results['T_motor_corrected'],
                'Grip Force (N)': calc_results['max_grip_force'],
                'Safety Margin': calc_results['grip_safety_margin'],
                'Power (W)': calc_results['max_power'],
                'Status': 'Safe' if calc_results['grip_safety_margin'] > 1.5 else 'Warning'
            })
        except Exception as e:
            results.append({
                'Case': row['Case'],
                'Weight (kg)': row['Weight (kg)'],
                'Angle (deg)': row['Angle (deg)'],
                'Motor Torque (Nm)': 'Error',
                'Grip Force (N)': 'Error',
                'Safety Margin': 'Error',
                'Power (W)': 'Error',
                'Status': 'Error'
            })
    
    return pd.DataFrame(results)

def display_batch_results(results: pd.DataFrame):
    """배치 결과 표시"""
    st.subheader("📊 배치 계산 결과")
    
    # 결과 테이블
    st.dataframe(results, use_container_width=True)
    
    # 결과 시각화
    if len(results) > 0 and 'Motor Torque (Nm)' in results.columns:
        # 숫자 데이터만 필터링
        numeric_results = results[results['Motor Torque (Nm)'] != 'Error'].copy()
        
        if len(numeric_results) > 0:
            # 토크 분포
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('모터 토크 분포', '안전 여유도 분포', '무게 vs 토크', '각도 vs 토크')
            )
            
            # 토크 히스토그램
            fig.add_trace(
                go.Histogram(
                    x=numeric_results['Motor Torque (Nm)'].astype(float),
                    name='Motor Torque',
                    nbinsx=20
                ),
                row=1, col=1
            )
            
            # 안전 여유도 히스토그램
            fig.add_trace(
                go.Histogram(
                    x=numeric_results['Safety Margin'].astype(float),
                    name='Safety Margin',
                    nbinsx=20
                ),
                row=1, col=2
            )
            
            # 무게 vs 토크 산점도
            fig.add_trace(
                go.Scatter(
                    x=numeric_results['Weight (kg)'],
                    y=numeric_results['Motor Torque (Nm)'].astype(float),
                    mode='markers',
                    name='Weight vs Torque',
                    marker=dict(
                        size=8,
                        color=numeric_results['Safety Margin'].astype(float),
                        colorscale='RdYlGn',
                        showscale=True
                    )
                ),
                row=2, col=1
            )
            
            # 각도 vs 토크 산점도
            fig.add_trace(
                go.Scatter(
                    x=numeric_results['Angle (deg)'],
                    y=numeric_results['Motor Torque (Nm)'].astype(float),
                    mode='markers',
                    name='Angle vs Torque',
                    marker=dict(size=8, color='blue')
                ),
                row=2, col=2
            )
            
            fig.update_layout(height=700, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # 최적 설계 추천
            st.subheader("🎯 최적 설계 추천")
            
            # 안전 여유도가 충분하면서 토크가 가장 낮은 설계 찾기
            safe_designs = numeric_results[numeric_results['Safety Margin'].astype(float) > 1.5]
            
            if len(safe_designs) > 0:
                optimal_design = safe_designs.loc[safe_designs['Motor Torque (Nm)'].astype(float).idxmin()]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🏆 추천 설계**")
                    st.write(f"케이스: {optimal_design['Case']}")
                    st.write(f"무게: {optimal_design['Weight (kg)']} kg")
                    st.write(f"각도: {optimal_design['Angle (deg)']} 도")
                    st.write(f"모터 토크: {optimal_design['Motor Torque (Nm)']} Nm")
                    st.write(f"안전 여유도: {optimal_design['Safety Margin']}")
                
                with col2:
                    st.markdown("**📈 성능 지표**")
                    torque_percentile = (numeric_results['Motor Torque (Nm)'].astype(float) < float(optimal_design['Motor Torque (Nm)'])).mean() * 100
                    safety_percentile = (numeric_results['Safety Margin'].astype(float) < float(optimal_design['Safety Margin'])).mean() * 100
                    
                    st.write(f"토크 순위: 하위 {torque_percentile:.1f}%")
                    st.write(f"안전성 순위: 상위 {100-safety_percentile:.1f}%")
            else:
                st.warning("안전 여유도를 만족하는 설계가 없습니다. 매개변수를 조정해보세요.")
    
    # 결과 다운로드
    csv = results.to_csv(index=False)
    st.download_button(
        label="📥 배치 결과 다운로드",
        data=csv,
        file_name="batch_motor_calc_results.csv",
        mime="text/csv"
    )

def display_parameter_optimization(safety_factor: float, efficiency: float):
    """매개변수 최적화 모드"""
    st.header("🎯 매개변수 최적화 모드")
    
    st.markdown("목표 성능을 달성하기 위한 최적의 매개변수를 찾습니다.")
    
    # 최적화 목표 설정
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 최적화 목표")
        
        optimization_target = st.selectbox(
            "최적화 목표",
            ["최소 토크", "최대 안전 여유도", "최소 전력", "균형 최적화"]
        )
        
        target_weight = st.number_input("목표 무게 (kg)", value=100.0, min_value=0.1)
        target_grip_force = st.number_input("목표 그립력 (N)", value=500.0, min_value=1.0)
        max_torque_limit = st.number_input("최대 토크 제한 (Nm)", value=10.0, min_value=0.1)
    
    with col2:
        st.subheader("📏 최적화 범위")
        
        angle_range = st.slider("각도 범위 (도)", 5.0, 30.0, (8.0, 20.0))
        pivot_range = st.slider("피벗 거리 범위 (mm)", 100.0, 300.0, (150.0, 200.0))
        gear_range = st.slider("감속비 범위", 10, 100, (30, 60))
        action_distance = st.number_input("작동 거리 (mm)", value=100.0, min_value=1.0)
    
    if st.button("🚀 최적화 실행"):
        optimal_result = perform_optimization(
            optimization_target, target_weight, target_grip_force, max_torque_limit,
            angle_range, pivot_range, gear_range, action_distance,
            safety_factor, efficiency
        )
        
        display_optimization_results(optimal_result)

def perform_optimization(target, weight, grip_force, max_torque, angle_range, pivot_range, 
                        gear_range, action_distance, safety_factor, efficiency):
    """최적화 수행 (간단한 그리드 서치)"""
    best_result = None
    best_score = float('inf') if target == "최소 토크" else -float('inf')
    
    # 그리드 서치
    angles = np.linspace(angle_range[0], angle_range[1], 20)
    pivots = np.linspace(pivot_range[0], pivot_range[1], 20)
    gears = range(gear_range[0], gear_range[1] + 1, 5)
    
    results = []
    
    for angle in angles:
        for pivot in pivots:
            for gear in gears:
                inputs = {
                    'W': weight,
                    'theta_deg': angle,
                    'L_pivot': pivot,
                    'L_100mm': action_distance,
                    'R_g': gear,
                    'grip_force_req': grip_force,
                    'friction_coeff': 0.5,
                    'material_type': 'Steel',
                    'operating_temp': 25,
                    'max_speed': 100.0,
                    'backlash': 0.5,
                    'stiffness': 1000.0
                }
                
                try:
                    calc_results = calculate_gripper_forces_advanced(inputs, safety_factor, efficiency)
                    
                    # 제약 조건 확인
                    if (calc_results['T_motor_corrected'] <= max_torque and
                        calc_results['grip_safety_margin'] > 1.2 and
                        calc_results['max_grip_force'] >= grip_force):
                        
                        # 목표 함수 계산
                        if target == "최소 토크":
                            score = calc_results['T_motor_corrected']
                            is_better = score < best_score
                        elif target == "최대 안전 여유도":
                            score = calc_results['grip_safety_margin']
                            is_better = score > best_score
                        elif target == "최소 전력":
                            score = calc_results['max_power']
                            is_better = score < best_score
                        else:  # 균형 최적화
                            score = (calc_results['T_motor_corrected'] / max_torque +
                                   1 / calc_results['grip_safety_margin'] +
                                   calc_results['max_power'] / 1000)
                            is_better = score < best_score
                        
                        if is_better:
                            best_score = score
                            best_result = {
                                'inputs': inputs,
                                'results': calc_results,
                                'score': score
                            }
                        
                        results.append({
                            'angle': angle,
                            'pivot': pivot,
                            'gear': gear,
                            'torque': calc_results['T_motor_corrected'],
                            'safety': calc_results['grip_safety_margin'],
                            'power': calc_results['max_power'],
                            'score': score
                        })
                
                except:
                    continue
    
    return {
        'best': best_result,
        'all_results': results,
        'target': target
    }

def display_optimization_results(optimal_result):
    """최적화 결과 표시"""
    if optimal_result['best'] is None:
        st.error("최적화 조건을 만족하는 해를 찾지 못했습니다. 제약 조건을 완화해보세요.")
        return
    
    st.subheader("🏆 최적화 결과")
    
    best = optimal_result['best']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 최적 매개변수**")
        st.write(f"핑거 각도: {best['inputs']['theta_deg']:.2f} 도")
        st.write(f"피벗 거리: {best['inputs']['L_pivot']:.1f} mm")
        st.write(f"감속비: {best['inputs']['R_g']}")
        st.write(f"목표 점수: {best['score']:.4f}")
    
    with col2:
        st.markdown("**📊 성능 지표**")
        st.write(f"모터 토크: {best['results']['T_motor_corrected']:.4f} Nm")
        st.write(f"안전 여유도: {best['results']['grip_safety_margin']:.2f}")
        st.write(f"최대 전력: {best['results']['max_power']:.1f} W")
        st.write(f"최대 그립력: {best['results']['max_grip_force']:.1f} N")
    
    # 최적화 과정 시각화
    if optimal_result['all_results']:
        st.subheader("📈 최적화 과정 시각화")
        
        results_df = pd.DataFrame(optimal_result['all_results'])
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('각도-피벗 관계', '토크 분포', '안전성 분포', '전력 분포')
        )
        
        # 3D 산점도 (각도, 피벗, 토크)
        fig.add_trace(
            go.Scatter(
                x=results_df['angle'],
                y=results_df['pivot'],
                mode='markers',
                marker=dict(
                    size=6,
                    color=results_df['torque'],
                    colorscale='viridis',
                    showscale=True
                ),
                name='Angle-Pivot'
            ),
            row=1, col=1
        )
        
        # 최적점 표시
        fig.add_trace(
            go.Scatter(
                x=[best['inputs']['theta_deg']],
                y=[best['inputs']['L_pivot']],
                mode='markers',
                marker=dict(size=15, color='red', symbol='star'),
                name='Optimal Point'
            ),
            row=1, col=1
        )
        
        # 토크 분포
        fig.add_trace(
            go.Histogram(x=results_df['torque'], name='Torque Distribution'),
            row=1, col=2
        )
        
        # 안전성 분포
        fig.add_trace(
            go.Histogram(x=results_df['safety'], name='Safety Distribution'),
            row=2, col=1
        )
        
        # 전력 분포
        fig.add_trace(
            go.Histogram(x=results_df['power'], name='Power Distribution'),
            row=2, col=2
        )
        
        fig.update_layout(height=700, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def display_comparison_analysis(safety_factor: float, efficiency: float):
    """비교 분석 모드"""
    st.header("⚖️ 비교 분석 모드")
    
    st.markdown("여러 설계안을 비교하여 최적의 선택을 도와줍니다.")
    
    # 비교할 설계안 입력
    num_designs = st.slider("비교할 설계안 수", 2, 5, 3)
    
    designs = []
    
    for i in range(num_designs):
        with st.expander(f"🔧 설계안 {i+1}", expanded=(i==0)):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(f"설계안 이름", value=f"Design {i+1}", key=f"name_{i}")
                weight = st.number_input(f"무게 (kg)", value=100.0 + i*20, key=f"weight_{i}")
                angle = st.number_input(f"각도 (도)", value=10.0 + i*2, key=f"angle_{i}")
            
            with col2:
                pivot = st.number_input(f"피벗 거리 (mm)", value=170.0 + i*10, key=f"pivot_{i}")
                gear = st.number_input(f"감속비", value=40 + i*10, key=f"gear_{i}")
                action = st.number_input(f"작동 거리 (mm)", value=100.0, key=f"action_{i}")
            
            designs.append({
                'name': name,
                'inputs': {
                    'W': weight,
                    'theta_deg': angle,
                    'L_pivot': pivot,
                    'L_100mm': action,
                    'R_g': int(gear),
                    'grip_force_req': 500.0,
                    'friction_coeff': 0.5,
                    'material_type': 'Steel',
                    'operating_temp': 25,
                    'max_speed': 100.0,
                    'backlash': 0.5,
                    'stiffness': 1000.0
                }
            })
    
    if st.button("⚖️ 설계안 비교 실행"):
        comparison_results = perform_design_comparison(designs, safety_factor, efficiency)
        display_comparison_results(comparison_results)

def perform_design_comparison(designs, safety_factor, efficiency):
    """설계안 비교 수행"""
    results = []
    
    for design in designs:
        try:
            calc_results = calculate_gripper_forces_advanced(design['inputs'], safety_factor, efficiency)
            
            results.append({
                'name': design['name'],
                'torque': calc_results['T_motor_corrected'],
                'safety': calc_results['grip_safety_margin'],
                'power': calc_results['max_power'],
                'grip_force': calc_results['max_grip_force'],
                'efficiency': calc_results['efficiency'],
                'inputs': design['inputs'],
                'status': 'OK' if calc_results['grip_safety_margin'] > 1.5 else 'Warning'
            })
        except Exception as e:
            results.append({
                'name': design['name'],
                'torque': 'Error',
                'safety': 'Error',
                'power': 'Error',
                'grip_force': 'Error',
                'efficiency': 'Error',
                'inputs': design['inputs'],
                'status': 'Error'
            })
    
    return results

def display_comparison_results(results):
    """비교 결과 표시"""
    st.subheader("📊 설계안 비교 결과")
    
    # 비교 테이블
    comparison_data = []
    for result in results:
        if result['status'] != 'Error':
            comparison_data.append({
                '설계안': result['name'],
                '모터 토크 (Nm)': f"{result['torque']:.4f}",
                '안전 여유도': f"{result['safety']:.2f}",
                '최대 전력 (W)': f"{result['power']:.1f}",
                '최대 그립력 (N)': f"{result['grip_force']:.1f}",
                '상태': result['status']
            })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # 성능 비교 레이더 차트
        st.subheader("🎯 성능 비교 레이더 차트")
        
        # 정규화된 성능 지표
        numeric_results = [r for r in results if r['status'] != 'Error']
        
        if len(numeric_results) > 1:
            # 정규화를 위한 최대값/최소값 계산
            max_torque = max(r['torque'] for r in numeric_results)
            min_torque = min(r['torque'] for r in numeric_results)
            max_safety = max(r['safety'] for r in numeric_results)
            max_power = max(r['power'] for r in numeric_results)
            min_power = min(r['power'] for r in numeric_results)
            
            fig = go.Figure()
            
            categories = ['토크 효율성', '안전성', '전력 효율성', '그립 성능', '종합 점수']
            
            for result in numeric_results:
                # 점수 계산 (높을수록 좋음)
                torque_score = (max_torque - result['torque']) / (max_torque - min_torque + 0.001) * 100
                safety_score = (result['safety'] / max_safety) * 100
                power_score = (max_power - result['power']) / (max_power - min_power + 0.001) * 100
                grip_score = (result['grip_force'] / max(r['grip_force'] for r in numeric_results)) * 100
                overall_score = (torque_score + safety_score + power_score + grip_score) / 4
                
                scores = [torque_score, safety_score, power_score, grip_score, overall_score]
                
                fig.add_trace(go.Scatterpolar(
                    r=scores,
                    theta=categories,
                    fill='toself',
                    name=result['name']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="설계안별 성능 비교"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # 추천 설계안
        st.subheader("🏆 추천 설계안")
        
        if numeric_results:
            # 종합 점수 계산
            best_design = None
            best_score = -1
            
            for result in numeric_results:
                if result['safety'] > 1.5:  # 안전 조건 만족
                    # 정규화된 종합 점수 (토크는 낮을수록, 안전성은 높을수록 좋음)
                    torque_norm = (max_torque - result['torque']) / max_torque
                    safety_norm = result['safety'] / max_safety
                    power_norm = (max_power - result['power']) / max_power
                    
                    total_score = (torque_norm + safety_norm + power_norm) / 3
                    
                    if total_score > best_score:
                        best_score = total_score
                        best_design = result
            
            if best_design:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success(f"**추천 설계안: {best_design['name']}**")
                    st.write(f"종합 점수: {best_score*100:.1f}/100")
                    st.write(f"모터 토크: {best_design['torque']:.4f} Nm")
                    st.write(f"안전 여유도: {best_design['safety']:.2f}")
                    st.write(f"최대 전력: {best_design['power']:.1f} W")
                
                with col2:
                    st.markdown("**📋 설계 매개변수**")
                    inputs = best_design['inputs']
                    st.write(f"무게: {inputs['W']} kg")
                    st.write(f"각도: {inputs['theta_deg']} 도")
                    st.write(f"피벗 거리: {inputs['L_pivot']} mm")
                    st.write(f"감속비: {inputs['R_g']}")
            else:
                st.warning("안전 조건을 만족하는 설계안이 없습니다.")
    
    # 결과 다운로드
    if comparison_data:
        csv = pd.DataFrame(comparison_data).to_csv(index=False)
        st.download_button(
            label="📥 비교 결과 다운로드",
            data=csv,
            file_name="design_comparison_results.csv",
            mime="text/csv"
        )

# 메인 실행
if __name__ == "__main__":
    motor_calc()
