import streamlit as st
import importlib
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 페이지 설정
st.set_page_config(
    page_title="🛠️ 다기능 분석 도구",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 로드
def load_css():
    try:
        with open('assets/style.css', 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass  # CSS 파일이 없어도 계속 진행

load_css()

# 화면 크기 감지를 위한 JavaScript 추가
st.markdown("""
<script>
    document.addEventListener('DOMContentLoaded', (event) => {
        const updateScreenWidth = () => {
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: window.innerWidth,
                    key: 'screen_width'
                }, '*');
            }
        };
        
        updateScreenWidth();
        window.addEventListener('resize', updateScreenWidth);
    });
</script>
""", unsafe_allow_html=True)

# 모듈 매핑 정의
MODULE_MAP = {
    # 분석 도구
    "3D 선형성 평가": "apps.analysis.linear_analysis:linearity_analysis",
    "속도 및 가속도 분석": "apps.analysis.speed_analysis:speed_analysis",
    
    # 시뮬레이션 도구
    "수륙 양용 기차": "apps.simulation.amphibious_train:display_amphibious_train_project",
    "로봇 자율주행 시뮬레이션": "apps.simulation.robot_simulation:robotsimulation",
    "로봇 자율주행 시뮬레이션 V2": "apps.simulation.robot_simulation_v2:robotsimulation02",
    
    # 유틸리티 도구
    "프로젝트 진행 간트 차트": "apps.utilities.gantt_chart:gantt_chart",
    "모터 용량 계산": "apps.utilities.motor_calc:motor_calc",
    "게시판": "apps.utilities.posting:posting",
    
    # 게임
    "오목 게임": "apps.games.gomoku_module:gomoku_game"
}

def load_module(module_path):
    """모듈 경로에서 함수 동적 로드"""
    try:
        module_name, func_name = module_path.split(':')
        module = importlib.import_module(module_name)
        return getattr(module, func_name)
    except Exception as e:
        st.error(f"모듈 로드 오류 ({module_path}): {str(e)}")
        return None

# 앱 상태 초기화
if 'screen_width' not in st.session_state:
    st.session_state.screen_width = 1200
if 'current_tool' not in st.session_state:
    st.session_state.current_tool = "3D 선형성 평가"

# 사이드바 구성
with st.sidebar:
    st.title("🛠️ 분석 도구 모음")
    st.markdown("---")
    
    # 카테고리별 도구 선택
    st.header("📊 분석 도구")
    analysis_tool = st.radio(
        "분석 도구 선택:",
        ("3D 선형성 평가", "속도 및 가속도 분석"),
        key="analysis_tool"
    )
    
    st.header("🤖 시뮬레이션 도구")
    simulation_tool = st.radio(
        "시뮬레이션 도구 선택:",
        ("수륙 양용 기차", "로봇 자율주행 시뮬레이션", "로봇 자율주행 시뮬레이션 V2"),
        key="simulation_tool"
    )
    
    st.header("🔧 유틸리티 도구")
    utility_tool = st.radio(
        "유틸리티 도구 선택:",
        ("프로젝트 진행 간트 차트", "모터 용량 계산", "게시판"),
        key="utility_tool"
    )
    
    st.header("🎮 게임")
    game_tool = st.radio(
        "게임 선택:",
        ("오목 게임",),
        key="game_tool"
    )
    
    # 현재 선택된 도구 결정 (라디오 버튼 변경 감지)
    current_selections = {
        "analysis": analysis_tool,
        "simulation": simulation_tool,
        "utility": utility_tool,
        "game": game_tool
    }
    
    # 변경된 선택 찾기
    for category, selection in current_selections.items():
        if st.session_state.get(f"last_{category}", "") != selection:
            st.session_state.current_tool = selection
            st.session_state[f"last_{category}"] = selection
            # 다른 카테고리 초기화
            for other_cat in current_selections:
                if other_cat != category:
                    st.session_state[f"last_{other_cat}"] = ""
    
    st.markdown("---")
    
    # 설정 섹션
    st.subheader("⚙️ 설정")
    theme_mode = st.radio(
        "테마:",
        ("라이트 모드", "다크 모드"),
        horizontal=True
    )
    
    # 테마 적용
    if theme_mode == "다크 모드":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .css-1d391kg {
            background-color: #262730;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # 새로고침 버튼
    if st.button("🔄 페이지 새로고침"):
        st.experimental_rerun()
    
    # 정보 표시
    st.markdown("---")
    st.markdown("### 📋 정보")
    st.markdown("**Version:** 2.0")
    st.markdown("**업데이트:** 2025-06-10")
    st.markdown("**개발자:** ABB TSU Team")

# 메인 컨텐츠 영역
current_tool = st.session_state.current_tool

# 도구 로드 및 실행
if current_tool:
    try:
        module_path = MODULE_MAP.get(current_tool)
        if module_path:
            module_func = load_module(module_path)
            if module_func:
                # 초기화 함수가 있다면 실행 (posting 모듈용)
                if current_tool == "게시판":
                    try:
                        from apps.utilities.posting import initialize_posts
                        initialize_posts()
                    except:
                        pass
                
                # 메인 함수 실행
                module_func()
            else:
                st.error(f"'{current_tool}' 도구를 로드할 수 없습니다.")
        else:
            st.error(f"도구 '{current_tool}'에 대한 모듈 경로를 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"도구 실행 중 오류가 발생했습니다: {str(e)}")
        st.info("💡 문제가 지속되면 페이지를 새로고침하거나 관리자에게 문의하세요.")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🛠️ <strong>다기능 분석 도구</strong> | 개발: ABB TSU Team | 
        <a href='https://github.com' target='_blank'>GitHub</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)
