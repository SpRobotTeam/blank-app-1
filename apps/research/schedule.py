import streamlit as st
import streamlit.components.v1 as components
from .utils import SCHEDULE_HTML_PATH

def schedule_viewer():
    """연구 일정 뷰어"""
    st.title("📅 연구 진행 일정")
    st.write("---")
    st.write("26주간의 연구 진행 일정을 시각적으로 확인할 수 있습니다.")

    try:
        # HTML 파일을 직접 임베드
        with open(SCHEDULE_HTML_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # HTML 내용에 Streamlit 테마와 어울리도록 최소한의 CSS 수정 적용
        html_content = html_content.replace(
            'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);', 
            'background: white;'
        )
        html_content = html_content.replace(
            'font-family: \'Malgun Gothic\', Arial, sans-serif;', 
            'font-family: sans-serif;'
        )
        html_content = html_content.replace(
            'box-shadow: 0 20px 40px rgba(0,0,0,0.1);', 
            'box-shadow: none;'
        )

        # HTML 내용을 직접 렌더링
        components.html(html_content, height=1000, scrolling=True)
        
        st.success("✅ 연구 일정이 성공적으로 로드되었습니다.")
        
    except FileNotFoundError:
        st.error("❌ 연구 일정 HTML 파일을 찾을 수 없습니다.")
        st.info(f"📁 예상 경로: `{SCHEDULE_HTML_PATH}`")
        st.info("파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"HTML 파일을 읽는 중 오류가 발생했습니다: {e}")

    st.write("---")
    st.info("ℹ️ 이 섹션은 `welding_gantry_research_schedule.html` 파일의 내용을 직접 표시합니다.")
    
    # 일정 요약 정보
    st.subheader("📊 일정 요약")
    st.markdown("""
    - **전체 기간**: 26주 (약 6개월)
    - **주요 단계**: 기초 연구 → 설계 분석 → 구조 해석 → 통합 검증
    - **핵심 마일스톤**: 주요 구조물별 FEA 분석 완료, 시스템 통합 설계 검증
    """)
