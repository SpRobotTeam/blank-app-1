import streamlit as st
import time
import functools

def timed_cache(seconds=600):
    """
    지정된 시간(초) 동안 함수 결과를 캐시하는 데코레이터
    """
    def decorator(func):
        # 캐시와 타임스탬프 저장용 딕셔너리
        cache = {}
        timestamps = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 함수 호출에 대한 고유 키 생성
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            # 캐시 항목 만료 확인
            if key in cache and current_time - timestamps[key] < seconds:
                return cache[key]
            
            # 캐시 항목이 없거나 만료된 경우 함수 실행
            result = func(*args, **kwargs)
            cache[key] = result
            timestamps[key] = current_time
            return result
        
        return wrapper
    
    return decorator

def lazy_load_data(file_path, loader_func, *args, **kwargs):
    """
    필요할 때만 데이터를 로드하고 세션에 캐싱
    """
    cache_key = f"data_cache_{file_path}"
    if cache_key not in st.session_state:
        with st.spinner(f"데이터 로드 중..."):
            st.session_state[cache_key] = loader_func(file_path, *args, **kwargs)
    
    return st.session_state[cache_key]

@st.cache_data
def load_csv_cached(file_path):
    """CSV 파일을 캐시와 함께 로드"""
    import pandas as pd
    return pd.read_csv(file_path)

@st.cache_data
def load_excel_cached(file_path, sheet_name=0):
    """Excel 파일을 캐시와 함께 로드"""
    import pandas as pd
    return pd.read_excel(file_path, sheet_name=sheet_name)

def progress_bar_wrapper(iterable, desc="처리 중..."):
    """진행률 표시가 포함된 반복문 래퍼"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total = len(iterable)
    for i, item in enumerate(iterable):
        progress = (i + 1) / total
        progress_bar.progress(progress)
        status_text.text(f"{desc} {i + 1}/{total}")
        yield item
    
    progress_bar.empty()
    status_text.empty()
