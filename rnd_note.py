import streamlit as st
import os
import base64
import re
from streamlit_pdf_viewer import pdf_viewer # PDF 뷰어 라이브러리 추가

# --- 파일 경로 정의 ---
FILE_DIR = "week_files/"
PDF_PATH = os.path.join(FILE_DIR, "소부재 용접 갠트리 로봇 __B-LINE__ 컨셉 기술백서.pdf")
SCHEDULE_HTML_PATH = os.path.join(FILE_DIR, "welding_gantry_research_schedule.html")

# --- Streamlit 페이지 설정 ---
st.set_page_config(
    page_title="소부재 용접 갠트리 로봇 연구",
    page_icon="🤖",
    layout="wide"
)

# --- 유틸리티 함수 ---
@st.cache_data # 데이터 캐싱으로 성능 향상
def load_research_notes_metadata():
    """주차별 연구노트 파일 목록과 메타데이터 (제목, 요약)를 로드합니다."""
    md_files = sorted([f for f in os.listdir(FILE_DIR) if f.startswith('week_') and f.endswith('.md')],
                      key=lambda x: int(x.split('_')[1])) # 숫자 부분으로 정렬

    notes_metadata = []
    for file_name in md_files:
        file_path = os.path.join(FILE_DIR, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # 첫 번째 제목 (H1) 추출
                title_match = re.search(r'^#\s*(.+?)\n', content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else file_name

                # 첫 번째 부제목 (H2) 아래의 내용 중 일부를 요약으로 추출
                summary_match = re.search(r'##\s*(\d+\.?\s*[\w\s\/]+)\s*\n([\s\S]+?)(?=\n##|$)', content)
                summary = ""
                if summary_match:
                    summary_text = summary_match.group(2).strip()
                    # 첫 2~3줄만 가져오기
                    summary_lines = summary_text.split('\n')
                    summary = " ".join([line.strip() for line in summary_lines if line.strip()][:3]) + "..."
                else:
                    summary = "요약 내용을 찾을 수 없습니다."

                notes_metadata.append({
                    "file_name": file_name,
                    "file_path": file_path,
                    "label": f"Week {int(file_name.split('_')[1])}: {title.split(': ')[-1].strip()}",
                    "title": title,
                    "summary": summary
                })
        except Exception as e:
            st.warning(f"연구노트 파일 '{file_name}' 로드 중 오류 발생: {e}")
            notes_metadata.append({
                "file_name": file_name,
                "file_path": file_path,
                "label": f"Week {int(file_name.split('_')[1])}: (오류 발생)",
                "title": "(오류)",
                "summary": f"파일 로드 오류: {e}"
            })
    return notes_metadata

NOTES_METADATA = load_research_notes_metadata()
NUM_WEEKS = len(NOTES_METADATA)

# --- 페이지 렌더링 함수 ---
def render_main_page():
    st.title("🚀 소부재 용접 갠트리 로봇 B-LINE 컨셉 연구 종합")
    st.write("---")
    st.markdown("""
    본 웹 애플리케이션은 에스피시스템스에서 개발 중인 소부재 용접 자동화 로봇 시스템 (B-LINE 컨셉)에 대한
    26주간의 연구 결과를 종합적으로 제공합니다. 조선소의 소형 블록 및 부재 용접을 99% 무인 자동화하여
    생산성을 혁신하는 목표 아래, 6개월간 기계 설계 및 해석 측면의 기초 연구가 수행되었습니다.
    """)

    st.header("✨ 주요 연구 목표")
    st.markdown("""
    - **갠트리 로봇 시스템 아키텍처 구축:** 전체 시스템의 기능 및 구조 정의.
    - **핵심 기구부 부품 사양 검토:** 모터, 베어링, LM 가이드, 볼스크류, 랙&피니언 등 주요 구동계 분석.
    - **구조물 강성 및 안정성 해석:** 휠샤프트, 세들, 거더, 캐리지, Z축 빔 등 주요 구조물의 FEA 분석.
    - **충격 하중 및 수명 평가:** 스토퍼 충격력, 동적 하중 조건에서의 구조물 내구성 및 부품 수명 검증.
    - **최종 통합 보고서 작성:** 26주간의 연구 결과를 종합하고 향후 개발 전략 제시.
    """)
    st.write("---")

    st.header("📊 연구 개요 통계")
    try:
        with open(SCHEDULE_HTML_PATH, "r", encoding="utf-8") as f:
            schedule_html_content = f.read()
            
        total_weeks_match = re.search(r'<div class="stat-number">(\d+)</div>\s*<div class="stat-label">총 연구 주차</div>', schedule_html_content)
        major_fields_match = re.search(r'<div class="stat-number">(\d+)</div>\s*<div class="stat-label">주요 검토 분야</div>', schedule_html_content)
        report_pages_match = re.search(r'<div class="stat-number">(\d+)</div>\s*<div class="stat-label">검토보고서 페이지</div>', schedule_html_content)
        analysis_count_match = re.search(r'<div class="stat-number">(.*?)</div>\s*<div class="stat-label">구조해석 건수</div>', schedule_html_content)

        total_weeks = total_weeks_match.group(1) if total_weeks_match else "N/A"
        major_fields = major_fields_match.group(1) if major_fields_match else "N/A"
        report_pages = report_pages_match.group(1) if report_pages_match else "N/A"
        analysis_count = analysis_count_match.group(1) if analysis_count_match else "N/A"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="총 연구 주차", value=total_weeks)
        with col2:
            st.metric(label="주요 검토 분야", value=major_fields)
        with col3:
            st.metric(label="검토 보고서 페이지", value=report_pages)
        with col4:
            st.metric(label="구조 해석 건수", value=analysis_count)

    except FileNotFoundError:
        st.warning("연구 일정 HTML 파일을 찾을 수 없어 연구 통계를 표시할 수 없습니다.")
    except Exception as e:
        st.warning(f"연구 일정 HTML 파싱 중 오류 발생: {e}")

    st.write("---")
    st.subheader("💡 연구 성과 요약")
    st.markdown("""
    - 모든 주요 기구부 및 구조물에 대한 **강성, 안전계수, 수명, 동적 하중 대응 능력**이 검증되었습니다.
    - 특히 **세들 프레임의 구조 개선**을 통해 안전계수가 대폭 향상되었으며, **거더 처짐량에 대한 회귀식**을 도출하여
      정밀 제어 및 예측 유지보수 기반을 마련했습니다.
    - 각 축별 **모터 토크 여유율**과 **구동계 부품 수명** 또한 충분한 것으로 확인되었습니다.
    """)

    st.subheader("📚 핵심 연구 결과 데이터 요약 (Week 26 기반)")
    try:
        week26_path = os.path.join(FILE_DIR, "week_26_연구노트.md")
        with open(week26_path, "r", encoding="utf-8") as f:
            week26_content = f.read()

        # "구조 강성 및 변위" 테이블 파싱
        table_match = re.search(r'### 3-1\. 구조 강성 및 변위\s*\| 구성 요소 \| 최대 응력 \(MPa\) \| 최대 변위 \(mm\) \| 안전계수 \|\s*\|-+\s*\|-+\s*\|-+\s*\|-+\s*\|\s*([\s\S]+?)(?=\n\n|\n###|$)', week26_content)
        
        if table_match:
            table_str = table_match.group(1).strip()
            # 각 행을 파싱하여 데이터프레임으로 변환
            import pandas as pd
            data = []
            for line in table_str.split('\n'):
                if line.strip() and not line.strip().startswith('|---'):
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) == 4: # 헤더 제외
                        try:
                            data.append({
                                "구성 요소": parts[0],
                                "최대 응력 (MPa)": float(parts[1]),
                                "최대 변위 (mm)": float(parts[2]),
                                "안전계수": float(parts[3])
                            })
                        except ValueError:
                            # 데이터 변환 오류 무시 (예: '15+' 같은 값)
                            data.append({
                                "구성 요소": parts[0],
                                "최대 응력 (MPa)": parts[1],
                                "최대 변위 (mm)": parts[2],
                                "안전계수": parts[3]
                            })
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            st.caption("※ Week 26 연구노트 기반 주요 구조물 해석 결과 요약")
        else:
            st.info("Week 26 연구노트에서 '구조 강성 및 변위' 데이터를 찾을 수 없습니다.")

        # "시스템 구성 비중 예측" 차트 (Week 01)
        week01_path = os.path.join(FILE_DIR, "week_01_연구노트.md")
        with open(week01_path, "r", encoding="utf-8") as f:
            week01_content = f.read()
        
        chart_match = re.search(r'### 5-2\. 시스템 구성 비중 예측\s*```chart\s*bar\s*([\s\S]+?)```', week01_content)
        if chart_match:
            chart_data_str = chart_match.group(1).strip()
            chart_data = {}
            for line in chart_data_str.split('\n'):
                if ':' in line:
                    key, value = line.split(':')
                    chart_data[key.strip()] = int(value.strip())
            
            chart_df = pd.DataFrame(list(chart_data.items()), columns=['구성요소', '비중'])
            st.bar_chart(chart_df, x='구성요소', y='비중', height=300)
            st.caption("※ Week 01 연구노트 기반 시스템 구성 비중 예측")
        else:
            st.info("Week 01 연구노트에서 '시스템 구성 비중 예측' 차트 데이터를 찾을 수 없습니다.")

    except FileNotFoundError:
        st.warning("일부 연구노트 파일을 찾을 수 없어 상세 데이터를 표시할 수 없습니다.")
    except Exception as e:
        st.warning(f"메인 페이지 데이터 파싱 중 오류 발생: {e}")

    st.write("---")
    st.info("👈 왼쪽 메뉴를 통해 상세 연구 노트 및 기술 백서 내용을 확인하실 수 있습니다.")


def render_research_notes_page():
    st.title("📝 주차별 연구 노트")
    st.write("---")

    if not NOTES_METADATA:
        st.warning("`week_files` 폴더에 연구 노트 파일이 없습니다. 파일명을 확인해주세요 (`week_XX_연구노트.md` 형식).")
        return

    # 검색 기능
    search_query = st.text_input("연구노트 검색 (제목 또는 요약)", "").lower()
    
    filtered_notes = [
        note for note in NOTES_METADATA 
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
        current_idx = len(filtered_notes) - 1 # 기본값은 마지막 주차

    # 버튼 기반 내비게이션
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 이전 주차"):
            if current_idx > 0:
                current_idx -= 1
                st.session_state.current_note_idx = current_idx
            else:
                st.warning("첫 번째 연구 노트입니다.")
    with col3:
        if st.button("다음 주차 ➡️"):
            if current_idx < len(filtered_notes) - 1:
                current_idx += 1
                st.session_state.current_note_idx = current_idx
            else:
                st.warning("마지막 연구 노트입니다.")
    
    # 드롭다운 선택
    selected_note_label = st.selectbox(
        "확인할 연구 주차를 선택하세요:",
        options=[note["label"] for note in filtered_notes],
        index=current_idx,
        key="note_selector"
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

        st.markdown(note_content) # Markdown 형식으로 렌더링
    except FileNotFoundError:
        st.error(f"'{selected_note['file_path']}' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    
    # 수학 수식 렌더링 확인 (자동으로 됨)
    st.markdown("---")
    st.info("💡 Markdown 파일 내의 LaTeX 수식은 자동으로 렌더링됩니다. (예: $T = J \\times \\alpha$)")


def render_technical_paper_page():
    st.title("📄 소부재 용접 갠트리 로봇 B-LINE 컨셉 기술백서")
    st.write("---")
    st.write("26주간의 연구 노트를 종합 정리한 **기술백서**입니다.")

    try:
        # PDF 다운로드 버튼
        with open(PDF_PATH, "rb") as f:
            pdf_bytes = f.read()
            st.download_button(
                label="기술백서 PDF 다운로드",
                data=pdf_bytes,
                file_name="소부재_용접_갠트리_로봇_B-LINE_컨셉_기술백서.pdf",
                mime="application/pdf"
            )
        
        # streamlit-pdf-viewer 사용
        pdf_viewer(PDF_PATH, width=700, height=800) # width와 height를 조절하여 적절한 크기로 표시
        st.info("기술백서 PDF가 페이지에 임베드되어 있습니다.")

    except FileNotFoundError:
        st.error("기술백서 PDF 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"PDF 파일을 처리하는 중 오류가 발생했습니다: {e}")

    st.subheader("기술백서 주요 내용 요약")
    st.markdown("""
    - **개요**: 조선소 소형 블록/부재 용접의 99% 무인 자동화를 목표로 하는 B-LINE 컨셉 설명.
    - **기술 검토**: B-LINE 시스템 개념, 관련 자동화 기술 배경.
    - **설계 해석**: 주차별 핵심 설계 및 해석 결과 상세 분석 (베어링 수명, 구동모터 용량, 구조 강도 등).
    - **적용성 분석**: 연구 결과가 산업 현장에 미칠 효과 수치화.
    - **결론**: 설계 타당성 종합 평가 및 향후 개발 방향 제시.
    """)

def render_research_schedule_page():
    st.title("📅 연구 진행 일정")
    st.write("---")
    st.write("26주간의 연구 진행 일정을 시각적으로 확인할 수 있습니다.")

    try:
        # HTML 파일을 직접 임베드
        with open(SCHEDULE_HTML_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # HTML 내용에 Streamlit 테마와 어울리도록 최소한의 CSS 수정 적용 (선택 사항)
        html_content = html_content.replace('background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);', 'background: white;')
        html_content = html_content.replace('font-family: \'Malgun Gothic\', Arial, sans-serif;', 'font-family: sans-serif;')
        html_content = html_content.replace('box-shadow: 0 20px 40px rgba(0,0,0,0.1);', 'box-shadow: none;') # Streamlit은 자체 그림자 있으므로 제거

        st.components.v1.html(html_content, height=1000, scrolling=True) # HTML 내용을 직접 렌더링
    except FileNotFoundError:
        st.error("연구 일정 HTML 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"HTML 파일을 읽는 중 오류가 발생했습니다: {e}")

    st.info("이 섹션은 `welding_gantry_research_schedule.html` 파일의 내용을 직접 표시합니다.")

# --- 사이드바 구성 ---
st.sidebar.title("메뉴")
selected_page = st.sidebar.radio("이동", ["메인 페이지", "연구 노트", "기술 백서", "연구 일정"])

# 연구 노트 주차 목록 확장 (사이드바)
if selected_page == "연구 노트":
    with st.sidebar.expander("주차별 연구 노트 목록"):
        for i, note in enumerate(NOTES_METADATA):
            # 클릭 시 해당 주차로 이동하도록 세션 상태 변경
            if st.button(note["label"], key=f"sidebar_week_{i}"):
                st.session_state.selected_page = "연구 노트"
                st.session_state.current_note_idx = i
                st.rerun() # 페이지 리로드

# --- 메인 콘텐츠 렌더링 ---
if selected_page == "메인 페이지":
    render_main_page()
elif selected_page == "연구 노트":
    render_research_notes_page()
elif selected_page == "기술 백서":
    render_technical_paper_page()
elif selected_page == "연구 일정":
    render_research_schedule_page()

# 세션 상태 초기화 (다른 페이지로 이동 시 연구 노트 인덱스 초기화 방지)
if "current_note_idx" not in st.session_state:
    st.session_state.current_note_idx = NUM_WEEKS - 1 # 기본값은 마지막 주차
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "메인 페이지"

# Sidebar radio button changes session_state implicitly.
# We ensure the page is correctly rendered based on selected_page.
# This rerun is primarily for initial load or sidebar clicks to notes.
if selected_page != st.session_state.selected_page:
    st.session_state.selected_page = selected_page
    st.rerun()