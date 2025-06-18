import streamlit as st
import re
from .utils import load_research_notes_metadata

def research_notes_viewer():
    """연구 노트 뷰어"""
    st.title("📝 주차별 연구 노트")
    st.write("---")

    notes_metadata = load_research_notes_metadata()
    
    if not notes_metadata:
        st.warning("`week_files` 폴더에 연구 노트 파일이 없습니다. 파일명을 확인해주세요 (`week_XX_연구노트.md` 형식).")
        return

    # 검색 기능
    search_query = st.text_input("연구노트 검색 (제목 또는 요약)", "").lower()
    
    filtered_notes = [
        note for note in notes_metadata 
        if search_query in note["title"].lower() or search_query in note["summary"].lower()
    ]

    if not filtered_notes:
        st.info("검색 결과가 없습니다.")
        return

    # 주차 선택 (기본값은 가장 최신 주차)
    current_idx = 0
    if "current_note_idx" in st.session_state and st.session_state.current_note_idx < len(filtered_notes):
        current_idx = st.session_state.current_note_idx
    else:
        current_idx = len(filtered_notes) - 1

    # 버튼 기반 내비게이션
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 이전 주차", key="prev_week"):
            if current_idx > 0:
                current_idx -= 1
                st.session_state.current_note_idx = current_idx
                st.rerun()
            else:
                st.warning("첫 번째 연구 노트입니다.")
    with col3:
        if st.button("다음 주차 ➡️", key="next_week"):
            if current_idx < len(filtered_notes) - 1:
                current_idx += 1
                st.session_state.current_note_idx = current_idx
                st.rerun()
            else:
                st.warning("마지막 연구 노트입니다.")
    
    # 드롭다운 선택
    selected_note_label = st.selectbox(
        "확인할 연구 주차를 선택하세요:",
        options=[note["label"] for note in filtered_notes],
        index=current_idx,
        key="research_note_selector"
    )

    # selectbox 변경 시 current_note_idx 업데이트
    selected_idx = [i for i, note in enumerate(filtered_notes) if note["label"] == selected_note_label][0]
    st.session_state.current_note_idx = selected_idx

    # 선택된 연구 노트 파일 내용 읽어오기
    selected_note = filtered_notes[selected_idx]
    st.subheader(f"{selected_note['title']}")
    st.caption(f"파일: `{selected_note['file_name']}`")
    st.info(f"**요약**: {selected_note['summary']}")

    try:
        with open(selected_note['file_path'], "r", encoding="utf-8") as f:
            note_content = f.read()
        
        # 주석 제거 (```chart ... ```)
        note_content = re.sub(r'```chart[\s\S]+?```', '', note_content)

        st.markdown(note_content)
    except FileNotFoundError:
        st.error(f"'{selected_note['file_path']}' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    
    st.markdown("---")
    st.info("💡 Markdown 파일 내의 LaTeX 수식은 자동으로 렌더링됩니다. (예: $T = J \\times \\alpha$)")

# 세션 상태 초기화
if "current_note_idx" not in st.session_state:
    notes_metadata = load_research_notes_metadata()
    st.session_state.current_note_idx = len(notes_metadata) - 1 if notes_metadata else 0
