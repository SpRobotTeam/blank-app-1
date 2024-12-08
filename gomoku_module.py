import streamlit as st
import numpy as np
import random

BOARD_SIZE = 15

def init_board():
    """Initialize the game board."""
    return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def count_consecutive_stones(board, x, y, dx, dy, player):
    """Count consecutive stones in a given direction."""
    count = 0
    nx, ny = x + dx, y + dy
    while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == player:
        count += 1
        nx += dx
        ny += dy
    return count

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

def gomoku_game():
    """Main game loop."""
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
    gomoku_game()