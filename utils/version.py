"""
버전 정보를 관리하는 유틸리티 모듈
"""
import json
import os
from pathlib import Path

def get_version_info():
    """VERSION 파일에서 버전 정보를 읽어옵니다."""
    try:
        version_file = Path(__file__).parent.parent / "VERSION"
        if version_file.exists():
            with open(version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # VERSION 파일이 없으면 package.json에서 읽기
            package_file = Path(__file__).parent.parent / "package.json"
            if package_file.exists():
                with open(package_file, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    return {
                        "version": package_data.get("version", "2.1.0"),
                        "developer": package_data.get("author", "SPsystems 연구소 개발팀"),
                        "build_date": "unknown",
                        "git_commit": "unknown"
                    }
    except Exception:
        pass
    
    # 기본값 반환
    return {
        "version": "2.1.0",
        "developer": "SPsystems 연구소 개발팀",
        "build_date": "unknown",
        "git_commit": "unknown"
    }

def get_app_version():
    """애플리케이션 버전 반환"""
    return get_version_info().get("version", "2.1.0")

def get_developer():
    """개발팀 정보 반환"""
    return get_version_info().get("developer", "SPsystems 연구소 개발팀")

def get_build_info():
    """빌드 정보 반환"""
    version_info = get_version_info()
    return {
        "version": version_info.get("version", "2.1.0"),
        "build_date": version_info.get("build_date", "unknown"),
        "git_commit": version_info.get("git_commit", "unknown")[:8] if version_info.get("git_commit") != "unknown" else "unknown"
    }
