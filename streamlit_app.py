<<<<<<< HEAD
import streamlit as st
from linear_analysis import linearity_analysis
from speed_analysis import speed_analysis
from gantt_chart import gantt_chart
from gomoku_module import gomoku_game

st.set_page_config(page_title="분석 도구 및 오목 게임", layout="wide")

st.sidebar.title("도구 선택")
analysis_type = st.sidebar.radio(
    "분석 유형을 선택하세요:",
    ("3D 선형성 평가", "속도 및 가속도 분석", "프로젝트 진행 간트 차트", "오목 게임")
)
=======
# 필요한 라이브러리 설치
# pip install matplotlib
# pip install pandas
# pip install openpyxl
# pip install plotly
# pip install streamlit
# pip install xlsxwriter

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import plotly.graph_objs as go
import plotly.express as px
from io import BytesIO
import random

# Streamlit 와이드 모드 활성화
st.set_page_config(page_title="분석 도구 및 오목 게임", layout="wide")

# 사이드바에서 분석 유형 선택
st.sidebar.title("도구 선택")
analysis_type = st.sidebar.radio("분석 유형을 선택하세요:", ("3D 선형성 평가", "속도 및 가속도 분석", "프로젝트 진행 간트 차트", "오목 게임"))
>>>>>>> ca777fb1b525feb3c0e85bced88ea060f9abbef2

if analysis_type == "3D 선형성 평가":
    linearity_analysis()
elif analysis_type == "속도 및 가속도 분석":
<<<<<<< HEAD
    speed_analysis()
elif analysis_type == "프로젝트 진행 간트 차트":
    gantt_chart()
elif analysis_type == "오목 게임":
    gomoku_game()
=======
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

elif analysis_type == "프로젝트 진행 간트 차트":
    st.title("프로젝트 진행 간트 차트")

    # 파일 업로드 위젯 사용하여 엑셀 파일 업로드
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요.", type=['xlsx'], key="gantt")
    if uploaded_file is not None:
        # 엑셀 파일에서 데이터 읽기
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        except Exception as e:
            st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
            st.stop()

        # 시작 및 종료 날짜 변환
        try:
            df['Start'] = pd.to_datetime(df['Start'])
            df['End'] = pd.to_datetime(df['End'])
        except KeyError:
            st.error("엑셀 파일에 'Start' 또는 'End' 열이 없습니다. 데이터를 확인하세요.")
            st.stop()

        # 진행률 열 확인
        if 'Progress' not in df.columns:
            df['Progress'] = 0  # 진행률이 없는 경우 기본값을 0으로 설정

        # Streamlit 레이아웃 설정
        order_by = st.radio(
            "정렬 기준을 선택하세요:",
            ('Start', 'End'),
            index=0,
            horizontal=True
        )

        # 그룹핑 열 선택 (예: 팀, 카테고리 등)
        group_column = None
        if 'Group' in df.columns:
            group_column = 'Group'
            st.sidebar.title("그룹별 필터링")
            unique_groups = df['Group'].unique()
            selected_groups = st.sidebar.multiselect("그룹을 선택하세요:", options=unique_groups, default=unique_groups)
            df = df[df['Group'].isin(selected_groups)]

        # 정렬 기준에 따라 데이터프레임 정렬
        sorted_df = df.sort_values(by=order_by)

        # 간트 차트 생성 (엑셀 순서 유지, 우하향으로 구성)
        fig = px.timeline(
            sorted_df, 
            x_start="Start", 
            x_end="End", 
            y="Task", 
            title='프로젝트 진행 간트 차트', 
            color=group_column if group_column else "Task",
            text='Task',
            labels={'Task': '작업', 'Start': '시작 날짜', 'End': '종료 날짜', 'Group': '그룹'}
        )
        fig.update_yaxes(categoryorder='array', categoryarray=sorted_df['Task'])  # 엑셀 파일의 순서를 유지
        fig.update_layout(yaxis_autorange='reversed', xaxis_showgrid=True, yaxis_showgrid=True)  # 우하향으로 구성 및 격자표 추가
        fig.update_xaxes(tickformat="%y-%m-%d")  # 날짜 형식을 yy-mm-%d로 변경

        # 진행률 추가 표시
        for i, row in sorted_df.iterrows():
            fig.add_shape(
                type='rect',
                x0=row['Start'],
                x1=row['Start'] + (row['End'] - row['Start']) * row['Progress'] / 100,
                y0=i - 0.1,
                y1=i + 0.1,
                fillcolor='rgba(0, 128, 0, 0.5)',
                line=dict(width=0)
            )

        # Streamlit 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

        # 진행 상황 요약 표시
        st.subheader("진행 상황 요약")
        total_tasks = len(sorted_df)
        completed_tasks = len(sorted_df[sorted_df['Progress'] == 100])
        avg_progress = sorted_df['Progress'].mean()

        st.metric("총 작업 수", total_tasks)
        st.metric("완료된 작업 수", completed_tasks)
        st.metric("평균 진행률", f"{avg_progress:.2f}%")

        # 작업을 엑셀로 내보내기
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            sorted_df.to_excel(writer, index=False, sheet_name='Gantt Chart')
            processed_data = output.getvalue()

        st.download_button(
            label="엑셀로 내보내기",
            data=processed_data,
            file_name='project_schedule_export.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # 드래그로 수정 기능 (현재 Streamlit과 Plotly만으로는 지원되지 않음)
        st.info("작업을 드래그로 수정하는 기능은 현재 지원되지 않습니다. 대신 엑셀에서 직접 수정하거나 입력된 데이터를 수정해 주세요.")
    else:
        st.info("엑셀 파일을 업로드해 주세요.")

elif analysis_type == "오목 게임":
    st.title("오목 게임 (Gomoku)")

    BOARD_SIZE = 15

    def init_board():
        return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def count_consecutive_stones(board, x, y, dx, dy, player):
        count = 0
        nx, ny = x + dx, y + dy
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == player:
            count += 1
            nx += dx
            ny += dy
        return count

    def evaluate_position(board, x, y, player):
        if board[x][y] != '.':
            return -1

        directions = [
            [(0, 1), (0, -1)],  # 가로
            [(1, 0), (-1, 0)],  # 세로
            [(1, 1), (-1, -1)], # 대각선 \
            [(1, -1), (-1, 1)]  # 대각선 /
        ]
        
        score = 0
        for dir_pair in directions:
            stones = 1
            space_before = 0
            space_after = 0
            
            for dx, dy in dir_pair:
                count = count_consecutive_stones(board, x, y, dx, dy, player)
                stones += count
                
                nx, ny = x + dx * (count + 1), y + dy * (count + 1)
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == '.':
                    if dx == dir_pair[0][0] and dy == dir_pair[0][1]:
                        space_before = 1
                    else:
                        space_after = 1

            if stones >= 5:
                score += 100000
            elif stones == 4 and (space_before + space_after) >= 1:
                score += 10000
            elif stones == 3 and (space_before + space_after) == 2:
                score += 1000
            elif stones == 2 and (space_before + space_after) == 2:
                score += 100
            elif stones == 1 and (space_before + space_after) == 2:
                score += 10

        return score

    def ai_move(board, difficulty):
        empty_positions = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == '.':
                    attack_score = evaluate_position(board, i, j, '⚫')
                    defense_score = evaluate_position(board, i, j, '⚪')
                    
                    if difficulty == "쉬움":
                        score = attack_score * 0.3 + defense_score * 0.3
                    elif difficulty == "중간":
                        score = attack_score * 0.7 + defense_score * 0.7
                    else:
                        score = attack_score + defense_score
                    
                    if difficulty == "쉬움":
                        score = score * random.uniform(0.1, 1.0)
                    elif difficulty == "중간":
                        score = score * random.uniform(0.5, 1.0)
                    
                    empty_positions.append((score, i, j))
        
        if empty_positions:
            empty_positions.sort(reverse=True)
            max_score = empty_positions[0][0]
            best_positions = []
            for score, i, j in empty_positions:
                if score >= max_score * 0.9:
                    best_positions.append((i, j))
                else:
                    break
            return random.choice(best_positions)
        return None

    def check_winner(board, x, y, player):
        directions = [
            [(0, 1), (0, -1)],  # 가로
            [(1, 0), (-1, 0)],  # 세로
            [(1, 1), (-1, -1)], # 대각선 \
            [(1, -1), (-1, 1)]  # 대각선 /
        ]
        
        for dir_pair in directions:
            count = 1
            for dx, dy in dir_pair:
                nx, ny = x, y
                while True:
                    nx += dx
                    ny += dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == player:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False

    def play_game():
        if 'game_mode' not in st.session_state:
            st.session_state.game_mode = 'pvp'
        if 'difficulty' not in st.session_state:
            st.session_state.difficulty = '중간'

        with st.sidebar:
            game_mode = st.radio(
                "게임 모드 선택",
                ('플레이어 vs 플레이어', '플레이어 vs AI'),
                key='game_mode_radio'
            )
            st.session_state.game_mode = 'pvp' if game_mode == '플레이어 vs 플레이어' else 'pvc'
            
            if st.session_state.game_mode == 'pvc':
                difficulty = st.select_slider(
                    "AI 난이도",
                    options=["쉬움", "중간", "어려움"],
                    value=st.session_state.difficulty
                )
                st.session_state.difficulty = difficulty
                
                st.write("난이도 설명:")
                st.write("- 쉬움: AI가 실수를 자주 하며, 공격과 수비를 잘 하지 못합니다.")
                st.write("- 중간: AI가 기본적인 전략을 사용하며, 때때로 좋은 수를 찾습니다.")
                st.write("- 어려움: AI가 공격과 수비를 적극적으로 하며, 최적의 수를 찾으려 합니다.")

        with st.sidebar.expander("게임 규칙"):
            st.write("""
            - 흑돌(⚫)이 먼저 시작합니다
            - 플레이어는 번갈아가며 돌을 놓습니다
            - 가로, 세로, 대각선으로 5개의 돌을 연속으로 놓으면 승리합니다
            - 빈 칸을 클릭하여 돌을 놓을 수 있습니다
            """)
        
        players = ['⚫', '⚪']
        
        if 'board' not in st.session_state:
            st.session_state.board = init_board()
            st.session_state.turn = 0
            st.session_state.winner = None
        
        board = st.session_state.board
        turn = st.session_state.turn
        player = players[turn % 2]

        if st.session_state.winner is None:
            if st.session_state.game_mode == 'pvc' and player == '⚪':
                st.markdown(f"### 현재 차례: AI (백돌) - 난이도: {st.session_state.difficulty}")
            else:
                st.markdown(f"### 현재 차례: {'흑돌' if player == '⚫' else '백돌'}")
            
            st.markdown("""
            <style>
            div.stButton > button {
                width: 45px;
                height: 45px;
                padding: 0px;
                font-size: 24px;
                font-weight: bold;
                border-radius: 50%;
                margin: 1px;
            }
            div.stButton > button:disabled {
                color: inherit;
                background-color: inherit;
            }
            div.stButton > button[data-value='⚫'] {
                color: black !important;
                background-color: white !important;
            }
            div.stButton > button[data-value='⚪'] {
                color: white !important;
                background-color: black !important;
            }
            div.row-widget.stButton {
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)
            
            game_board = st.container()
            
            with game_board:
                for i in range(BOARD_SIZE):
                    cols = st.columns(BOARD_SIZE)
                    for j in range(BOARD_SIZE):
                        if board[i][j] == '.':
                            if cols[j].button("", key=f"{i}-{j}"):
                                board[i][j] = player
                                if check_winner(board, i, j, player):
                                    st.session_state.winner = player
                                else:
                                    st.session_state.turn += 1
                                    if (st.session_state.game_mode == 'pvc' and 
                                        st.session_state.winner is None and 
                                        st.session_state.turn % 2 == 1):
                                        ai_pos = ai_move(board, st.session_state.difficulty)
                                        if ai_pos:
                                            ai_i, ai_j = ai_pos
                                            board[ai_i][ai_j] = '⚪'
                                            if check_winner(board, ai_i, ai_j, '⚪'):
                                                st.session_state.winner = '⚪'
                                            st.session_state.turn += 1
                                st.rerun()
                        else:
                            cols[j].button(
                                board[i][j], 
                                key=f"{i}-{j}", 
                                disabled=True,
                                kwargs={'data-value': board[i][j]}
                            )
        
        if st.session_state.winner is not None:
            winner_text = f"AI ({st.session_state.difficulty})" if st.session_state.winner == '⚪' and st.session_state.game_mode == 'pvc' else f"{'흑돌' if st.session_state.winner == '⚫' else '백돌'}"
            st.success(f"🎉 {winner_text} 승리! 🎉")
            if st.button("새 게임 시작", key="restart"):
                del st.session_state.board
                del st.session_state.turn
                del st.session_state.winner
                st.rerun()

    if __name__ == "__main__":
        play_game()
>>>>>>> ca777fb1b525feb3c0e85bced88ea060f9abbef2
