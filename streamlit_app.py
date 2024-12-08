import streamlit as st
from linear_analysis import linearity_analysis
from speed_analysis import speed_analysis
from gantt_chart import gantt_chart
from gomoku_module import gomoku_game
from AmphibiousTrainDevelopment import display_amphibious_train_project

st.set_page_config(page_title="분석 도구 및 오목 게임", layout="wide")

st.sidebar.title("도구 선택")
analysis_type = st.sidebar.radio(
    "분석 유형을 선택하세요:",
    (
        "3D 선형성 평가", 
        "속도 및 가속도 분석", 
        "프로젝트 진행 간트 차트", 
        "오목 게임",
        "수륙 양용 기차"
     )
)

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

