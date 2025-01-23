import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
import random

def robotsimulation02():
    st.title("Multi-Robot SLAM Simulation")

    # 탭 구성
    tab_params, tab_simulation = st.tabs(["Parameters", "Simulation"])

    # Parameters 탭 설정
    with tab_params:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Environment Parameters")
            grid_size = st.slider("Grid Size", 50, 200, 100)
            num_obstacles = st.slider("Number of Random Obstacles", 5, 30, 15)
            obstacle_size = st.slider("Max Obstacle Size", 3, 15, 8)

        with col2:
            st.subheader("Robot Parameters")
            num_robots = st.slider("Number of Robots", 1, 5, 2)
            sensor_range = st.slider("Sensor Range", 10, 50, 30)
            num_sensors = st.slider("Number of Sensors", 5, 15, 9)
            robot_speed = st.slider("Robot Speed", 1, 5, 3)
            
            st.subheader("Navigation Parameters")
            safety_distance = st.slider("Safety Distance", 2, 8, 3, help="Minimum distance from obstacles")
            critical_distance = st.slider("Critical Distance", 3, 10, 5, help="Distance to start avoiding obstacles")
            turn_sensitivity = st.slider("Turn Sensitivity", 0.1, 1.0, 0.5, help="How aggressively robot turns")

        with col3:
            st.subheader("Simulation Parameters")
            total_steps = st.slider("Simulation Steps", 200, 10000000000, 200)
            base_interval = st.slider("Base Update Interval (ms)", 10, 100, 20)
            visualization_steps = st.slider("Visualization Update Frequency", 1, 10, 5)
            
            st.subheader("SLAM Parameters")
            confidence_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.7)
            decay_factor = st.slider("Memory Decay Factor", 0.9, 1.0, 0.95)

    def create_environment(grid_size, num_obstacles, max_size):
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
        def __init__(self, x, y, theta, id, safety_dist):
            # 기본 속성
            self.x = x
            self.y = y
            self.theta = theta
            self.id = id
            self.color = plt.cm.tab10(id / num_robots)
            self.safety_distance = safety_dist
            
            # 이동 관련 속성
            self.velocity = np.zeros(2)
            self.acceleration = np.zeros(2)
            self.last_positions = []
            self.path_history = []
            self.max_path_length = 50
            
            # stuck 상태 관련
            self.stuck_count = 0
            self.previous_direction = None
            self.movement_threshold = 0.15
            self.stuck_threshold = 3
            self.position_history_size = 7
            self.variance_threshold = 0.15
            
            # 상태 모니터링
            self.status = "Normal"
            self.time_in_status = 0
            self.escape_attempts = 0
            self.last_successful_move_time = 0
            self.detection_zone = []
            self.decision_zone = []

        def update_status(self, current_time):
            if self.is_stuck():
                if self.status != "Stuck":
                    self.status = "Stuck"
                    self.time_in_status = 0
                    self.escape_attempts += 1
                else:
                    self.time_in_status += 1
                    
                if self.time_in_status > 50:
                    self.status = "Emergency_Escape"
            else:
                if self.status != "Normal":
                    self.status = "Normal"
                    self.time_in_status = 0
                else:
                    self.time_in_status += 1

        def calculate_detection_zones(self):
            self.detection_zone = []
            self.decision_zone = []
            
            # 센서 감지 영역 (부채꼴 모양)
            angles = np.linspace(self.theta - np.pi/2, self.theta + np.pi/2, 20)
            for r in np.arange(0, sensor_range, 2):
                for angle in angles:
                    x = int(self.y + r * np.sin(angle))
                    y = int(self.x + r * np.cos(angle))
                    if 0 <= x < grid_size and 0 <= y < grid_size:
                        self.detection_zone.append((x, y))
                        
            # 의사결정 영역 (로봇 주변 원형)
            for angle in np.linspace(0, 2*np.pi, 30):
                for r in np.arange(0, critical_distance, 1):
                    x = int(self.y + r * np.sin(angle))
                    y = int(self.x + r * np.cos(angle))
                    if 0 <= x < grid_size and 0 <= y < grid_size:
                        self.decision_zone.append((x, y))

        def is_stuck(self):
            if self.stuck_count > self.stuck_threshold:
                return True
                    
            if len(self.last_positions) >= self.position_history_size:
                recent_positions = self.last_positions[-self.position_history_size:]
                x_positions = [p[0] for p in recent_positions]
                y_positions = [p[1] for p in recent_positions]
                
                x_variance = np.var(x_positions)
                y_variance = np.var(y_positions)
                
                total_distance = sum(np.sqrt((x_positions[i+1] - x_positions[i])**2 + 
                                        (y_positions[i+1] - y_positions[i])**2) 
                                for i in range(len(x_positions)-1))
                
                return (x_variance < self.variance_threshold and 
                        y_variance < self.variance_threshold) or \
                    (total_distance < self.movement_threshold * self.position_history_size)
            
            return False

        def check_collision(self, new_x, new_y, environment, robots):
            boundary_margin = self.safety_distance + 2
            if (new_x < boundary_margin or new_x > grid_size - boundary_margin or
                new_y < boundary_margin or new_y > grid_size - boundary_margin):
                return True

            robot_radius = self.safety_distance
            x_min = int(max(0, new_y - robot_radius))
            x_max = int(min(grid_size, new_y + robot_radius + 1))
            y_min = int(max(0, new_x - robot_radius))
            y_max = int(min(grid_size, new_x + robot_radius + 1))

            if x_min >= x_max or y_min >= y_max:
                return True

            check_area = environment[x_min:x_max, y_min:y_max]
            if np.any(check_area == 1):
                return True

            for robot in robots:
                if robot.id != self.id:
                    dist = np.sqrt((new_x - robot.x)**2 + (new_y - robot.y)**2)
                    if dist < (self.safety_distance + robot.safety_distance):
                        return True

            return False

        def move(self, distance, rotation, environment, robots):
            rotation = np.clip(rotation, -np.pi * 0.8, np.pi * 0.8)
            self.theta += rotation
            self.theta = self.theta % (2 * np.pi)

            target_velocity = np.array([
                distance * np.cos(self.theta),
                distance * np.sin(self.theta)
            ])

            repulsive_force = np.zeros(2)
            for robot in robots:
                if robot.id != self.id:
                    diff = np.array([self.x - robot.x, self.y - robot.y])
                    dist = np.linalg.norm(diff)
                    if dist < self.safety_distance * 4:
                        force_magnitude = (1.0 / dist**2) * 2.0
                        repulsive_force += (diff / dist) * force_magnitude

            boundary_force = np.zeros(2)
            boundary_margin = self.safety_distance * 3
            
            if self.x < boundary_margin:
                boundary_force[0] += 1.0 / (self.x + 1)**2
            elif self.x > grid_size - boundary_margin:
                boundary_force[0] -= 1.0 / (grid_size - self.x + 1)**2
                
            if self.y < boundary_margin:
                boundary_force[1] += 1.0 / (self.y + 1)**2
            elif self.y > grid_size - boundary_margin:
                boundary_force[1] -= 1.0 / (grid_size - self.y + 1)**2

            self.acceleration = (target_velocity - self.velocity) * 0.1 + repulsive_force + boundary_force
            self.velocity += self.acceleration
            self.velocity *= 0.9

            new_x = self.x + self.velocity[0]
            new_y = self.y + self.velocity[1]

            if not self.check_collision(new_x, new_y, environment, robots):
                old_x, old_y = self.x, self.y
                self.x = new_x
                self.y = new_y
                
                self.path_history.append((self.y, self.x))
                if len(self.path_history) > self.max_path_length:
                    self.path_history.pop(0)

                movement = np.sqrt((self.x - old_x)**2 + (self.y - old_y)**2)
                if movement < self.movement_threshold:
                    self.stuck_count += 1
                else:
                    self.stuck_count = 0

                self.last_positions.append((new_x, new_y))
                if len(self.last_positions) > 10:
                    self.last_positions.pop(0)
                    
                return True
            return False

    def measure_distance(environment, robot, sensor_range):
        distances = []
        angles = np.linspace(-np.pi/2, np.pi/2, num_sensors)
        sensor_readings = []
        
        for angle in angles:
            min_distance = sensor_range
            theta = robot.theta + angle
            hit_point = None
            
            for r in np.arange(0, sensor_range, 0.3):
                x = int(robot.y + r * np.sin(theta))
                y = int(robot.x + r * np.cos(theta))
                
                if not (0 <= x < grid_size and 0 <= y < grid_size):
                    min_distance = r
                    hit_point = (x, y)
                    break
                    
                if environment[x, y] == 1:
                    min_distance = r
                    hit_point = (x, y)
                    break
            
            distances.append(min_distance)
            if hit_point:
                sensor_readings.append((min_distance, theta, hit_point))
        
        return distances, sensor_readings

    def update_slam_map(slam_map, robot, sensor_readings, confidence_threshold, decay_factor):
        slam_map = slam_map * decay_factor
        
        for distance, theta, hit_point in sensor_readings:
            if distance < sensor_range:
                x, y = hit_point
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    confidence = 1.0 - (distance / sensor_range)
                    if confidence > confidence_threshold:
                        slam_map[x, y] = min(1.0, slam_map[x, y] + confidence * 0.1)
                        
                        robot_x = int(robot.y)
                        robot_y = int(robot.x)
                        for alpha in np.linspace(0, 1, 20):
                            free_x = int(robot_x + alpha * (x - robot_x))
                            free_y = int(robot_y + alpha * (y - robot_y))
                            if 0 <= free_x < grid_size and 0 <= free_y < grid_size:
                                slam_map[free_x, free_y] *= 0.95
        
        return slam_map

    def emergency_escape_behavior(robot, environment, robots):
        escape_directions = []
        for angle in np.linspace(0, 2*np.pi, 16):
            distance = 0
            for r in range(1, int(sensor_range)):
                x = int(robot.x + r * np.cos(angle))
                y = int(robot.y + r * np.sin(angle))
                if not (0 <= x < grid_size and 0 <= y < grid_size) or environment[x, y] == 1:
                    break
                distance = r
            escape_directions.append((angle, distance))
        
        best_direction = max(escape_directions, key=lambda x: x[1])
        turn_angle = best_direction[0] - robot.theta
        return robot.move(robot_speed * 2, turn_angle, environment, robots)

    def autonomous_navigation(robot, distances, speed, critical_dist, turn_sense, environment, robots):
            front_idx = len(distances) // 2
            front_sector = distances[front_idx-1:front_idx+2]
            left_sector = distances[:len(distances)//3]
            right_sector = distances[-len(distances)//3:]
            
            front_dist = np.mean(front_sector)
            left_dist = np.mean(left_sector)
            right_dist = np.mean(right_sector)
            
            move_speed = speed
            turn_angle = 0
            
            detection_distance = critical_dist * 3.0

            nearby_robots = [r for r in robots if r.id != robot.id]
            for other_robot in nearby_robots:
                rel_x = other_robot.x - robot.x
                rel_y = other_robot.y - robot.y
                dist = np.sqrt(rel_x**2 + rel_y**2)
                
                if dist < detection_distance:
                    angle_to_robot = np.arctan2(rel_y, rel_x)
                    angle_diff = (angle_to_robot - robot.theta + np.pi) % (2 * np.pi) - np.pi
                    
                    if abs(angle_diff) < np.pi/2:
                        move_speed *= 0.2
                        turn_angle = np.sign(angle_diff) * np.pi * 0.8 * turn_sense
                        if dist < critical_dist:
                            move_speed = -speed

            # Stuck 상태 처리 개선
            if robot.is_stuck():
                # 랜덤한 탐색 방향 설정
                if robot.previous_direction is None:
                    turn_angle = np.random.uniform(-np.pi, np.pi)
                else:
                    turn_angle = robot.previous_direction + np.random.uniform(-np.pi/2, np.pi/2)
                
                # 후진 거리를 동적으로 조절
                reverse_distance = min(distances) if min(distances) < critical_dist else critical_dist
                move_speed = -speed * (1.0 + reverse_distance/critical_dist)
                
                # 장애물이 적은 방향으로 회전
                if left_dist > right_dist * 1.2:
                    turn_angle = np.pi/2 * turn_sense
                elif right_dist > left_dist * 1.2:
                    turn_angle = -np.pi/2 * turn_sense
                
                # 연속된 stuck 상태에서 더 과감한 행동
                if robot.stuck_count > 5:
                    move_speed *= 1.5
                    turn_angle *= 1.5
                
                # 이전 위치들을 고려한 탈출 방향 설정
                if len(robot.last_positions) > 3:
                    last_x = [pos[0] for pos in robot.last_positions[-3:]]
                    last_y = [pos[1] for pos in robot.last_positions[-3:]]
                    escape_x = 2 * robot.x - np.mean(last_x)
                    escape_y = 2 * robot.y - np.mean(last_y)
                    escape_angle = np.arctan2(escape_y - robot.y, escape_x - robot.x)
                    turn_angle = escape_angle - robot.theta

                robot.previous_direction = turn_angle
                
            else:
                # 일반적인 장애물 회피 로직
                if front_dist < detection_distance:
                    distance_factor = max(0.1, (front_dist / detection_distance) ** 2)
                    move_speed *= distance_factor
                    
                    if left_dist > right_dist * 1.5:
                        turn_angle = np.pi * 0.7 * turn_sense
                    elif right_dist > left_dist * 1.5:
                        turn_angle = -np.pi * 0.7 * turn_sense
                    else:
                        turn_angle = np.pi * turn_sense
                        move_speed *= 0.5
                    
                    if front_dist < robot.safety_distance * 1.5:
                        move_speed = -speed * 0.7
                        turn_angle *= 1.5
                else:
                    min_dist = min(distances)
                    if min_dist < critical_dist * 2:
                        turn_angle = np.random.uniform(-np.pi/3, np.pi/3) * turn_sense

            # 최종 움직임 실행 전 보정
            turn_angle = np.clip(turn_angle, -np.pi, np.pi)
            move_speed = np.clip(move_speed, -speed * 1.5, speed * 1.5)
        
            return robot.move(move_speed, turn_angle, environment, robots)
    

# Simulation 탭에서 실행되는 메인 시뮬레이션
    with tab_simulation:
        # 시뮬레이션 제어 영역
        control_col1, control_col2, control_col3 = st.columns([1, 2, 1])
        
        with control_col1:
            start_button = st.button("Start Simulation")
        
        with control_col2:
            # 속도 조절 슬라이더 (0.1x ~ 5x)
            speed_multiplier = st.slider("Simulation Speed", 0.1, 5.0, 1.0, 0.1,
                                       help="Adjust simulation speed (1.0 = normal speed)")
        
        with control_col3:
            # 일시정지 버튼 추가
            pause_button = st.button("Pause/Resume")

        if start_button:
            # 시뮬레이션 상태 초기화
            if 'simulation_paused' not in st.session_state:
                st.session_state.simulation_paused = False
            
            environment = create_environment(grid_size, num_obstacles, obstacle_size)
            slam_map = np.zeros_like(environment)
            
            robots = []
            for i in range(num_robots):
                while True:
                    x = random.randint(10, grid_size - 10)
                    y = random.randint(10, grid_size - 10)
                    if environment[y, x] == 0:
                        robots.append(Robot(x, y, random.random() * 2 * np.pi, i, safety_distance))
                        break

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            placeholder = st.empty()
            progress_bar = st.progress(0)
            
            # 일시정지 상태 표시
            # status_text = st.empty()
            status_container = st.empty()




            for step in range(total_steps):
                # 일시정지 버튼 상태 확인
                if pause_button:
                    st.session_state.simulation_paused = not st.session_state.simulation_paused
                
                # 일시정지 상태 표시
                if st.session_state.simulation_paused:
                #     status_text.warning("Simulation Paused")
                #     continue
                    status_container.warning("Simulation Paused")
                    continue
                # else:
                #     status_text.info("Simulation Running")
                else:
                    status_container.info("Simulation Running")


                for robot in robots:
                    robot.update_status(step)
                    distances, sensor_readings = measure_distance(environment, robot, sensor_range)
                    
                    if robot.status == "Emergency_Escape":
                        moved = emergency_escape_behavior(robot, environment, robots)
                    else:
                        moved = autonomous_navigation(robot, distances, robot_speed, 
                                                   critical_distance, turn_sensitivity, 
                                                   environment, robots)
                    
                    if moved:
                        slam_map = update_slam_map(
                            slam_map, 
                            robot, 
                            sensor_readings, 
                            confidence_threshold, 
                            decay_factor
                        )

                if step % visualization_steps == 0:
                    ax1.clear()
                    ax2.clear()

                    # 기본 환경과 SLAM 맵 표시
                    ax1.imshow(environment.T, cmap="gray", origin="lower")
                    ax2.imshow(slam_map.T, cmap="gray", origin="lower")
                    
                    ax1.set_title("Real Environment")
                    ax2.set_title("SLAM Map")

                    for robot in robots:
                        # 감지 영역과 의사결정 영역 표시
                        robot.calculate_detection_zones()
                        
                        # 감지 영역 표시 (반투명 파란색)
                        for x, y in robot.detection_zone:
                            ax1.plot(x, y, ',', color='blue', alpha=0.1)
                            
                        # 의사결정 영역 표시 (반투명 녹색)
                        for x, y in robot.decision_zone:
                            ax1.plot(x, y, ',', color='green', alpha=0.1)

                        # 로봇 상태에 따른 색상 설정
                        status_colors = {
                            "Normal": robot.color,
                            "Stuck": "red",
                            "Emergency_Escape": "orange"
                        }
                        robot_color = status_colors.get(robot.status, robot.color)
                        
                        # 로봇 위치 및 방향 표시
                        ax1.plot(robot.y, robot.x, "o", color=robot_color, markersize=10)
                        ax2.plot(robot.y, robot.x, "o", color=robot_color, markersize=10)
                        
                        direction_x = robot.x + 5 * np.cos(robot.theta)
                        direction_y = robot.y + 5 * np.sin(robot.theta)
                        ax1.plot([robot.y, direction_y], [robot.x, direction_x], 
                                color=robot_color, linewidth=2)
                        ax2.plot([robot.y, direction_y], [robot.x, direction_x], 
                                color=robot_color, linewidth=2)

                        # 이동 경로 표시
                        if len(robot.path_history) > 1:
                            path = np.array(robot.path_history)
                            ax1.plot(path[:, 0], path[:, 1], '-', 
                                   color=robot_color, alpha=0.5, linewidth=1)
                            ax2.plot(path[:, 0], path[:, 1], '-', 
                                   color=robot_color, alpha=0.5, linewidth=1)

                        # 상태 정보 표시
                        robot_status_text = (  # status_text 대신 robot_status_text 사용
                            f'Robot {robot.id}:\n'
                            f'Status: {robot.status}\n'
                            f'Time in status: {robot.time_in_status}\n'
                            f'Escape attempts: {robot.escape_attempts}\n'
                            f'Speed: {np.linalg.norm(robot.velocity):.2f}'
                        )
                        ax1.text(5, grid_size - 15 - (robot.id * 25), 
                                robot_status_text, color=robot_color, fontsize=8)

                    ax1.set_xlim(0, grid_size)
                    ax1.set_ylim(0, grid_size)
                    ax2.set_xlim(0, grid_size)
                    ax2.set_ylim(0, grid_size)

                    placeholder.pyplot(fig)
                    progress_bar.progress(step / total_steps)

                # 속도 조절 적용
                actual_interval = base_interval / speed_multiplier
                time.sleep(actual_interval / 1000)

            st.success("Simulation completed!")
