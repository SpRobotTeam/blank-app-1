import streamlit as st
import math
from typing import Tuple

def calculate_gripper_forces(W: float, theta_deg: float, L_pivot: float, L_100mm: float, R_g: float) -> Tuple[float, ...]:
    """
    그리퍼 관련 힘과 토크를 계산하는 함수
    
    Args:
        W: 워크의 무게 (kg)
        theta_deg: 핑거 각도 (도)
        L_pivot: 핑거 회전 중심 거리 (mm)
        L_100mm: 작동 지점 거리 (mm)
        R_g: 감속비
    
    Returns:
        Tuple[float, ...]: (F_push, T_finger_pivot, F_100mm, T_gear_output, T_motor)
    """
    # 단위 변환
    theta_rad = math.radians(theta_deg)
    L_pivot_m = L_pivot / 1000
    L_100mm_m = L_100mm / 1000
    g = 9.81

    # 계산
    F_push = math.tan(theta_rad) * (W * g)
    T_finger_pivot = F_push * L_pivot_m
    F_100mm = T_finger_pivot / L_100mm_m
    T_gear_output = F_100mm * L_100mm_m
    T_motor = T_gear_output / R_g

    return F_push, T_finger_pivot, F_100mm, T_gear_output, T_motor

def motor_calc():
    # 페이지 설정
    st.set_page_config(page_title="로봇 그리퍼 모터 토크 계산기", layout="wide")
    
    # 제목
    st.title("로봇 그리퍼 모터 토크 계산기 (SI 단위)")
    
    # 소개
    st.markdown("""
    이 계산기는 로봇 그리퍼의 모터 토크를 계산하기 위한 도구입니다.  
    각 단계별로 수식과 설명이 포함되어 있으며, 입력값과 계산 결과가 함께 표시됩니다.  
    모든 값은 SI 단위를 사용합니다.
    """)

    # 입력 섹션 - 두 컬럼으로 나누어 배치
    col1, col2 = st.columns(2)
    
    with col1:
        W = st.number_input("워크의 무게 (kg)", value=112.0, step=0.1, min_value=0.0)
        theta_deg = st.number_input("핑거 각도 (도)", value=11.0, step=0.1, min_value=0.0)
        
    with col2:
        L_pivot = st.number_input("핑거 회전 중심 거리 (mm)", value=173.13, step=0.1, min_value=0.0)
        L_100mm = st.number_input("작동 지점 거리 (mm)", value=100.0, step=0.1, min_value=0.0)
        R_g = st.number_input("감속비", value=40, step=1, min_value=1)

    # 계산 실행
    try:
        F_push, T_finger_pivot, F_100mm, T_gear_output, T_motor = calculate_gripper_forces(
            W, theta_deg, L_pivot, L_100mm, R_g
        )

        # 결과 표시
        st.header("계산 결과")
        results = {
            "핑거를 밀어내는 힘": (F_push, "N"),
            "핑거 회전축 토크": (T_finger_pivot, "Nm"),
            "100mm 지점의 힘": (F_100mm, "N"),
            "감속기 출력 토크": (T_gear_output, "Nm"),
            "모터 필요 토크": (T_motor, "Nm")
        }

        # 결과를 표 형태로 표시
        col1, col2 = st.columns([2, 1])
        with col1:
            for name, (value, unit) in results.items():
                st.metric(name, f"{value:.2f} {unit}")

        # 수식 설명
        with st.expander("상세 계산 과정"):
            st.markdown("""
            ### 1. 핑거를 밀어내는 힘
            $F_{push} = \tan(\theta) \cdot (W \cdot g)$
            
            ### 2. 핑거 회전축 토크
            $T_{finger\_pivot} = F_{push} \cdot L_{pivot}$
            
            ### 3. 100mm 지점의 힘
            $F_{100mm} = \frac{T_{finger\_pivot}}{L_{100mm}}$
            
            ### 4. 감속기 출력 토크
            $T_{gear\_output} = F_{100mm} \cdot L_{100mm}$
            
            ### 5. 모터 필요 토크
            $T_{motor} = \frac{T_{gear\_output}}{R_g}$
            """)

    except Exception as e:
        st.error(f"계산 중 오류가 발생했습니다: {str(e)}")
        
    # 푸터
    st.markdown("""
    ---
    ### 참고사항:
    - 모든 계산은 SI 단위계를 기준으로 수행됩니다
    - 음수 값은 입력할 수 없습니다
    - 감속비는 1 이상의 정수여야 합니다
    """)
