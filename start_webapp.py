"""
🚀 GANTY-LODER 프로젝트 BOM 분석 웹앱 시작 가이드

이 스크립트를 실행하면:
1. 프로젝트 분석 엑셀 파일 생성
2. BOM 입력 템플릿 파일 생성
3. Streamlit 웹앱 실행

실행 방법:
python start_webapp.py
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """필요한 패키지 설치"""
    try:
        print("📦 필요한 패키지 설치 중...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 패키지 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패: {e}")
        return False

def create_excel_files():
    """엑셀 파일 생성"""
    try:
        print("📊 엑셀 파일 생성 중...")
        subprocess.check_call([sys.executable, "create_excel_files.py"])
        print("✅ 엑셀 파일 생성 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 엑셀 파일 생성 실패: {e}")
        return False
    except FileNotFoundError:
        print("⚠️ create_excel_files.py 파일을 찾을 수 없습니다.")
        return False

def start_streamlit():
    """Streamlit 웹앱 시작"""
    try:
        print("🚀 Streamlit 웹앱 시작 중...")
        print("🌐 브라우저에서 http://localhost:8501 으로 접속하세요")
        print("⚠️ 종료하려면 Ctrl+C를 누르세요")
        subprocess.call([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 웹앱을 종료합니다.")
    except Exception as e:
        print(f"❌ 웹앱 시작 실패: {e}")

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🛠️  GANTY-LODER 프로젝트 BOM 분석 웹앱")
    print("   ABB TSU Team - 프로젝트 분석 도구")
    print("=" * 60)
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    print(f"📁 현재 디렉토리: {current_dir}")
    
    # requirements.txt 파일 확인
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt 파일이 없습니다.")
        return
    
    # streamlit_app.py 파일 확인
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py 파일이 없습니다.")
        return
    
    print("\n🔧 설정 확인 완료!")
    print("─" * 60)
    
    # 1. 패키지 설치
    if not install_requirements():
        print("💡 패키지 설치가 실패했습니다. 수동으로 설치하세요:")
        print("   pip install -r requirements.txt")
        return
    
    print("─" * 60)
    
    # 2. 엑셀 파일 생성 (선택사항)
    create_excel_files()
    
    print("─" * 60)
    
    # 3. Streamlit 앱 시작
    print("📋 사용 가능한 기능:")
    print("   • 기본 프로젝트 데이터 분석")
    print("   • 엑셀 파일 업로드 및 분석")
    print("   • BOM 분석 템플릿 다운로드")
    print("   • 인터랙티브 차트 및 시각화")
    print("   • 분석 결과 다운로드")
    
    print("\n🎯 웹앱 사용법:")
    print("   1. 브라우저에서 사이드바의 '📈 프로젝트 분석' 선택")
    print("   2. '기본 데이터 분석' 탭에서 샘플 데이터 확인")
    print("   3. '파일 업로드 분석' 탭에서 자신의 BOM 파일 분석")
    print("   4. '도구 및 템플릿' 탭에서 템플릿 다운로드")
    
    print("\n" + "─" * 60)
    
    start_streamlit()

if __name__ == "__main__":
    main()
