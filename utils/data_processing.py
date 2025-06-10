import pandas as pd
import numpy as np
import streamlit as st

def preprocess_excel_data(df, required_columns=None, fill_strategy='mean'):
    """데이터 전처리 공통 함수"""
    # NaN 처리
    if fill_strategy == 'mean':
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    elif fill_strategy == 'zero':
        df = df.fillna(0)
    elif fill_strategy == 'drop':
        df = df.dropna()
    
    # 필수 컬럼 확인
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"필수 컬럼이 누락되었습니다: {', '.join(missing)}")
    
    return df

def safe_operation(func):
    """함수 실행을 안전하게 감싸는 데코레이터"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"작업 중 오류가 발생했습니다: {str(e)}")
            return None
    return wrapper

def validate_data_types(df, column_types):
    """데이터 타입 검증"""
    errors = []
    for column, expected_type in column_types.items():
        if column in df.columns:
            if expected_type == 'numeric':
                if not pd.api.types.is_numeric_dtype(df[column]):
                    errors.append(f"'{column}' 컬럼은 숫자 형태여야 합니다.")
            elif expected_type == 'datetime':
                try:
                    pd.to_datetime(df[column])
                except:
                    errors.append(f"'{column}' 컬럼은 날짜 형태여야 합니다.")
    
    if errors:
        raise ValueError("\\n".join(errors))
    
    return True

def format_number(value, decimals=2):
    """숫자 포맷팅"""
    if pd.isna(value):
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{value:,.{decimals}f}"
    return str(value)

def create_download_link(df, filename="data.xlsx"):
    """Excel 다운로드 링크 생성"""
    from io import BytesIO
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    excel_data = output.getvalue()
    
    st.download_button(
        label="📥 Excel 파일 다운로드",
        data=excel_data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
