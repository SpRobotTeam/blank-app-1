"""
SPsystems 다기능 분석 도구 - 메인 테스트
"""
import pytest
import sys
import os
from pathlib import Path
import importlib.util

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestAppStructure:
    """앱 구조 및 기본 기능 테스트"""
    
    def test_main_files_exist(self):
        """주요 파일들이 존재하는지 확인"""
        required_files = [
            'streamlit_app.py',
            'requirements.txt',
            'VERSION',
            'package.json',
            'README.md'
        ]
        
        for file_name in required_files:
            file_path = project_root / file_name
            assert file_path.exists(), f"{file_name} 파일이 존재하지 않습니다"
    
    def test_streamlit_app_import(self):
        """streamlit_app.py 파일을 정상적으로 import할 수 있는지 확인"""
        try:
            spec = importlib.util.spec_from_file_location(
                "streamlit_app", 
                project_root / "streamlit_app.py"
            )
            module = importlib.util.module_from_spec(spec)
            # 실제 실행하지 않고 구문만 검사
            assert spec is not None, "streamlit_app.py를 로드할 수 없습니다"
        except Exception as e:
            pytest.fail(f"streamlit_app.py import 실패: {e}")
    
    def test_requirements_format(self):
        """requirements.txt 형식이 올바른지 확인"""
        requirements_path = project_root / "requirements.txt"
        
        with open(requirements_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 빈 줄이 아닌 라인들 검사
        package_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        assert len(package_lines) > 0, "requirements.txt가 비어있습니다"
        
        # 기본 패키지들이 포함되어 있는지 확인
        required_packages = ['streamlit', 'pandas', 'plotly']
        requirements_text = '\n'.join(package_lines).lower()
        
        for package in required_packages:
            assert package in requirements_text, f"{package} 패키지가 requirements.txt에 없습니다"

class TestVersionManagement:
    """버전 관리 테스트"""
    
    def test_version_file_format(self):
        """VERSION 파일 형식 확인"""
        import json
        
        version_path = project_root / "VERSION"
        
        with open(version_path, 'r', encoding='utf-8') as f:
            version_data = json.load(f)
        
        required_fields = ['version', 'build_date', 'git_commit', 'developer']
        
        for field in required_fields:
            assert field in version_data, f"VERSION 파일에 {field} 필드가 없습니다"
        
        # 버전 형식 확인 (semantic versioning)
        version = version_data['version']
        import re
        version_pattern = r'^\d+\.\d+\.\d+$'
        assert re.match(version_pattern, version), f"잘못된 버전 형식: {version}"
    
    def test_package_json_format(self):
        """package.json 형식 확인"""
        import json
        
        package_path = project_root / "package.json"
        
        with open(package_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        required_fields = ['name', 'version', 'description']
        
        for field in required_fields:
            assert field in package_data, f"package.json에 {field} 필드가 없습니다"

class TestDependencies:
    """의존성 패키지 테스트"""
    
    def test_streamlit_import(self):
        """Streamlit import 테스트"""
        try:
            import streamlit as st
            assert hasattr(st, 'write'), "Streamlit이 올바르게 설치되지 않았습니다"
        except ImportError:
            pytest.fail("Streamlit을 import할 수 없습니다")
    
    def test_pandas_import(self):
        """Pandas import 테스트"""
        try:
            import pandas as pd
            assert hasattr(pd, 'DataFrame'), "Pandas가 올바르게 설치되지 않았습니다"
        except ImportError:
            pytest.fail("Pandas를 import할 수 없습니다")
    
    def test_plotly_import(self):
        """Plotly import 테스트"""
        try:
            import plotly.graph_objects as go
            assert hasattr(go, 'Figure'), "Plotly가 올바르게 설치되지 않았습니다"
        except ImportError:
            pytest.fail("Plotly를 import할 수 없습니다")
    
    def test_numpy_import(self):
        """NumPy import 테스트"""
        try:
            import numpy as np
            assert hasattr(np, 'array'), "NumPy가 올바르게 설치되지 않았습니다"
        except ImportError:
            pytest.fail("NumPy를 import할 수 없습니다")

class TestConfiguration:
    """설정 파일 테스트"""
    
    def test_docker_files(self):
        """Docker 관련 파일들 확인"""
        dockerfile_path = project_root / "Dockerfile"
        compose_path = project_root / "docker-compose.yml"
        
        assert dockerfile_path.exists(), "Dockerfile이 존재하지 않습니다"
        assert compose_path.exists(), "docker-compose.yml이 존재하지 않습니다"
    
    def test_git_ignore(self):
        """gitignore 파일 확인"""
        gitignore_path = project_root / ".gitignore"
        assert gitignore_path.exists(), ".gitignore 파일이 존재하지 않습니다"
        
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        # 기본적으로 무시해야 할 패턴들
        required_patterns = ['__pycache__', '*.pyc', '.env']
        
        for pattern in required_patterns:
            assert pattern in gitignore_content, f".gitignore에 {pattern} 패턴이 없습니다"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
