import streamlit as st
import pandas as pd
from .utils import load_research_notes_metadata, load_week26_structure_data, load_week01_chart_data, load_schedule_stats

def research_dashboard():
    """연구 대시보드 메인 페이지"""
    st.title("🚀 소부재 용접 갠트리 로봇 B-LINE 컨셉 연구 종합")
    st.write("---")
    
    st.markdown("""
    본 연구 대시보드는 에스피시스템스에서 개발 중인 소부재 용접 자동화 로봇 시스템 (B-LINE 컨셉)에 대한
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
    stats = load_schedule_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="총 연구 주차", value=stats["total_weeks"])
    with col2:
        st.metric(label="주요 검토 분야", value=stats["major_fields"])
    with col3:
        st.metric(label="검토 보고서 페이지", value=stats["report_pages"])
    with col4:
        st.metric(label="구조 해석 건수", value=stats["analysis_count"])

    st.write("---")
    st.subheader("💡 연구 성과 요약")
    st.markdown("""
    - 모든 주요 기구부 및 구조물에 대한 **강성, 안전계수, 수명, 동적 하중 대응 능력**이 검증되었습니다.
    - 특히 **세들 프레임의 구조 개선**을 통해 안전계수가 대폭 향상되었으며, **거더 처짐량에 대한 회귀식**을 도출하여
      정밀 제어 및 예측 유지보수 기반을 마련했습니다.
    - 각 축별 **모터 토크 여유율**과 **구동계 부품 수명** 또한 충분한 것으로 확인되었습니다.
    """)

    st.subheader("📚 핵심 연구 결과 데이터 요약 (Week 26 기반)")
    
    # Week 26 구조 강성 데이터 표시
    df_structure = load_week26_structure_data()
    if not df_structure.empty:
        st.dataframe(df_structure, use_container_width=True)
        st.caption("※ Week 26 연구노트 기반 주요 구조물 해석 결과 요약")
    else:
        st.info("Week 26 연구노트에서 '구조 강성 및 변위' 데이터를 찾을 수 없습니다.")

    # Week 01 시스템 구성 비중 차트
    df_chart = load_week01_chart_data()
    if not df_chart.empty:
        st.bar_chart(df_chart, x='구성요소', y='비중', height=300)
        st.caption("※ Week 01 연구노트 기반 시스템 구성 비중 예측")
    else:
        st.info("Week 01 연구노트에서 '시스템 구성 비중 예측' 차트 데이터를 찾을 수 없습니다.")

    st.write("---")
    
    # 연구 노트 개요
    notes_metadata = load_research_notes_metadata()
    if notes_metadata:
        st.subheader("📝 연구 노트 개요")
        st.info(f"총 **{len(notes_metadata)}주차**의 연구 노트가 작성되었습니다.")
        
        # 최근 5주차 연구 노트 미리보기
        recent_notes = notes_metadata[-5:] if len(notes_metadata) >= 5 else notes_metadata
        st.markdown("**최근 연구 노트:**")
        for note in recent_notes:
            with st.expander(f"{note['label']}"):
                st.write(note['summary'])
    
    st.info("👈 왼쪽 메뉴에서 **연구 문서** 카테고리를 선택하여 상세 내용을 확인하실 수 있습니다.")
