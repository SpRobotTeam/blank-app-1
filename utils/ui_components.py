import streamlit as st
from datetime import datetime

def tool_header(title, description):
    """모든 도구에 공통적으로 적용할 헤더 컴포넌트"""
    st.title(f"🛠️ {title}")
    st.markdown(f"<p class='tool-description'>{description}</p>", unsafe_allow_html=True)
    st.markdown("---")

def file_upload_with_example(key, file_types, example_file=None):
    """일관된 파일 업로드 UI 컴포넌트"""
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("파일 업로드", type=file_types, key=key)
    with col2:
        if example_file and st.button("예제 파일 사용", key=f"example_{key}"):
            return example_file
    return uploaded_file

def responsive_columns(num_cols, content_funcs):
    """화면 크기에 따라 컬럼 레이아웃 조정"""
    # 화면이 작을 때는 단일 컬럼으로 변경
    screen_width = st.session_state.get('screen_width', 1200)
    if screen_width < 768:  # 모바일 화면으로 간주
        for func in content_funcs:
            func()
    else:
        cols = st.columns(num_cols)
        for i, func in enumerate(content_funcs):
            with cols[i % num_cols]:
                func()

def sidebar_info(version="1.0", update_date=None):
    """사이드바에 버전 정보 표시"""
    if update_date is None:
        update_date = datetime.now().strftime("%Y-%m-%d")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 정보")
    st.sidebar.markdown(f"**Version:** {version}")
    st.sidebar.markdown(f"**업데이트:** {update_date}")

def error_handler(error_message):
    """통일된 에러 메시지 표시"""
    st.error(f"⚠️ 오류가 발생했습니다: {error_message}")
    st.info("💡 문제가 지속되면 페이지를 새로고침하거나 관리자에게 문의하세요.")

def success_message(message):
    """성공 메시지 표시"""
    st.success(f"✅ {message}")

def info_message(message):
    """정보 메시지 표시"""
    st.info(f"ℹ️ {message}")
