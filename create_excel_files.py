import pandas as pd
import json
import os

def create_project_excel():
    """프로젝트 분석 엑셀 파일 생성"""
    
    # 메인 분석 데이터
    main_analysis_data = {
        '구분': ['기계 어셈블리', '기계 어셈블리', '기계 어셈블리', '기계 어셈블리', '기계 어셈블리', 
                '기계 어셈블리', '기계 어셈블리', '기계 어셈블리', '전장 시스템', '설치/시운전', 
                '설치/시운전', '후처리', '총계'],
        '항목': ['SADDLE', 'CARRIAGE', 'Y-AXIS', 'Z-AXIS', 'X-AXIS', 'R-AXIS', '잡자재', 
                '소계', '제어전장 구매품', '기계설치시운전', '제어설치시운전', '후처리 작업', '총계'],
        '총금액': [53070336, 15159090, 71698323, 30442500, 17198621, 452583000, 30000, 
                 640181870, 90000000, 120000000, 50000000, 80000000, 980181870],
        '제작서비스': [4977336, 2164090, 24698323, 2442500, 9198621, 7583000, 0, 
                    50063870, 0, 120000000, 50000000, 80000000, 300063870],
        '구매금액': [48093000, 12995000, 47000000, 28000000, 8000000, 445000000, 30000, 
                   590118000, 90000000, 0, 0, 0, 680118000],
        '제작비율': ['9.4%', '14.3%', '34.4%', '8.0%', '53.5%', '1.7%', '0%', 
                   '7.8%', '0%', '100%', '100%', '100%', '30.6%']
    }
    
    # 고가 구매품목 데이터
    expensive_items_data = {
        '품목': ['ABB 로봇 시스템', 'LINCOLN 용접기 R450', 'Y-AXIS GIRDER', '감속기 (YJD110)', 
                'APEX 감속기 (AFR140)', 'THK LM GUIDE', '한국이구스 에너지체인', 'THK 볼스크류'],
        '금액': [110000000, 34800000, 19500000, 2758000, 1795000, 1340720, 3400000, 2370000],
        '비고': ['R-AXIS 핵심 장비', '용접 핵심 장비', '제작 품목', 'SADDLE용, 6개', 
                'CARRIAGE용, 3개', 'Y-AXIS용, 6개', 'Z-AXIS용', 'Z-AXIS용']
    }
    
    # 주요 제작품목 데이터
    manufacturing_items_data = {
        '품목': ['X-RAIL', 'X-BEAM', 'POST-BODY', 'Y-AXIS GIRDER', 'CARRIAGE-PLATE', 'Z-BEAM'],
        '금액': [3675000, 4241500, 851250, 19500000, 1497000, 1857750],
        '수량': [1, 1, 18, 1, 1, 1],
        '어셈블리': ['X-AXIS', 'X-AXIS', 'X-AXIS', 'Y-AXIS', 'CARRIAGE', 'Z-AXIS']
    }
    
    # 분야별 비율 데이터
    category_ratio_data = {
        '분야': ['기계 어셈블리', '제어전장', '설치/시운전', '후처리'],
        '금액': [640181870, 90000000, 170000000, 80000000],
        '비율': ['65.3%', '9.2%', '17.3%', '8.2%']
    }
    
    # DataFrame 생성
    df_main = pd.DataFrame(main_analysis_data)
    df_expensive = pd.DataFrame(expensive_items_data)
    df_manufacturing = pd.DataFrame(manufacturing_items_data)
    df_category = pd.DataFrame(category_ratio_data)
    
    # 엑셀 파일 저장
    excel_file_path = 'project_bom_analysis.xlsx'
    
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        # 각 시트에 데이터 저장
        df_main.to_excel(writer, sheet_name='메인_분석표', index=False)
        df_expensive.to_excel(writer, sheet_name='고가_구매품목', index=False)
        df_manufacturing.to_excel(writer, sheet_name='주요_제작품목', index=False)
        df_category.to_excel(writer, sheet_name='분야별_비율', index=False)
        
        # 요약 시트 생성
        summary_data = {
            '항목': ['프로젝트명', '총 프로젝트 금액', '기계 어셈블리', '제어전장', '설치/시운전', '후처리'],
            '값': ['GANTY-LODER 자동 용접 시스템', '980,181,870원', '640,181,870원', '90,000,000원', '170,000,000원', '80,000,000원'],
            '비고': ['', '설치/시운전 포함', '65.3%', '9.2%', '17.3%', '8.2%']
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='프로젝트_요약', index=False)
    
    print(f"엑셀 파일이 생성되었습니다: {excel_file_path}")
    print(f"파일 크기: {os.path.getsize(excel_file_path)} bytes")
    
    return excel_file_path, df_main, df_expensive, df_manufacturing, df_category

def create_template_excel():
    """빈 템플릿 엑셀 파일 생성 (사용자가 데이터 입력용)"""
    
    template_data = {
        '구분': ['', '', '', '', ''],
        '항목': ['', '', '', '', ''],
        '총금액': [0, 0, 0, 0, 0],
        '제작서비스': [0, 0, 0, 0, 0],
        '구매금액': [0, 0, 0, 0, 0],
        '제작비율': ['', '', '', '', '']
    }
    
    df_template = pd.DataFrame(template_data)
    template_file_path = 'bom_template.xlsx'
    
    with pd.ExcelWriter(template_file_path, engine='openpyxl') as writer:
        df_template.to_excel(writer, sheet_name='BOM_데이터', index=False)
        
        # 가이드 시트 생성
        guide_data = {
            '컬럼명': ['구분', '항목', '총금액', '제작서비스', '구매금액', '제작비율'],
            '설명': [
                '기계 어셈블리, 전장 시스템, 설치/시운전, 후처리 등',
                'SADDLE, CARRIAGE, Y-AXIS 등 구체적인 항목명',
                '해당 항목의 총 금액 (숫자만 입력)',
                '제작 또는 서비스 금액 (숫자만 입력)',
                '구매 금액 (숫자만 입력)',
                '제작 비율 (예: 9.4%)'
            ],
            '예시': [
                '기계 어셈블리',
                'SADDLE',
                '53070336',
                '4977336',
                '48093000',
                '9.4%'
            ]
        }
        df_guide = pd.DataFrame(guide_data)
        df_guide.to_excel(writer, sheet_name='입력_가이드', index=False)
    
    print(f"템플릿 파일이 생성되었습니다: {template_file_path}")
    return template_file_path

if __name__ == "__main__":
    # 프로젝트 분석 엑셀 파일 생성
    excel_path, df_main, df_expensive, df_manufacturing, df_category = create_project_excel()
    
    # 템플릿 파일 생성
    template_path = create_template_excel()
    
    print("\n=== 파일 생성 완료 ===")
    print(f"1. 프로젝트 분석 파일: {excel_path}")
    print(f"2. 빈 템플릿 파일: {template_path}")
    
    print("\n=== 데이터 미리보기 ===")
    print("메인 분석 데이터 (처음 5행):")
    print(df_main.head())
    
    print("\n고가 구매품목 데이터:")
    print(df_expensive.head())
