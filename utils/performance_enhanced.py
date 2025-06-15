"""
성능 최적화 및 모니터링 유틸리티
"""
import streamlit as st
import time
import psutil
import functools
import logging
from typing import Any, Callable, Dict, Optional

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/performance.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def performance_monitor(func: Callable) -> Callable:
    """함수 실행 시간 및 리소스 사용량 모니터링"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_diff = end_memory - start_memory
            
            logger.info(f"Function {func.__name__}: "
                       f"Time={execution_time:.2f}s, "
                       f"Memory={memory_diff:+.2f}MB")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    
    return wrapper

@st.cache_data(ttl=3600)  # 1시간 캐시
def cached_data_loader(file_path: str) -> Dict[str, Any]:
    """캐시된 데이터 로더"""
    import json
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def cached_dataframe_processor(df_dict: dict) -> Any:
    """캐시된 데이터프레임 처리"""
    import pandas as pd
    return pd.DataFrame(df_dict)

def display_performance_metrics():
    """성능 지표 표시"""
    if st.sidebar.checkbox("🔍 성능 모니터링"):
        col1, col2, col3 = st.sidebar.columns(3)
        
        # CPU 사용률
        cpu_percent = psutil.cpu_percent(interval=1)
        col1.metric("CPU", f"{cpu_percent:.1f}%")
        
        # 메모리 사용률
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        col2.metric("Memory", f"{memory_percent:.1f}%")
        
        # 캐시 상태
        cache_info = st.cache_data.clear.__doc__  # 간단한 캐시 정보
        col3.metric("Cache", "Active")

def optimize_dataframe_display(df, max_rows: int = 1000):
    """대용량 데이터프레임 최적화 표시"""
    if len(df) > max_rows:
        st.warning(f"⚠️ 데이터가 {len(df):,}행으로 많습니다. 처음 {max_rows:,}행만 표시합니다.")
        return df.head(max_rows)
    return df

def memory_efficient_chart(data, chart_type: str = "line"):
    """메모리 효율적인 차트 생성"""
    import plotly.express as px
    
    # 데이터 크기에 따른 샘플링
    if len(data) > 10000:
        sample_size = min(5000, len(data) // 2)
        data_sampled = data.sample(n=sample_size).sort_index()
        st.info(f"📊 성능 최적화를 위해 {sample_size:,}개 점을 샘플링했습니다.")
    else:
        data_sampled = data
    
    if chart_type == "line":
        return px.line(data_sampled)
    elif chart_type == "scatter":
        return px.scatter(data_sampled)
    else:
        return px.bar(data_sampled)

class SessionStateManager:
    """세션 상태 관리자"""
    
    @staticmethod
    def initialize_state(key: str, default_value: Any):
        """세션 상태 초기화"""
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    @staticmethod
    def cleanup_old_states(keep_keys: list):
        """오래된 세션 상태 정리"""
        keys_to_remove = []
        for key in st.session_state.keys():
            if key not in keep_keys:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    @staticmethod
    def get_memory_usage():
        """세션 상태 메모리 사용량 계산"""
        import sys
        total_size = 0
        for key, value in st.session_state.items():
            total_size += sys.getsizeof(value)
        return total_size / 1024 / 1024  # MB

def error_boundary(func: Callable) -> Callable:
    """에러 경계 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            st.error(f"❌ 오류가 발생했습니다: {str(e)}")
            st.info("💡 페이지를 새로고침하거나 관리자에게 문의하세요.")
            return None
    return wrapper

# 전역 성능 설정
if 'performance_monitoring' not in st.session_state:
    st.session_state.performance_monitoring = False

def enable_performance_mode():
    """성능 모니터링 모드 활성화"""
    st.session_state.performance_monitoring = True
    display_performance_metrics()
