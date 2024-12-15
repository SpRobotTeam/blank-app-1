import streamlit as st
from linear_analysis import linearity_analysis
from speed_analysis import speed_analysis
from gantt_chart import gantt_chart
from gomoku_module import gomoku_game
from AmphibiousTrainDevelopment import display_amphibious_train_project
import json
import os
import pandas as pd
from datetime import datetime

# JSON 파일 경로 설정
DATA_FILE = "posts.json"

# 데이터 저장 함수
def save_posts_to_file():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(st.session_state.posts, file, ensure_ascii=False, indent=4)

# 데이터 로드 함수
def load_posts_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []  # 파일이 없으면 빈 리스트 반환

# 게시판 데이터 초기화
if "posts" not in st.session_state:
    st.session_state.posts = load_posts_from_file()

# 게시글 추가 함수
def add_post(title, content):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.posts.append({"title": title, "content": content, "time": current_time})
    save_posts_to_file()  # 데이터 저장

# 게시글 삭제 함수
def delete_post(index):
    st.session_state.posts.pop(index)
    save_posts_to_file()  # 데이터 저장


# 페이지 설정
st.set_page_config(page_title="분석 도구 및 오목 게임", layout="wide")


# 사이드바 메뉴
st.sidebar.title("도구 선택")
analysis_type = st.sidebar.radio(
    "분석 유형을 선택하세요:",
    (
        "3D 선형성 평가", 
        "속도 및 가속도 분석", 
        "프로젝트 진행 간트 차트", 
        "오목 게임",
        "수륙 양용 기차",
        "게시판"  # 게시판 메뉴 추가
     )
)

# 각 기능 실행
if analysis_type == "3D 선형성 평가":
    linearity_analysis()
elif analysis_type == "속도 및 가속도 분석":
    speed_analysis()
elif analysis_type == "프로젝트 진행 간트 차트":
    gantt_chart()
elif analysis_type == "오목 게임":
    gomoku_game()
elif analysis_type == "수륙 양용 기차":
    display_amphibious_train_project()
elif analysis_type == "게시판":
    st.title("📋 게시판")
    
    # 탭 설정
    tab1, tab2, tab3, tab4 = st.tabs(["작성", "보기", "삭제", "수정"])
    
    # 탭 1: 작성
    with tab1:
        st.subheader("게시글 작성")
        with st.form("post_form"):
            title = st.text_input("제목", placeholder="게시글 제목을 입력하세요.")
            content = st.text_area("내용", placeholder="게시글 내용을 입력하세요.")
            submitted = st.form_submit_button("작성")
            
            if submitted:
                if title and content:
                    add_post(title, content)
                    st.success("게시글이 작성되었습니다!")
                else:
                    st.error("제목과 내용을 모두 입력하세요!")
    
    # 탭 2: 보기
    with tab2:
        st.subheader("게시글 보기")
        if st.session_state.posts:
            df = pd.DataFrame(st.session_state.posts)
            st.dataframe(df, use_container_width=True)
            
            # 상세 보기
            selected_post = st.selectbox(
                "상세히 볼 게시글을 선택하세요:",
                options=[f"{i + 1}. {post['title']}" for i, post in enumerate(st.session_state.posts)],
                key="view_post"
            )
            if selected_post:
                index = int(selected_post.split(".")[0]) - 1
                post = st.session_state.posts[index]
                st.markdown(f"### {post['title']}")
                st.write(post["content"])
                st.write(f"**작성 시간:** {post['time']}")
        else:
            st.info("게시글이 없습니다.")
    
    # 탭 3: 삭제
    with tab3:
        st.subheader("게시글 삭제")
        if st.session_state.posts:
            for index, post in enumerate(st.session_state.posts):
                if st.button(f"삭제: {post['title']}", key=f"delete_{index}"):
                    delete_post(index)
                    st.warning(f"'{post['title']}' 게시글이 삭제되었습니다.")
                    st.experimental_rerun()  # 페이지 새로고침
        else:
            st.info("게시글이 없습니다.")
    
    # 탭 4: 수정
    with tab4:
        st.subheader("게시글 수정")
        if st.session_state.posts:
            selected_post = st.selectbox(
                "수정할 게시글을 선택하세요:",
                options=[f"{i + 1}. {post['title']}" for i, post in enumerate(st.session_state.posts)],
                key="edit_post"
            )
            if selected_post:
                index = int(selected_post.split(".")[0]) - 1
                post = st.session_state.posts[index]
                with st.form(f"edit_form_{index}"):
                    new_title = st.text_input("새 제목", value=post["title"])
                    new_content = st.text_area("새 내용", value=post["content"])
                    submitted = st.form_submit_button("수정 완료")
                    if submitted:
                        edit_post(index, new_title, new_content)
                        st.success(f"'{new_title}' 게시글이 수정되었습니다.")
                        st.experimental_rerun()
        else:
            st.info("게시글이 없습니다.")
