import streamlit as st
import os
import re
import pandas as pd

# --- 파일 경로 정의 ---
FILE_DIR = "week_files/"
PDF_PATH = os.path.join(FILE_DIR, "소부재 용접 갠트리 로봇 __B-LINE__ 컨셉 기술백서.pdf")
SCHEDULE_HTML_PATH = os.path.join(FILE_DIR, "welding_gantry_research_schedule.html")

@st.cache_data
def load_research_notes_metadata():
    """주차별 연구노트 파일 목록과 메타데이터 (제목, 요약)를 로드합니다."""
    try:
        md_files = sorted([f for f in os.listdir(FILE_DIR) if f.startswith('week_') and f.endswith('.md')],
                          key=lambda x: int(x.split('_')[1]))
    except FileNotFoundError:
        st.warning(f"`{FILE_DIR}` 폴더를 찾을 수 없습니다.")
        return []

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

def load_week26_structure_data():
    """Week 26 연구노트에서 구조 강성 및 변위 테이블 데이터를 로드합니다."""
    try:
        week26_path = os.path.join(FILE_DIR, "week_26_연구노트.md")
        with open(week26_path, "r", encoding="utf-8") as f:
            week26_content = f.read()

        # "구조 강성 및 변위" 테이블 파싱
        table_match = re.search(r'### 3-1\. 구조 강성 및 변위\s*\| 구성 요소 \| 최대 응력 \(MPa\) \| 최대 변위 \(mm\) \| 안전계수 \|\s*\|-+\s*\|-+\s*\|-+\s*\|-+\s*\|\s*([\s\S]+?)(?=\n\n|\n###|$)', week26_content)
        
        if table_match:
            table_str = table_match.group(1).strip()
            data = []
            for line in table_str.split('\n'):
                if line.strip() and not line.strip().startswith('|---'):
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) == 4:
                        try:
                            data.append({
                                "구성 요소": parts[0],
                                "최대 응력 (MPa)": float(parts[1]),
                                "최대 변위 (mm)": float(parts[2]),
                                "안전계수": float(parts[3])
                            })
                        except ValueError:
                            data.append({
                                "구성 요소": parts[0],
                                "최대 응력 (MPa)": parts[1],
                                "최대 변위 (mm)": parts[2],
                                "안전계수": parts[3]
                            })
            return pd.DataFrame(data)
    except Exception as e:
        st.warning(f"Week 26 데이터 로드 중 오류: {e}")
    return pd.DataFrame()

def load_week01_chart_data():
    """Week 01 연구노트에서 시스템 구성 비중 예측 차트 데이터를 로드합니다."""
    try:
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
            
            return pd.DataFrame(list(chart_data.items()), columns=['구성요소', '비중'])
    except Exception as e:
        st.warning(f"Week 01 차트 데이터 로드 중 오류: {e}")
    return pd.DataFrame()

def load_schedule_stats():
    """연구 일정 HTML에서 통계 데이터를 추출합니다."""
    try:
        with open(SCHEDULE_HTML_PATH, "r", encoding="utf-8") as f:
            schedule_html_content = f.read()
            
        total_weeks_match = re.search(r'<div class="stat-number">(\d+)</div>\s*<div class="stat-label">총 연구 주차</div>', schedule_html_content)
        major_fields_match = re.search(r'<div class="stat-number">(\d+)</div>\s*<div class="stat-label">주요 검토 분야</div>', schedule_html_content)
        report_pages_match = re.search(r'<div class="stat-number">(\d+)</div>\s*<div class="stat-label">검토보고서 페이지</div>', schedule_html_content)
        analysis_count_match = re.search(r'<div class="stat-number">(.*?)</div>\s*<div class="stat-label">구조해석 건수</div>', schedule_html_content)

        return {
            "total_weeks": total_weeks_match.group(1) if total_weeks_match else "N/A",
            "major_fields": major_fields_match.group(1) if major_fields_match else "N/A",
            "report_pages": report_pages_match.group(1) if report_pages_match else "N/A",
            "analysis_count": analysis_count_match.group(1) if analysis_count_match else "N/A"
        }
    except Exception as e:
        st.warning(f"연구 일정 통계 로드 중 오류: {e}")
        return {"total_weeks": "N/A", "major_fields": "N/A", "report_pages": "N/A", "analysis_count": "N/A"}
