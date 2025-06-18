import streamlit as st
import os
from .utils import PDF_PATH

def technical_paper_viewer():
    """기술 백서 뷰어"""
    st.title("📄 소부재 용접 갠트리 로봇 B-LINE 컨셉 기술백서")
    st.write("---")
    st.write("26주간의 연구 노트를 종합 정리한 **기술백서**입니다.")

    try:
        # PDF 다운로드 버튼
        with open(PDF_PATH, "rb") as f:
            pdf_bytes = f.read()
            st.download_button(
                label="📥 기술백서 PDF 다운로드",
                data=pdf_bytes,
                file_name="소부재_용접_갠트리_로봇_B-LINE_컨셉_기술백서.pdf",
                mime="application/pdf"
            )
        
        # PDF 뷰어 시도
        try:
            from streamlit_pdf_viewer import pdf_viewer
            pdf_viewer(PDF_PATH, width=700, height=800)
            st.info("✅ 기술백서 PDF가 페이지에 임베드되어 있습니다.")
        except ImportError:
            st.warning("PDF 뷰어 라이브러리가 설치되지 않았습니다. 다운로드 버튼을 사용해 PDF를 확인하세요.")
            st.code("pip install streamlit-pdf-viewer")
        except Exception as e:
            st.warning(f"PDF 뷰어 로드 중 오류: {e}")
            st.info("다운로드 버튼을 사용해 PDF를 확인하세요.")

    except FileNotFoundError:
        st.error("❌ 기술백서 PDF 파일을 찾을 수 없습니다.")
        st.info(f"📁 예상 경로: `{PDF_PATH}`")
        st.info("파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"PDF 파일을 처리하는 중 오류가 발생했습니다: {e}")

    st.write("---")
    st.subheader("📋 기술백서 주요 내용 요약")
    st.markdown("""
    - **개요**: 조선소 소형 블록/부재 용접의 99% 무인 자동화를 목표로 하는 B-LINE 컨셉 설명.
    - **기술 검토**: B-LINE 시스템 개념, 관련 자동화 기술 배경.
    - **설계 해석**: 주차별 핵심 설계 및 해석 결과 상세 분석 (베어링 수명, 구동모터 용량, 구조 강도 등).
    - **적용성 분석**: 연구 결과가 산업 현장에 미칠 효과 수치화.
    - **결론**: 설계 타당성 종합 평가 및 향후 개발 방향 제시.
    """)

    # 파일 정보 표시
    if os.path.exists(PDF_PATH):
        file_size = os.path.getsize(PDF_PATH)
        file_size_mb = file_size / (1024 * 1024)
        st.info(f"📊 파일 크기: {file_size_mb:.2f} MB")
