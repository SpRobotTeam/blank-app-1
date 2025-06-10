import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
import random
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# 공통 유틸리티 임포트
from utils.ui_components import tool_header, error_handler, success_message, info_message, sidebar_info
from utils.data_processing import safe_operation

@safe_operation
def robotsimulation():
    """
    다중 로봇 SLAM 시뮬레이션
    여러 로봇이 환경을 탐색하고 지도를 작성하는 과정을 시뮬레이션합니다.
    """
    # 도구 헤더 적용
    tool_header(
        "다중 로봇 SLAM 시뮬레이션", 
        "여러 로봇이 미지의 환경을 탐색하며 실시간으로 지도를 작성하는 SLAM(Simultaneous Localization and Mapping) 시뮬레이션입니다. 로봇의 자율 항법과 협력 탐색을 체험해보세요."
    )

    # 사이드바에 정보 표시
    with st.sidebar:
        sidebar_info(version="2.0", update_date="2025-06-10")
        
        # 시뮬레이션 상태 표시
        if 'simulation_running' in st.session_state and st.session_state.simulation_running:
            st.success("🟢 시뮬레이션 실행 중")
        else:
            st.info("⚪ 시뮬레이션 대기 중")
        
        # 성능 지표 표시
        if 'sim_stats' in st.session_state:
            stats = st.session_state.sim_stats
            st.markdown("### 📊 성능 지표")
            st.metric("탐색률", f"{stats.get('exploration_rate', 0):.1f}%")
            st.metric("충돌 횟수", stats.get('collisions', 0))
            st.metric("평균 속도", f"{stats.get('avg_speed', 0):.2f}")

    # 탭 구성
    tabs = st.tabs(["⚙️ 시뮬레이션 설정", "🤖 로봇 매개변수", "🎮 시뮬레이션 실행", "📈 분석 결과"])

    # 매개변수 저장을 위한 세션 상태 초기화
    if 'sim_params' not in st.session_state:
        st.session_state.sim_params = get_default_parameters()

    with tabs[0]:
        display_environment_settings()

    with tabs[1]:
        display_robot_settings()

    with tabs[2]:
        display_simulation_execution()

    with tabs[3]:
        display_analysis_results()

def get_default_parameters():
    """기본 시뮬레이션 매개변수"""
    return {
        'grid_size': 100,
        'num_obstacles': 15,
        'obstacle_size': 8,
        'num_robots': 2,
        'sensor_range': 30,
        'num_sensors': 9,
        'robot_speed': 3,
        'safety_distance': 3,
        'critical_distance': 5,
        'turn_sensitivity': 0.5,
        'total_steps': 500,
        'base_interval': 20,
        'visualization_steps': 5,
        'confidence_threshold': 0.7,
        'decay_factor': 0.95
    }

def display_environment_settings():
    """환경 설정 섹션"""
    st.header("🌍 환경 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("맵 구성")
        grid_size = st.slider(
            "격자 크기", 50, 200, 
            st.session_state.sim_params['grid_size'],
            help="시뮬레이션 환경의 격자 크기를 설정합니다."
        )
        
        num_obstacles = st.slider(
            "장애물 개수", 5, 30, 
            st.session_state.sim_params['num_obstacles'],
            help="환경에 배치될 랜덤 장애물의 개수입니다."
        )
        
        obstacle_size = st.slider(
            "최대 장애물 크기", 3, 15, 
            st.session_state.sim_params['obstacle_size'],
            help="개별 장애물의 최대 크기입니다."
        )
    
    with col2:
        st.subheader("시뮬레이션 설정")
        total_steps = st.slider(
            "시뮬레이션 스텝 수", 100, 2000, 
            st.session_state.sim_params['total_steps'],
            help="전체 시뮬레이션의 스텝 수입니다."
        )
        
        base_interval = st.slider(
            "기본 업데이트 간격 (ms)", 10, 100, 
            st.session_state.sim_params['base_interval'],
            help="시뮬레이션 업데이트 간격입니다."
        )
        
        visualization_steps = st.slider(
            "시각화 업데이트 빈도", 1, 10, 
            st.session_state.sim_params['visualization_steps'],
            help="화면 업데이트 빈도를 설정합니다."
        )
    
    # 매개변수 업데이트
    st.session_state.sim_params.update({
        'grid_size': grid_size,
        'num_obstacles': num_obstacles,
        'obstacle_size': obstacle_size,
        'total_steps': total_steps,
        'base_interval': base_interval,
        'visualization_steps': visualization_steps
    })
    
    # 환경 미리보기
    if st.button("🔍 환경 미리보기"):
        preview_environment()

def display_robot_settings():
    """로봇 설정 섹션"""
    st.header("🤖 로봇 매개변수")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("기본 설정")
        num_robots = st.slider(
            "로봇 개수", 1, 5, 
            st.session_state.sim_params['num_robots'],
            help="시뮬레이션에 참여할 로봇의 개수입니다."
        )
        
        robot_speed = st.slider(
            "로봇 속도", 1, 5, 
            st.session_state.sim_params['robot_speed'],
            help="로봇의 이동 속도입니다."
        )
        
        safety_distance = st.slider(
            "안전 거리", 2, 8, 
            st.session_state.sim_params['safety_distance'],
            help="장애물과 다른 로봇으로부터의 최소 안전 거리입니다."
        )
    
    with col2:
        st.subheader("센서 설정")
        sensor_range = st.slider(
            "센서 범위", 10, 50, 
            st.session_state.sim_params['sensor_range'],
            help="로봇 센서의 감지 범위입니다."
        )
        
        num_sensors = st.slider(
            "센서 개수", 5, 15, 
            st.session_state.sim_params['num_sensors'],
            help="로봇이 가진 센서의 개수입니다."
        )
    
    with col3:
        st.subheader("항법 설정")
        critical_distance = st.slider(
            "위험 거리", 3, 10, 
            st.session_state.sim_params['critical_distance'],
            help="장애물 회피를 시작하는 거리입니다."
        )
        
        turn_sensitivity = st.slider(
            "회전 민감도", 0.1, 1.0, 
            st.session_state.sim_params['turn_sensitivity'],
            help="로봇의 회전 반응 민감도입니다."
        )
    
    # SLAM 설정
    st.subheader("🗺️ SLAM 매개변수")
    col1, col2 = st.columns(2)
    
    with col1:
        confidence_threshold = st.slider(
            "신뢰도 임계값", 0.1, 1.0, 
            st.session_state.sim_params['confidence_threshold'],
            help="지도 업데이트를 위한 최소 신뢰도입니다."
        )
    
    with col2:
        decay_factor = st.slider(
            "메모리 감쇠 계수", 0.9, 1.0, 
            st.session_state.sim_params['decay_factor'],
            help="시간에 따른 지도 정보의 감쇠 정도입니다."
        )
    
    # 매개변수 업데이트
    st.session_state.sim_params.update({
        'num_robots': num_robots,
        'robot_speed': robot_speed,
        'safety_distance': safety_distance,
        'sensor_range': sensor_range,
        'num_sensors': num_sensors,
        'critical_distance': critical_distance,
        'turn_sensitivity': turn_sensitivity,
        'confidence_threshold': confidence_threshold,
        'decay_factor': decay_factor
    })
    
    # 로봇 성능 예측
    display_robot_performance_prediction()

def display_robot_performance_prediction():
    """로봇 성능 예측 표시"""
    st.subheader("🎯 성능 예측")
    
    params = st.session_state.sim_params
    
    # 간단한 성능 예측 모델
    exploration_efficiency = min(100, (params['sensor_range'] * params['num_sensors'] * params['robot_speed']) / 50)
    collision_risk = max(0, 100 - (params['safety_distance'] * params['critical_distance'] * 10))
    mapping_accuracy = params['confidence_threshold'] * params['decay_factor'] * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("탐색 효율성", f"{exploration_efficiency:.1f}%")
    with col2:
        st.metric("충돌 위험도", f"{collision_risk:.1f}%")
    with col3:
        st.metric("지도 정확도", f"{mapping_accuracy:.1f}%")

def preview_environment():
    """환경 미리보기"""
    params = st.session_state.sim_params
    environment = create_environment(
        params['grid_size'], 
        params['num_obstacles'], 
        params['obstacle_size']
    )
    
    fig = px.imshow(
        environment, 
        color_continuous_scale='Gray',
        title="환경 미리보기 (검은색: 장애물, 흰색: 자유 공간)"
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_simulation_execution():
    """시뮬레이션 실행 섹션"""
    st.header("🎮 시뮬레이션 실행")
    
    # 컨트롤 버튼들
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        start_button = st.button("▶️ 시뮬레이션 시작", type="primary")
    
    with col2:
        pause_button = st.button("⏸️ 일시정지")
    
    with col3:
        reset_button = st.button("🔄 리셋")
    
    with col4:
        speed_multiplier = st.slider("속도 배율", 0.1, 5.0, 1.0, 0.1)
    
    # 시뮬레이션 상태 관리
    if reset_button:
        reset_simulation()
    
    if pause_button:
        st.session_state.simulation_paused = not st.session_state.get('simulation_paused', False)
    
    if start_button:
        run_simulation(speed_multiplier)

def run_simulation(speed_multiplier):
    """시뮬레이션 실행"""
    params = st.session_state.sim_params
    
    # 초기화
    st.session_state.simulation_running = True
    environment = create_environment(
        params['grid_size'], 
        params['num_obstacles'], 
        params['obstacle_size']
    )
    
    # 로봇 초기화
    robots = initialize_robots(environment, params)
    slam_map = np.zeros_like(environment)
    
    # 시뮬레이션 상태 추적
    stats = {
        'exploration_rate': 0,
        'collisions': 0,
        'avg_speed': 0,
        'step_data': []
    }
    
    # UI 요소들
    progress_bar = st.progress(0)
    status_container = st.empty()
    chart_container = st.empty()
    
    # 메인 시뮬레이션 루프
    for step in range(params['total_steps']):
        # 일시정지 확인
        if st.session_state.get('simulation_paused', False):
            status_container.warning("⏸️ 시뮬레이션 일시정지됨")
            time.sleep(0.1)
            continue
        
        # 로봇 업데이트
        step_stats = update_robots(robots, environment, slam_map, params, step)
        stats['step_data'].append(step_stats)
        
        # 시각화 업데이트
        if step % params['visualization_steps'] == 0:
            update_visualization(
                environment, slam_map, robots, 
                chart_container, step, params['total_steps']
            )
        
        # 진행률 업데이트
        progress = (step + 1) / params['total_steps']
        progress_bar.progress(progress)
        
        # 상태 정보 업데이트
        current_stats = calculate_current_stats(stats['step_data'], robots)
        stats.update(current_stats)
        st.session_state.sim_stats = stats
        
        status_container.info(f"🟢 Step {step+1}/{params['total_steps']} - 탐색률: {stats['exploration_rate']:.1f}%")
        
        # 속도 조절
        actual_interval = params['base_interval'] / speed_multiplier
        time.sleep(actual_interval / 1000)
    
    # 시뮬레이션 완료
    st.session_state.simulation_running = False
    success_message("시뮬레이션이 완료되었습니다!")
    
    # 최종 결과 저장
    st.session_state.final_results = {
        'environment': environment,
        'slam_map': slam_map,
        'robots': robots,
        'stats': stats
    }

def create_environment(grid_size, num_obstacles, max_size):
    """환경 생성"""
    environment = np.zeros((grid_size, grid_size))
    
    # 경계 벽 생성
    environment[0:3, :] = 1
    environment[-3:, :] = 1
    environment[:, 0:3] = 1
    environment[:, -3:] = 1

    # 랜덤 장애물 생성
    for _ in range(num_obstacles):
        x = random.randint(5, grid_size - max_size - 5)
        y = random.randint(5, grid_size - max_size - 5)
        size_x = random.randint(3, max_size)
        size_y = random.randint(3, max_size)
        environment[x:x + size_x, y:y + size_y] = 1

    return environment

class Robot:
    """개선된 로봇 클래스"""
    def __init__(self, x, y, theta, robot_id, safety_dist, params):
        # 기본 속성
        self.x = x
        self.y = y
        self.theta = theta
        self.id = robot_id
        self.safety_distance = safety_dist
        self.params = params
        
        # 이동 관련
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
        self.path_history = []
        self.max_path_length = 100
        
        # 상태 관리
        self.status = "Normal"
        self.stuck_count = 0
        self.collision_count = 0
        self.distance_traveled = 0
        self.exploration_area = set()
        
        # 성능 지표
        self.efficiency_score = 0
        self.last_positions = []
        
    def update_position(self, new_x, new_y):
        """위치 업데이트"""
        old_x, old_y = self.x, self.y
        self.x = new_x
        self.y = new_y
        
        # 이동 거리 계산
        distance = np.sqrt((new_x - old_x)**2 + (new_y - old_y)**2)
        self.distance_traveled += distance
        
        # 경로 기록
        self.path_history.append((self.y, self.x))
        if len(self.path_history) > self.max_path_length:
            self.path_history.pop(0)
        
        # 탐색 영역 업데이트
        grid_x, grid_y = int(self.x // 5), int(self.y // 5)
        self.exploration_area.add((grid_x, grid_y))
        
        # 위치 기록
        self.last_positions.append((new_x, new_y))
        if len(self.last_positions) > 10:
            self.last_positions.pop(0)
    
    def is_stuck(self):
        """갇힘 상태 감지"""
        if len(self.last_positions) < 5:
            return False
        
        recent_positions = self.last_positions[-5:]
        x_positions = [p[0] for p in recent_positions]
        y_positions = [p[1] for p in recent_positions]
        
        x_variance = np.var(x_positions)
        y_variance = np.var(y_positions)
        
        return (x_variance < 0.1 and y_variance < 0.1)
    
    def get_sensor_readings(self, environment):
        """센서 데이터 획득"""
        distances = []
        angles = np.linspace(-np.pi/2, np.pi/2, self.params['num_sensors'])
        
        for angle in angles:
            min_distance = self.params['sensor_range']
            theta = self.theta + angle
            
            for r in np.arange(0, self.params['sensor_range'], 0.5):
                x = int(self.y + r * np.sin(theta))
                y = int(self.x + r * np.cos(theta))
                
                if not (0 <= x < len(environment) and 0 <= y < len(environment[0])):
                    min_distance = r
                    break
                    
                if environment[x, y] == 1:
                    min_distance = r
                    break
            
            distances.append(min_distance)
        
        return distances

def initialize_robots(environment, params):
    """로봇들 초기화"""
    robots = []
    grid_size = params['grid_size']
    
    for i in range(params['num_robots']):
        attempts = 0
        while attempts < 100:  # 무한 루프 방지
            x = random.randint(10, grid_size - 10)
            y = random.randint(10, grid_size - 10)
            if environment[y, x] == 0:
                robot = Robot(x, y, random.random() * 2 * np.pi, i, 
                            params['safety_distance'], params)
                robots.append(robot)
                break
            attempts += 1
    
    return robots

def update_robots(robots, environment, slam_map, params, step):
    """모든 로봇 업데이트"""
    step_stats = {
        'total_distance': 0,
        'collisions': 0,
        'stuck_robots': 0,
        'exploration_cells': set()
    }
    
    for robot in robots:
        # 센서 데이터 획득
        distances = robot.get_sensor_readings(environment)
        
        # 간단한 자율 항법 (실제 구현은 더 복잡)
        if robot.is_stuck():
            robot.status = "Stuck"
            step_stats['stuck_robots'] += 1
            # 랜덤 회전
            robot.theta += random.uniform(-np.pi/2, np.pi/2)
        else:
            robot.status = "Normal"
            # 앞으로 이동
            front_distance = distances[len(distances)//2]
            if front_distance > params['critical_distance']:
                new_x = robot.x + params['robot_speed'] * np.cos(robot.theta)
                new_y = robot.y + params['robot_speed'] * np.sin(robot.theta)
                
                # 충돌 체크 (간단한 버전)
                if (0 < new_x < params['grid_size'] and 
                    0 < new_y < params['grid_size'] and
                    environment[int(new_y), int(new_x)] == 0):
                    robot.update_position(new_x, new_y)
                else:
                    step_stats['collisions'] += 1
                    robot.collision_count += 1
                    robot.theta += np.pi/4  # 45도 회전
            else:
                # 장애물 회피를 위한 회전
                robot.theta += np.pi/3
        
        # 통계 업데이트
        step_stats['total_distance'] += robot.distance_traveled
        step_stats['exploration_cells'].update(robot.exploration_area)
    
    return step_stats

def update_visualization(environment, slam_map, robots, container, step, total_steps):
    """시각화 업데이트"""
    # Plotly를 사용한 인터랙티브 시각화
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('실제 환경', 'SLAM 지도'),
        specs=[[{'type': 'heatmap'}, {'type': 'heatmap'}]]
    )
    
    # 실제 환경
    fig.add_trace(
        go.Heatmap(
            z=environment.T,
            colorscale='Gray',
            showscale=False
        ),
        row=1, col=1
    )
    
    # SLAM 지도
    fig.add_trace(
        go.Heatmap(
            z=slam_map.T,
            colorscale='Gray',
            showscale=False
        ),
        row=1, col=2
    )
    
    # 로봇 위치 표시
    for robot in robots:
        color = 'red' if robot.status == 'Stuck' else 'blue'
        
        # 실제 환경에 로봇 표시
        fig.add_trace(
            go.Scatter(
                x=[robot.y], y=[robot.x],
                mode='markers',
                marker=dict(size=10, color=color),
                name=f'Robot {robot.id}',
                showlegend=(robot.id == 0)  # 첫 번째 로봇만 범례 표시
            ),
            row=1, col=1
        )
        
        # SLAM 지도에 로봇 표시
        fig.add_trace(
            go.Scatter(
                x=[robot.y], y=[robot.x],
                mode='markers',
                marker=dict(size=10, color=color),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # 경로 표시
        if len(robot.path_history) > 1:
            path = np.array(robot.path_history)
            fig.add_trace(
                go.Scatter(
                    x=path[:, 0], y=path[:, 1],
                    mode='lines',
                    line=dict(color=color, width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    
    fig.update_layout(
        title=f'SLAM 시뮬레이션 - Step {step}/{total_steps}',
        height=400
    )
    
    container.plotly_chart(fig, use_container_width=True)

def calculate_current_stats(step_data, robots):
    """현재 통계 계산"""
    if not step_data:
        return {'exploration_rate': 0, 'collisions': 0, 'avg_speed': 0}
    
    latest_data = step_data[-1]
    total_cells = len(latest_data['exploration_cells'])
    grid_size = st.session_state.sim_params['grid_size']
    max_cells = (grid_size // 5) ** 2  # 5x5 그리드 단위로 계산
    
    exploration_rate = (total_cells / max_cells) * 100 if max_cells > 0 else 0
    total_collisions = sum(robot.collision_count for robot in robots)
    avg_distance = sum(robot.distance_traveled for robot in robots) / len(robots)
    
    return {
        'exploration_rate': min(100, exploration_rate),
        'collisions': total_collisions,
        'avg_speed': avg_distance / len(step_data) if step_data else 0
    }

def reset_simulation():
    """시뮬레이션 리셋"""
    keys_to_remove = [
        'simulation_running', 'simulation_paused', 
        'sim_stats', 'final_results'
    ]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    
    success_message("시뮬레이션이 리셋되었습니다.")

def display_analysis_results():
    """분석 결과 섹션"""
    st.header("📈 분석 결과")
    
    if 'final_results' not in st.session_state:
        info_message("시뮬레이션을 실행한 후 결과를 확인할 수 있습니다.")
        return
    
    results = st.session_state.final_results
    stats = results['stats']
    
    # 요약 지표
    st.subheader("📊 성능 요약")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("최종 탐색률", f"{stats['exploration_rate']:.1f}%")
    with col2:
        st.metric("총 충돌 횟수", stats['collisions'])
    with col3:
        st.metric("평균 이동 속도", f"{stats['avg_speed']:.2f}")
    with col4:
        total_distance = sum(robot.distance_traveled for robot in results['robots'])
        st.metric("총 이동 거리", f"{total_distance:.1f}")
    
    # 시간별 성능 그래프
    if stats['step_data']:
        st.subheader("📈 시간별 성능 변화")
        
        steps = list(range(len(stats['step_data'])))
        exploration_data = []
        collision_data = []
        
        cumulative_exploration = set()
        cumulative_collisions = 0
        
        for i, data in enumerate(stats['step_data']):
            cumulative_exploration.update(data['exploration_cells'])
            cumulative_collisions += data['collisions']
            
            grid_size = st.session_state.sim_params['grid_size']
            max_cells = (grid_size // 5) ** 2
            exploration_rate = (len(cumulative_exploration) / max_cells) * 100
            
            exploration_data.append(exploration_rate)
            collision_data.append(cumulative_collisions)
        
        # Plotly 그래프
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('탐색률 변화', '누적 충돌 횟수'),
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Scatter(
                x=steps, y=exploration_data,
                mode='lines',
                name='탐색률 (%)',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=steps, y=collision_data,
                mode='lines',
                name='누적 충돌',
                line=dict(color='red')
            ),
            row=2, col=1
        )
        
        fig.update_layout(height=500, showlegend=False)
        fig.update_xaxes(title_text="시뮬레이션 스텝", row=2, col=1)
        fig.update_yaxes(title_text="탐색률 (%)", row=1, col=1)
        fig.update_yaxes(title_text="충돌 횟수", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 로봇별 성능 분석
    st.subheader("🤖 로봇별 성능")
    
    robot_data = []
    for robot in results['robots']:
        robot_data.append({
            'Robot ID': robot.id,
            '이동 거리': f"{robot.distance_traveled:.2f}",
            '탐색 영역': len(robot.exploration_area),
            '충돌 횟수': robot.collision_count,
            '최종 상태': robot.status
        })
    
    robot_df = pd.DataFrame(robot_data)
    st.dataframe(robot_df, use_container_width=True)
    
    # 추가 분석 및 권장사항
    display_recommendations(results)

def display_recommendations(results):
    """성능 개선 권장사항"""
    st.subheader("💡 성능 개선 권장사항")
    
    stats = results['stats']
    params = st.session_state.sim_params
    
    recommendations = []
    
    # 탐색률 기반 권장사항
    if stats['exploration_rate'] < 50:
        recommendations.append("탐색률이 낮습니다. 센서 범위를 늘리거나 로봇 수를 증가시켜보세요.")
    
    # 충돌 기반 권장사항
    if stats['collisions'] > params['num_robots'] * 10:
        recommendations.append("충돌이 많이 발생했습니다. 안전 거리를 늘리거나 회전 민감도를 조정해보세요.")
    
    # 속도 기반 권장사항
    if stats['avg_speed'] < 1.0:
        recommendations.append("평균 속도가 낮습니다. 로봇 속도를 높이거나 장애물을 줄여보세요.")
    
    # 효율성 평가
    efficiency = (stats['exploration_rate'] / 100) * (1 - min(1, stats['collisions'] / 50))
    if efficiency < 0.5:
        recommendations.append("전체적인 효율성이 낮습니다. 매개변수 균형을 재조정해보세요.")
    
    if not recommendations:
        recommendations.append("우수한 성능입니다! 현재 설정을 유지하세요.")
    
    for rec in recommendations:
        st.write(f"• {rec}")

# 메인 실행
if __name__ == "__main__":
    robotsimulation()
