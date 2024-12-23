import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
import random

# Streamlit 기본 설정
# st.set_page_config(layout="wide")

def robotsimulation():
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
            
            # 새로운 파라미터 추가
            st.subheader("Navigation Parameters")
            safety_distance = st.slider("Safety Distance", 2, 8, 3, help="Minimum distance from obstacles")
            critical_distance = st.slider("Critical Distance", 3, 10, 5, help="Distance to start avoiding obstacles")
            turn_sensitivity = st.slider("Turn Sensitivity", 0.1, 1.0, 0.5, help="How aggressively robot turns")

        with col3:
            st.subheader("Simulation Parameters")
            total_steps = st.slider("Simulation Steps", 200, 1000, 500)
            update_interval = st.slider("Update Interval (ms)", 10, 100, 20)
            visualization_steps = st.slider("Visualization Update Frequency", 1, 10, 5)
            
            # SLAM 파라미터
            st.subheader("SLAM Parameters")
            confidence_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.7, 
                                        help="Minimum confidence for updating SLAM map")
            decay_factor = st.slider("Memory Decay Factor", 0.9, 1.0, 0.95, 
                                help="How much to retain previous observations")

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
            self.x = x
            self.y = y
            self.theta = theta
            self.id = id
            self.color = plt.cm.tab10(id / num_robots)
            self.safety_distance = safety_dist
            self.last_positions = []
            self.stuck_count = 0
            self.previous_direction = None

        def move(self, distance, rotation, environment):
            rotation = np.clip(rotation, -np.pi/2, np.pi/2)
            self.theta += rotation
            self.theta = self.theta % (2 * np.pi)

            new_x = self.x + distance * np.cos(self.theta)
            new_y = self.y + distance * np.sin(self.theta)

            new_x = np.clip(new_x, 3 + self.safety_distance, grid_size - 3 - self.safety_distance)
            new_y = np.clip(new_y, 3 + self.safety_distance, grid_size - 3 - self.safety_distance)

            if not self.check_collision(new_x, new_y, environment):
                old_x, old_y = self.x, self.y
                self.x = new_x
                self.y = new_y
                
                movement = np.sqrt((self.x - old_x)**2 + (self.y - old_y)**2)
                if movement < 0.1:
                    self.stuck_count += 1
                else:
                    self.stuck_count = 0

                self.last_positions.append((new_x, new_y))
                if len(self.last_positions) > 10:
                    self.last_positions.pop(0)
                    
                return True
            return False

        def check_collision(self, new_x, new_y, environment):
            robot_radius = self.safety_distance
            x_min = int(max(0, new_y - robot_radius))
            x_max = int(min(grid_size, new_y + robot_radius + 1))
            y_min = int(max(0, new_x - robot_radius))
            y_max = int(min(grid_size, new_x + robot_radius + 1))

            check_area = environment[x_min:x_max, y_min:y_max]
            return np.any(check_area == 1)

        def is_stuck(self):
            return self.stuck_count > 5 or (
                len(self.last_positions) >= 5 and
                np.var([p[0] for p in self.last_positions[-5:]]) < 0.2 and
                np.var([p[1] for p in self.last_positions[-5:]]) < 0.2
            )

    def measure_distance(environment, robot, sensor_range):
        distances = []
        angles = np.linspace(-np.pi/2, np.pi/2, num_sensors)
        sensor_readings = []  # SLAM을 위한 센서 데이터 저장
        
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
        # 기존 맵의 값들을 감쇄
        slam_map = slam_map * decay_factor
        
        # 센서 데이터를 기반으로 맵 업데이트
        for distance, theta, hit_point in sensor_readings:
            if distance < sensor_range:  # 센서 범위 내의 데이터만 사용
                x, y = hit_point
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    confidence = 1.0 - (distance / sensor_range)  # 거리에 따른 신뢰도 계산
                    if confidence > confidence_threshold:
                        slam_map[x, y] = min(1.0, slam_map[x, y] + confidence * 0.1)
                        
                        # 로봇과 장애물 사이의 공간은 비어있음을 표시
                        robot_x = int(robot.y)
                        robot_y = int(robot.x)
                        for alpha in np.linspace(0, 1, 20):
                            free_x = int(robot_x + alpha * (x - robot_x))
                            free_y = int(robot_y + alpha * (y - robot_y))
                            if 0 <= free_x < grid_size and 0 <= free_y < grid_size:
                                slam_map[free_x, free_y] *= 0.95
        
        return slam_map

    def autonomous_navigation(robot, distances, speed, critical_dist, turn_sense, environment):
        front_idx = len(distances) // 2
        front_sector = distances[front_idx-1:front_idx+2]
        left_sector = distances[:len(distances)//3]
        right_sector = distances[-len(distances)//3:]
        
        front_dist = np.mean(front_sector)
        left_dist = np.mean(left_sector)
        right_dist = np.mean(right_sector)
        
        move_speed = speed
        turn_angle = 0
        
        if robot.is_stuck():
            move_speed = speed * 0.5
            if robot.previous_direction is None:
                robot.previous_direction = 1 if left_dist > right_dist else -1
            turn_angle = robot.previous_direction * np.pi/2 * turn_sense
        else:
            if front_dist < critical_dist:
                move_speed *= (front_dist / critical_dist)
                
                if left_dist > right_dist:
                    turn_angle = np.pi/3 * turn_sense
                    robot.previous_direction = 1
                else:
                    turn_angle = -np.pi/3 * turn_sense
                    robot.previous_direction = -1
                    
                if front_dist < robot.safety_distance:
                    move_speed = -speed * 0.3
                    turn_angle *= 1.5
            else:
                robot.previous_direction = None
                turn_angle = np.random.uniform(-0.1, 0.1) * turn_sense
        
        return robot.move(move_speed, turn_angle, environment)

    # Simulation 탭에서 실행되는 메인 시뮬레이션
    with tab_simulation:
        if st.button("Start Simulation"):
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

            for step in range(total_steps):
                for robot in robots:
                    distances, sensor_readings = measure_distance(environment, robot, sensor_range)
                    moved = autonomous_navigation(robot, distances, robot_speed, 
                                            critical_distance, turn_sensitivity, environment)
                    
                    # SLAM 맵 업데이트
                    if moved:
                        slam_map = update_slam_map(slam_map, robot, sensor_readings, 
                                                confidence_threshold, decay_factor)

                if step % visualization_steps == 0:
                    ax1.clear()
                    ax2.clear()

                    ax1.imshow(environment.T, cmap="gray", origin="lower")
                    ax1.set_title("Real Environment")

                    ax2.imshow(slam_map.T, cmap="gray", origin="lower")
                    ax2.set_title("SLAM Map")

                    for robot in robots:
                        # 로봇 위치 표시
                        ax1.plot(robot.y, robot.x, "o", color=robot.color, markersize=10)
                        ax2.plot(robot.y, robot.x, "o", color=robot.color, markersize=10)
                        
                        # 로봇 방향 표시
                        direction_x = robot.x + 5 * np.cos(robot.theta)
                        direction_y = robot.y + 5 * np.sin(robot.theta)
                        ax1.plot([robot.y, direction_y], [robot.x, direction_x], 
                                color=robot.color, linewidth=2)
                        ax2.plot([robot.y, direction_y], [robot.x, direction_x], 
                                color=robot.color, linewidth=2)

                    placeholder.pyplot(fig)
                    progress_bar.progress(step / total_steps)

                time.sleep(update_interval / 1000)

            st.success("Simulation completed!")
