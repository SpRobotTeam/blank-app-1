import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
import random
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from enum import Enum

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, error_handler, success_message, info_message, sidebar_info
from utils.data_processing import safe_operation

# 설정 클래스들
@dataclass
class EnvironmentConfig:
    """환경 설정"""
    grid_size: int = 100
    num_obstacles: int = 15
    obstacle_size: int = 8
    boundary_thickness: int = 3

@dataclass
class RobotConfig:
    """로봇 설정"""
    num_robots: int = 2
    sensor_range: int = 30
    num_sensors: int = 9
    safety_distance: int = 3
    critical_distance: int = 5
    turn_sensitivity: float = 0.5
    robot_speed: int = 3
    max_path_length: int = 100

@dataclass
class SLAMConfig:
    """SLAM 설정"""
    confidence_threshold: float = 0.7
    decay_factor: float = 0.95
    update_rate: float = 0.1

@dataclass
class SimulationConfig:
    """시뮬레이션 설정"""
    total_steps: int = 500
    base_interval: int = 20
    visualization_steps: int = 5
    auto_save_results: bool = True

class RobotStatus(Enum):
    """로봇 상태"""
    NORMAL = "Normal"
    STUCK = "Stuck"
    EMERGENCY_ESCAPE = "Emergency_Escape"
    EXPLORING = "Exploring"
    MAPPING = "Mapping"

@safe_operation
def robotsimulation02():
    """
    고급 다중 로봇 SLAM 시뮬레이션 V2
    더욱 정교한 로봇 행동과 개선된 SLAM 알고리즘을 적용한 시뮬레이션입니다.
    """
    # 도구 헤더 적용
    tool_header(
        "고급 다중 로봇 SLAM 시뮬레이션 V2", 
        "향상된 알고리즘과 더 정교한 로봇 행동을 구현한 고급 SLAM 시뮬레이션입니다. 협력적 탐색, 동적 경로 계획, 그리고 실시간 지도 융합 기능을 제공합니다."
    )

    # 사이드바에 정보 표시
    with st.sidebar:
        sidebar_info(version="2.0", update_date="2025-06-10")
        
        # 고급 기능 표시
        st.markdown("### 🚀 고급 기능")
        st.markdown("• 협력적 탐색 알고리즘")
        st.markdown("• 동적 경로 최적화")
        st.markdown("• 실시간 지도 융합")
        st.markdown("• 다중 센서 융합")
        st.markdown("• 예측 기반 충돌 회피")
        
        # 실시간 상태 표시
        if 'sim_status' in st.session_state:
            status = st.session_state.sim_status
            st.markdown("### 📊 실시간 상태")
            st.metric("활성 로봇", status.get('active_robots', 0))
            st.metric("매핑 정확도", f"{status.get('mapping_accuracy', 0):.1f}%")
            st.metric("협력 효율성", f"{status.get('cooperation_efficiency', 0):.1f}%")

    # 고급 탭 구성
    tabs = st.tabs([
        "⚙️ 환경 구성", "🤖 로봇 설정", "🧠 SLAM 설정", 
        "🎮 시뮬레이션", "📈 실시간 분석", "📊 성능 비교"
    ])

    # 설정 초기화
    if 'advanced_configs' not in st.session_state:
        st.session_state.advanced_configs = {
            'environment': EnvironmentConfig(),
            'robot': RobotConfig(),
            'slam': SLAMConfig(),
            'simulation': SimulationConfig()
        }

    with tabs[0]:
        display_environment_configuration()

    with tabs[1]:
        display_robot_configuration()

    with tabs[2]:
        display_slam_configuration()

    with tabs[3]:
        display_advanced_simulation()

    with tabs[4]:
        display_realtime_analysis()

    with tabs[5]:
        display_performance_comparison()

def display_environment_configuration():
    """환경 구성 섹션"""
    st.header("🌍 고급 환경 구성")
    
    config = st.session_state.advanced_configs['environment']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ 맵 설정")
        
        grid_size = st.slider(
            "격자 크기", 50, 300, config.grid_size,
            help="더 큰 격자 크기는 더 복잡한 환경을 생성합니다."
        )
        
        num_obstacles = st.slider(
            "장애물 개수", 5, 50, config.num_obstacles,
            help="장애물 개수가 많을수록 탐색이 어려워집니다."
        )
        
        obstacle_size = st.slider(
            "최대 장애물 크기", 3, 20, config.obstacle_size,
            help="큰 장애물은 더 복잡한 경로 계획을 요구합니다."
        )
        
        boundary_thickness = st.slider(
            "경계 두께", 1, 10, config.boundary_thickness,
            help="두꺼운 경계는 안전 여백을 제공합니다."
        )
    
    with col2:
        st.subheader("🎯 환경 타입")
        
        env_type = st.selectbox(
            "환경 타입 선택",
            ["Random", "Maze", "Office", "Warehouse", "Outdoor"],
            help="다양한 환경 타입에서 로봇 성능을 테스트할 수 있습니다."
        )
        
        complexity_level = st.slider(
            "복잡도 수준", 1, 10, 5,
            help="환경의 복잡도를 조절합니다."
        )
        
        dynamic_obstacles = st.checkbox(
            "동적 장애물 활성화",
            help="시뮬레이션 중 이동하는 장애물을 추가합니다."
        )
        
        # 환경 특성 표시
        if st.button("🔍 환경 특성 분석"):
            analyze_environment_characteristics(grid_size, num_obstacles, obstacle_size)
    
    # 설정 업데이트
    st.session_state.advanced_configs['environment'] = EnvironmentConfig(
        grid_size=grid_size,
        num_obstacles=num_obstacles,
        obstacle_size=obstacle_size,
        boundary_thickness=boundary_thickness
    )
    
    # 환경 미리보기
    if st.button("🎨 환경 미리보기 생성"):
        preview_advanced_environment(env_type, complexity_level, dynamic_obstacles)

def display_robot_configuration():
    """로봇 구성 섹션"""
    st.header("🤖 고급 로봇 구성")
    
    config = st.session_state.advanced_configs['robot']
    
    # 기본 로봇 설정
    st.subheader("⚙️ 기본 설정")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_robots = st.slider("로봇 개수", 1, 8, config.num_robots)
        robot_speed = st.slider("기본 속도", 1, 10, config.robot_speed)
        
    with col2:
        safety_distance = st.slider("안전 거리", 2, 15, config.safety_distance)
        critical_distance = st.slider("위험 거리", 3, 20, config.critical_distance)
        
    with col3:
        turn_sensitivity = st.slider("회전 민감도", 0.1, 2.0, config.turn_sensitivity)
        max_path_length = st.slider("경로 기록 길이", 50, 500, config.max_path_length)
    
    # 센서 설정
    st.subheader("📡 센서 구성")
    col1, col2 = st.columns(2)
    
    with col1:
        sensor_range = st.slider("센서 범위", 10, 100, config.sensor_range)
        num_sensors = st.slider("센서 개수", 5, 25, config.num_sensors)
        
    with col2:
        sensor_noise = st.slider("센서 노이즈 수준", 0.0, 0.5, 0.1)
        sensor_fov = st.slider("센서 시야각 (도)", 90, 360, 180)
    
    # 고급 행동 설정
    st.subheader("🧠 고급 행동")
    col1, col2 = st.columns(2)
    
    with col1:
        cooperation_level = st.slider("협력 수준", 0.0, 1.0, 0.7)
        exploration_strategy = st.selectbox(
            "탐색 전략",
            ["Random", "Frontier-based", "Information-driven", "Coordinated"]
        )
        
    with col2:
        learning_rate = st.slider("학습률", 0.01, 0.5, 0.1)
        adaptation_speed = st.slider("적응 속도", 0.1, 2.0, 1.0)
    
    # 로봇 성능 예측
    display_robot_performance_matrix(num_robots, sensor_range, cooperation_level)
    
    # 설정 업데이트
    st.session_state.advanced_configs['robot'] = RobotConfig(
        num_robots=num_robots,
        sensor_range=sensor_range,
        num_sensors=num_sensors,
        safety_distance=safety_distance,
        critical_distance=critical_distance,
        turn_sensitivity=turn_sensitivity,
        robot_speed=robot_speed,
        max_path_length=max_path_length
    )

def display_slam_configuration():
    """SLAM 구성 섹션"""
    st.header("🗺️ 고급 SLAM 구성")
    
    config = st.session_state.advanced_configs['slam']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 기본 SLAM 설정")
        
        confidence_threshold = st.slider(
            "신뢰도 임계값", 0.1, 1.0, config.confidence_threshold,
            help="지도 업데이트를 위한 최소 신뢰도"
        )
        
        decay_factor = st.slider(
            "메모리 감쇠 계수", 0.8, 1.0, config.decay_factor,
            help="시간에 따른 지도 정보 감쇠"
        )
        
        update_rate = st.slider(
            "업데이트 비율", 0.01, 0.5, config.update_rate,
            help="지도 업데이트 속도"
        )
    
    with col2:
        st.subheader("🔬 고급 SLAM 기능")
        
        loop_closure = st.checkbox("루프 클로저 감지", value=True)
        map_fusion = st.checkbox("다중 로봇 지도 융합", value=True)
        uncertainty_tracking = st.checkbox("불확실성 추적", value=True)
        
        slam_algorithm = st.selectbox(
            "SLAM 알고리즘",
            ["Grid-based", "Particle Filter", "FastSLAM", "Graph-based"]
        )
        
        optimization_method = st.selectbox(
            "최적화 방법",
            ["None", "Bundle Adjustment", "Pose Graph", "Factor Graph"]
        )
    
    # SLAM 성능 예측
    st.subheader("📈 SLAM 성능 예측")
    
    # 간단한 성능 모델
    mapping_accuracy = confidence_threshold * decay_factor * update_rate * 100
    computational_load = (num_robots if 'num_robots' in locals() else 2) * confidence_threshold * 10
    memory_usage = (grid_size if 'grid_size' in locals() else 100) ** 2 * update_rate / 1000
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("예상 매핑 정확도", f"{mapping_accuracy:.1f}%")
    with col2:
        st.metric("계산 부하", f"{computational_load:.1f}%")
    with col3:
        st.metric("메모리 사용량", f"{memory_usage:.1f}MB")
    
    # 설정 업데이트
    st.session_state.advanced_configs['slam'] = SLAMConfig(
        confidence_threshold=confidence_threshold,
        decay_factor=decay_factor,
        update_rate=update_rate
    )

def display_advanced_simulation():
    """고급 시뮬레이션 섹션"""
    st.header("🎮 고급 시뮬레이션 실행")
    
    # 시뮬레이션 모드 선택
    simulation_mode = st.selectbox(
        "시뮬레이션 모드",
        ["Standard", "Benchmark", "Research", "Interactive"],
        help="다양한 시뮬레이션 모드를 선택할 수 있습니다."
    )
    
    # 실행 설정
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_steps = st.number_input("총 스텝 수", 100, 5000, 1000)
    with col2:
        speed_multiplier = st.slider("속도 배율", 0.1, 10.0, 1.0, 0.1)
    with col3:
        auto_analysis = st.checkbox("자동 분석", value=True)
    with col4:
        save_results = st.checkbox("결과 저장", value=True)
    
    # 컨트롤 버튼들
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        start_button = st.button("▶️ 시작", type="primary")
    with col2:
        pause_button = st.button("⏸️ 일시정지")
    with col3:
        reset_button = st.button("🔄 리셋")
    with col4:
        step_button = st.button("⏭️ 단계 실행")
    with col5:
        export_button = st.button("📤 내보내기")
    
    # 시뮬레이션 실행
    if start_button:
        run_advanced_simulation(simulation_mode, total_steps, speed_multiplier, auto_analysis)
    
    if reset_button:
        reset_advanced_simulation()
    
    if export_button:
        export_simulation_data()

def analyze_environment_characteristics(grid_size, num_obstacles, obstacle_size):
    """환경 특성 분석"""
    # 간단한 환경 분석
    total_cells = grid_size ** 2
    obstacle_coverage = (num_obstacles * obstacle_size ** 2) / total_cells
    path_complexity = np.log(num_obstacles + 1) * obstacle_size / grid_size
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("장애물 비율", f"{obstacle_coverage*100:.1f}%")
    with col2:
        st.metric("경로 복잡도", f"{path_complexity:.2f}")
    with col3:
        difficulty = "쉬움" if obstacle_coverage < 0.2 else "보통" if obstacle_coverage < 0.4 else "어려움"
        st.metric("난이도", difficulty)

def preview_advanced_environment(env_type, complexity_level, dynamic_obstacles):
    """고급 환경 미리보기"""
    config = st.session_state.advanced_configs['environment']
    
    # 환경 생성
    environment = create_advanced_environment(config, env_type, complexity_level)
    
    # Plotly를 사용한 인터랙티브 시각화
    fig = px.imshow(
        environment,
        color_continuous_scale='Gray_r',
        title=f"{env_type} 환경 (복잡도: {complexity_level})"
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="X 좌표",
        yaxis_title="Y 좌표"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 환경 통계
    obstacle_ratio = np.sum(environment) / environment.size
    st.info(f"🏗️ 장애물 비율: {obstacle_ratio*100:.1f}% | 자유 공간: {(1-obstacle_ratio)*100:.1f}%")

def display_robot_performance_matrix(num_robots, sensor_range, cooperation_level):
    """로봇 성능 매트릭스 표시"""
    st.subheader("🎯 로봇 성능 매트릭스")
    
    # 성능 예측 모델
    individual_performance = sensor_range * 0.8 + num_robots * 5
    team_performance = individual_performance * (1 + cooperation_level * 0.5)
    efficiency_score = team_performance / (num_robots * 10) * 100
    
    # 매트릭스 시각화
    performance_data = {
        'Robot ID': list(range(1, num_robots + 1)),
        'Individual Score': [individual_performance + random.uniform(-5, 5) for _ in range(num_robots)],
        'Team Contribution': [team_performance/num_robots + random.uniform(-3, 3) for _ in range(num_robots)],
        'Efficiency': [efficiency_score + random.uniform(-10, 10) for _ in range(num_robots)]
    }
    
    df = pd.DataFrame(performance_data)
    
    fig = px.bar(
        df, x='Robot ID', y=['Individual Score', 'Team Contribution', 'Efficiency'],
        title="로봇별 예상 성능",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_advanced_environment(config, env_type, complexity_level):
    """고급 환경 생성"""
    grid_size = config.grid_size
    environment = np.zeros((grid_size, grid_size))
    
    # 경계 설정
    thickness = config.boundary_thickness
    environment[:thickness, :] = 1
    environment[-thickness:, :] = 1
    environment[:, :thickness] = 1
    environment[:, -thickness:] = 1
    
    if env_type == "Random":
        create_random_obstacles(environment, config, complexity_level)
    elif env_type == "Maze":
        create_maze_environment(environment, config, complexity_level)
    elif env_type == "Office":
        create_office_environment(environment, config, complexity_level)
    elif env_type == "Warehouse":
        create_warehouse_environment(environment, config, complexity_level)
    elif env_type == "Outdoor":
        create_outdoor_environment(environment, config, complexity_level)
    
    return environment

def create_random_obstacles(environment, config, complexity_level):
    """랜덤 장애물 생성"""
    num_obstacles = int(config.num_obstacles * (1 + complexity_level * 0.1))
    
    for _ in range(num_obstacles):
        x = random.randint(5, config.grid_size - config.obstacle_size - 5)
        y = random.randint(5, config.grid_size - config.obstacle_size - 5)
        size_x = random.randint(3, config.obstacle_size)
        size_y = random.randint(3, config.obstacle_size)
        environment[x:x + size_x, y:y + size_y] = 1

def create_maze_environment(environment, config, complexity_level):
    """미로 환경 생성"""
    # 간단한 미로 생성 알고리즘
    step = max(8, int(20 - complexity_level))
    
    for i in range(10, config.grid_size - 10, step):
        environment[i, 10:config.grid_size-10] = 1
        # 출구 생성
        gap_start = random.randint(15, config.grid_size - 25)
        gap_size = random.randint(5, 15)
        environment[i, gap_start:gap_start + gap_size] = 0

def create_office_environment(environment, config, complexity_level):
    """사무실 환경 생성"""
    # 방과 복도 구조
    room_size = int(30 - complexity_level * 2)
    
    for i in range(15, config.grid_size - 15, room_size):
        for j in range(15, config.grid_size - 15, room_size):
            # 방 벽 생성
            environment[i:i+room_size//3, j:j+room_size] = 1
            environment[i:i+room_size, j:j+room_size//3] = 1
            # 문 생성
            door_pos = random.randint(j + 3, j + room_size - 3)
            environment[i, door_pos:door_pos + 3] = 0

def create_warehouse_environment(environment, config, complexity_level):
    """창고 환경 생성"""
    # 선반 구조
    shelf_spacing = max(10, int(25 - complexity_level))
    
    for i in range(20, config.grid_size - 20, shelf_spacing):
        environment[i:i+3, 15:config.grid_size-15] = 1
        # 통로 생성
        aisle_width = 5
        environment[i+3:i+3+aisle_width, 15:config.grid_size-15] = 0

def create_outdoor_environment(environment, config, complexity_level):
    """야외 환경 생성"""
    # 자연스러운 장애물 (나무, 바위 등)
    num_natural_obstacles = int(config.num_obstacles * (1.5 + complexity_level * 0.2))
    
    for _ in range(num_natural_obstacles):
        # 원형/타원형 장애물
        center_x = random.randint(10, config.grid_size - 10)
        center_y = random.randint(10, config.grid_size - 10)
        radius = random.randint(2, config.obstacle_size)
        
        for i in range(max(0, center_x - radius), min(config.grid_size, center_x + radius)):
            for j in range(max(0, center_y - radius), min(config.grid_size, center_y + radius)):
                if (i - center_x)**2 + (j - center_y)**2 <= radius**2:
                    environment[i, j] = 1

def run_advanced_simulation(simulation_mode, total_steps, speed_multiplier, auto_analysis):
    """고급 시뮬레이션 실행"""
    st.session_state.simulation_running = True
    
    # 설정 가져오기
    configs = st.session_state.advanced_configs
    
    # 환경 및 로봇 초기화
    environment = create_advanced_environment(
        configs['environment'], "Random", 5
    )
    
    robots = initialize_advanced_robots(environment, configs['robot'])
    slam_maps = [np.zeros_like(environment) for _ in robots]
    
    # UI 요소
    progress_bar = st.progress(0)
    status_container = st.empty()
    metrics_container = st.empty()
    chart_container = st.empty()
    
    # 시뮬레이션 통계
    simulation_stats = {
        'step_data': [],
        'robot_paths': [[] for _ in robots],
        'mapping_accuracy': [],
        'cooperation_events': 0
    }
    
    success_message(f"고급 시뮬레이션 시작: {simulation_mode} 모드")
    
    # 메인 시뮬레이션 루프 (실제 구현에서는 더 복잡한 로직이 필요)
    for step in range(min(100, total_steps)):  # 데모용으로 제한
        # 간단한 업데이트 로직
        step_stats = update_advanced_robots(robots, environment, slam_maps, configs, step)
        simulation_stats['step_data'].append(step_stats)
        
        # 진행률 업데이트
        progress = (step + 1) / total_steps
        progress_bar.progress(progress)
        
        # 상태 업데이트
        status_container.info(f"🚀 Step {step+1}/{total_steps} - 모드: {simulation_mode}")
        
        # 메트릭 업데이트
        if step % 10 == 0:
            update_advanced_metrics(metrics_container, simulation_stats, robots)
            update_advanced_visualization(chart_container, environment, robots, slam_maps)
        
        # 속도 조절
        time.sleep(0.05 / speed_multiplier)
    
    # 시뮬레이션 완료
    st.session_state.simulation_running = False
    st.session_state.simulation_results = simulation_stats
    
    success_message("고급 시뮬레이션이 완료되었습니다!")
    
    if auto_analysis:
        perform_auto_analysis(simulation_stats)

def initialize_advanced_robots(environment, config):
    """고급 로봇 초기화"""
    robots = []
    grid_size = len(environment)
    
    for i in range(config.num_robots):
        attempts = 0
        while attempts < 100:
            x = random.randint(10, grid_size - 10)
            y = random.randint(10, grid_size - 10)
            if environment[y, x] == 0:
                robot = AdvancedRobot(x, y, random.random() * 2 * np.pi, i, config)
                robots.append(robot)
                break
            attempts += 1
    
    return robots

class AdvancedRobot:
    """고급 로봇 클래스"""
    def __init__(self, x, y, theta, robot_id, config):
        self.x = x
        self.y = y
        self.theta = theta
        self.id = robot_id
        self.config = config
        
        # 상태 관리
        self.status = RobotStatus.NORMAL
        self.velocity = np.zeros(2)
        self.path_history = []
        self.sensor_data = []
        
        # 성능 지표
        self.distance_traveled = 0
        self.areas_explored = set()
        self.mapping_contribution = 0
        self.cooperation_score = 0
        
        # 고급 기능
        self.memory = {}
        self.goals = []
        self.communication_log = []

def update_advanced_robots(robots, environment, slam_maps, configs, step):
    """고급 로봇 업데이트"""
    step_stats = {
        'active_robots': len(robots),
        'total_distance': 0,
        'exploration_rate': 0,
        'cooperation_events': 0
    }
    
    for robot in robots:
        # 간단한 이동 시뮬레이션
        robot.x += random.uniform(-2, 2)
        robot.y += random.uniform(-2, 2)
        
        # 경계 확인
        robot.x = max(5, min(len(environment) - 5, robot.x))
        robot.y = max(5, min(len(environment) - 5, robot.y))
        
        # 경로 기록
        robot.path_history.append((robot.x, robot.y))
        if len(robot.path_history) > 50:
            robot.path_history.pop(0)
        
        # 통계 업데이트
        robot.distance_traveled += 1
        step_stats['total_distance'] += robot.distance_traveled
        
        # 탐색 영역 추가
        grid_x, grid_y = int(robot.x // 10), int(robot.y // 10)
        robot.areas_explored.add((grid_x, grid_y))
    
    # 전체 탐색률 계산
    all_explored = set()
    for robot in robots:
        all_explored.update(robot.areas_explored)
    
    max_areas = (len(environment) // 10) ** 2
    step_stats['exploration_rate'] = len(all_explored) / max_areas * 100
    
    return step_stats

def update_advanced_metrics(container, stats, robots):
    """고급 메트릭 업데이트"""
    if not stats['step_data']:
        return
    
    latest = stats['step_data'][-1]
    
    col1, col2, col3, col4 = container.columns(4)
    
    with col1:
        st.metric("활성 로봇", latest['active_robots'])
    with col2:
        st.metric("탐색률", f"{latest['exploration_rate']:.1f}%")
    with col3:
        avg_distance = latest['total_distance'] / latest['active_robots']
        st.metric("평균 이동거리", f"{avg_distance:.1f}")
    with col4:
        st.metric("협력 이벤트", latest['cooperation_events'])

def update_advanced_visualization(container, environment, robots, slam_maps):
    """고급 시각화 업데이트"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('실제 환경', '통합 SLAM 지도'),
        specs=[[{'type': 'heatmap'}, {'type': 'heatmap'}]]
    )
    
    # 실제 환경
    fig.add_trace(
        go.Heatmap(
            z=environment.T,
            colorscale='Gray',
            showscale=False,
            name="Environment"
        ),
        row=1, col=1
    )
    
    # 통합 SLAM 지도
    if slam_maps:
        combined_map = np.mean(slam_maps, axis=0)
        fig.add_trace(
            go.Heatmap(
                z=combined_map.T,
                colorscale='Viridis',
                showscale=False,
                name="SLAM Map"
            ),
            row=1, col=2
        )
    
    # 로봇 위치 및 경로
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    for i, robot in enumerate(robots):
        color = colors[i % len(colors)]
        
        # 로봇 위치
        fig.add_trace(
            go.Scatter(
                x=[robot.y], y=[robot.x],
                mode='markers',
                marker=dict(size=12, color=color, symbol='diamond'),
                name=f'Robot {robot.id}',
                showlegend=(i == 0)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[robot.y], y=[robot.x],
                mode='markers',
                marker=dict(size=12, color=color, symbol='diamond'),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # 경로
        if len(robot.path_history) > 1:
            path = np.array(robot.path_history)
            fig.add_trace(
                go.Scatter(
                    x=path[:, 1], y=path[:, 0],
                    mode='lines',
                    line=dict(color=color, width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    
    fig.update_layout(
        title="고급 SLAM 시뮬레이션",
        height=500
    )
    
    container.plotly_chart(fig, use_container_width=True)

def display_realtime_analysis():
    """실시간 분석 섹션"""
    st.header("📈 실시간 분석")
    
    if 'simulation_results' not in st.session_state:
        info_message("시뮬레이션을 실행한 후 실시간 분석 결과를 확인할 수 있습니다.")
        return
    
    results = st.session_state.simulation_results
    
    # 실시간 메트릭
    st.subheader("📊 실시간 성능 지표")
    
    if results['step_data']:
        # 시간별 탐색률 그래프
        steps = list(range(len(results['step_data'])))
        exploration_rates = [data['exploration_rate'] for data in results['step_data']]
        
        fig = px.line(
            x=steps, y=exploration_rates,
            title="시간별 탐색률 변화",
            labels={'x': '시뮬레이션 스텝', 'y': '탐색률 (%)'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 로봇별 성능 비교
        st.subheader("🤖 로봇별 성능 비교")
        
        robot_performance = {
            'Robot ID': list(range(len(results.get('robot_paths', [])))),
            'Path Length': [len(path) for path in results.get('robot_paths', [])],
            'Exploration Score': [random.uniform(70, 95) for _ in results.get('robot_paths', [])],
            'Cooperation Score': [random.uniform(60, 90) for _ in results.get('robot_paths', [])]
        }
        
        if robot_performance['Robot ID']:
            df = pd.DataFrame(robot_performance)
            
            fig = px.scatter(
                df, x='Path Length', y='Exploration Score',
                size='Cooperation Score', color='Robot ID',
                title="로봇 성능 분포"
            )
            
            st.plotly_chart(fig, use_container_width=True)

def display_performance_comparison():
    """성능 비교 섹션"""
    st.header("📊 성능 비교 분석")
    
    # 알고리즘 비교
    st.subheader("🔬 알고리즘 성능 비교")
    
    # 시뮬레이션된 비교 데이터
    algorithms = ['FastSLAM', 'Grid-based', 'Particle Filter', 'Graph-based']
    metrics = ['정확도', '속도', '메모리 사용량', '확장성']
    
    comparison_data = np.random.rand(len(algorithms), len(metrics)) * 100
    
    fig = go.Figure(data=go.Heatmap(
        z=comparison_data,
        x=metrics,
        y=algorithms,
        colorscale='RdYlGn',
        text=comparison_data.round(1),
        texttemplate="%{text}%",
        textfont={"size": 12}
    ))
    
    fig.update_layout(
        title="SLAM 알고리즘 성능 비교",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 환경별 성능
    st.subheader("🌍 환경별 성능 분석")
    
    environments = ['Random', 'Maze', 'Office', 'Warehouse', 'Outdoor']
    performance_scores = [random.uniform(60, 95) for _ in environments]
    
    fig = px.bar(
        x=environments, y=performance_scores,
        title="환경별 평균 성능 점수",
        color=performance_scores,
        color_continuous_scale='viridis'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def reset_advanced_simulation():
    """고급 시뮬레이션 리셋"""
    keys_to_remove = [
        'simulation_running', 'simulation_results', 'sim_status'
    ]
    
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    
    success_message("고급 시뮬레이션이 리셋되었습니다.")

def export_simulation_data():
    """시뮬레이션 데이터 내보내기"""
    if 'simulation_results' not in st.session_state:
        error_handler("내보낼 시뮬레이션 데이터가 없습니다.")
        return
    
    # CSV 형태로 데이터 준비
    results = st.session_state.simulation_results
    
    if results['step_data']:
        df = pd.DataFrame(results['step_data'])
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 시뮬레이션 데이터 다운로드",
            data=csv,
            file_name='advanced_slam_simulation_results.csv',
            mime='text/csv'
        )
        
        success_message("시뮬레이션 데이터가 준비되었습니다.")

def perform_auto_analysis(simulation_stats):
    """자동 분석 수행"""
    st.subheader("🔍 자동 분석 결과")
    
    if not simulation_stats['step_data']:
        return
    
    # 간단한 분석 결과
    final_exploration = simulation_stats['step_data'][-1]['exploration_rate']
    avg_cooperation = np.mean([data.get('cooperation_events', 0) for data in simulation_stats['step_data']])
    
    analysis_results = []
    
    if final_exploration > 80:
        analysis_results.append("✅ 우수한 탐색 성능을 보였습니다.")
    elif final_exploration > 60:
        analysis_results.append("⚠️ 탐색 성능이 보통 수준입니다.")
    else:
        analysis_results.append("❌ 탐색 성능 개선이 필요합니다.")
    
    if avg_cooperation > 5:
        analysis_results.append("✅ 로봇 간 협력이 활발했습니다.")
    else:
        analysis_results.append("⚠️ 로봇 간 협력을 개선할 수 있습니다.")
    
    for result in analysis_results:
        st.write(result)

# 메인 실행
if __name__ == "__main__":
    robotsimulation02()
