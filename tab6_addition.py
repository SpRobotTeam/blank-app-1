
        # 새로운 데이터 관리 탭 추가
        with tab6:
            st.header("📋 데이터 관리")
            
            # 엑셀 다운로드 섹션
            st.subheader("📥 엑셀 파일 다운로드")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 엑셀 파일 생성 및 다운로드
                if st.button("📊 엑셀 파일 생성"):
                    try:
                        excel_data = create_excel_download(data)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"GANTY_LODER_분석_{timestamp}.xlsx"
                        
                        st.download_button(
                            label="💾 엑셀 파일 다운로드",
                            data=excel_data,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        st.success("✅ 엑셀 파일이 성공적으로 생성되었습니다!")
                    except Exception as e:
                        st.error(f"엑셀 파일 생성 오류: {str(e)}")
            
            with col2:
                # JSON 다운로드
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📄 JSON 데이터 다운로드",
                    data=json_str,
                    file_name=f"project_analysis_{timestamp}.json",
                    mime="application/json"
                )
            
            st.markdown("---")
            
            # 데이터 업로드 섹션
            st.subheader("📤 데이터 업로드")
            
            uploaded_file = st.file_uploader(
                "새로운 프로젝트 데이터를 업로드하세요",
                type=['json', 'xlsx', 'csv'],
                help="JSON, Excel, CSV 형식을 지원합니다."
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.json'):
                        new_data = json.load(uploaded_file)
                        st.success("✅ JSON 데이터가 성공적으로 로드되었습니다!")
                        
                    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(uploaded_file)
                        st.success("✅ 엑셀 데이터가 성공적으로 로드되었습니다!")
                        st.dataframe(df.head())
                        
                    elif uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                        st.success("✅ CSV 데이터가 성공적으로 로드되었습니다!")
                        st.dataframe(df.head())
                    
                    # 데이터 적용 버튼
                    if st.button("🔄 데이터 적용 및 새로고침"):
                        st.warning("🔄 이 기능은 실제 환경에서 구현될 예정입니다.")
                        st.info("현재는 데모 모드로 데이터 변경이 적용되지 않습니다.")
                        
                except Exception as e:
                    st.error(f"데이터 로드 오류: {str(e)}")
            
            st.markdown("---")
            
            # 데이터 미리보기
            st.subheader("🔍 데이터 미리보기")
            
            preview_option = st.selectbox(
                "미리보기 데이터 선택:",
                ["메인 분석 데이터", "고가 구매품목", "주요 제작품목", "분야별 비율"]
            )
            
            if preview_option == "메인 분석 데이터":
                st.dataframe(pd.DataFrame(data['main_analysis']), use_container_width=True)
            elif preview_option == "고가 구매품목":
                st.dataframe(pd.DataFrame(data['expensive_items']), use_container_width=True)
            elif preview_option == "주요 제작품목":
                st.dataframe(pd.DataFrame(data['manufacturing_items']), use_container_width=True)
            elif preview_option == "분야별 비율":
                st.dataframe(pd.DataFrame(data['category_ratios']), use_container_width=True)
            
            # API 연동 옵션 (미래 기능)
            st.subheader("🌐 외부 연동 (미래 기능)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("🔗 **ERP 연동**: 실시간 BOM 데이터 동기화")
                if st.button("📄 ERP 연결 테스트"):
                    st.warning("🚧 ERP 연동 기능은 개발 예정입니다.")
            
            with col2:
                st.info("📈 **비용 추적**: 자동 비용 업데이트")
                if st.button("🔄 비용 데이터 업데이트"):
                    st.warning("🚧 비용 추적 기능은 개발 예정입니다.")
    
    # 푸터 정보
    st.markdown("---")
    st.markdown("""
    ### 📈 프로젝트 분석 도구 정보
    - **버전**: 2.0.0 (고급 분석 기능 추가)
    - **최종 업데이트**: 2025-06-13
    - **데이터 기준**: GANTY-LODER 자동 용접 시스템 BOM
    - **새 기능**: 트리맵, 레이더 차트, 엑셀 다운로드
    - **개발**: ABB TSU Team
    """)

if __name__ == "__main__":
    project_analysis()
