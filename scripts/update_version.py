#!/usr/bin/env python3
"""
SPsystems 다기능 분석 도구 - 버전 관리 스크립트
자동으로 버전을 업데이트하고 관련 파일들을 수정합니다.
"""

import json
import re
import argparse
import datetime
from pathlib import Path
import subprocess
import sys

class VersionManager:
    def __init__(self, project_root=None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent
        self.package_json_path = self.project_root / "package.json"
        self.streamlit_app_path = self.project_root / "streamlit_app.py"
        self.readme_path = self.project_root / "README.md"
        self.version_file_path = self.project_root / "VERSION"
        
    def load_package_json(self):
        """package.json 파일 로드"""
        with open(self.package_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_package_json(self, data):
        """package.json 파일 저장"""
        with open(self.package_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_current_version(self):
        """현재 버전 가져오기"""
        package_data = self.load_package_json()
        return package_data.get('version', '1.0.0')
    
    def parse_version(self, version_str):
        """버전 문자열을 major.minor.patch로 분석"""
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str)
        if not match:
            raise ValueError(f"잘못된 버전 형식: {version_str}")
        return tuple(map(int, match.groups()))
    
    def increment_version(self, version_type='patch'):
        """버전 증가"""
        current_version = self.get_current_version()
        major, minor, patch = self.parse_version(current_version)
        
        if version_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif version_type == 'minor':
            minor += 1
            patch = 0
        elif version_type == 'patch':
            patch += 1
        else:
            raise ValueError(f"잘못된 버전 타입: {version_type}")
        
        return f"{major}.{minor}.{patch}"
    
    def update_package_json(self, new_version, changelog_entry=None):
        """package.json 업데이트"""
        package_data = self.load_package_json()
        old_version = package_data.get('version', '1.0.0')
        package_data['version'] = new_version
        
        # 체인지로그 업데이트
        if changelog_entry:
            if 'changelog' not in package_data:
                package_data['changelog'] = {}
            
            package_data['changelog'][new_version] = {
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'changes': changelog_entry if isinstance(changelog_entry, list) else [changelog_entry]
            }
        
        self.save_package_json(package_data)
        print(f"✅ package.json 버전 업데이트: {old_version} → {new_version}")
    
    def update_streamlit_app(self, new_version):
        """streamlit_app.py의 버전 정보 업데이트"""
        if not self.streamlit_app_path.exists():
            print("⚠️ streamlit_app.py 파일을 찾을 수 없습니다.")
            return
        
        with open(self.streamlit_app_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 버전 정보 업데이트
        version_pattern = r'st\.markdown\("(\*\*Version:\*\*) ([^"]+)"\)'
        new_version_line = f'st.markdown("**Version:** {new_version}")'
        
        if re.search(version_pattern, content):
            content = re.sub(version_pattern, new_version_line, content)
            
            with open(self.streamlit_app_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ streamlit_app.py 버전 업데이트: {new_version}")
        else:
            print("⚠️ streamlit_app.py에서 버전 정보를 찾을 수 없습니다.")
    
    def update_readme(self, new_version):
        """README.md의 버전 정보 업데이트"""
        if not self.readme_path.exists():
            print("⚠️ README.md 파일을 찾을 수 없습니다.")
            return
        
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 버전 정보 업데이트 (여러 패턴 지원)
        patterns = [
            (r'### v(\d+\.\d+\.\d+)', f'### v{new_version}'),
            (r'\*\*버전\*\*: (\d+\.\d+\.\d+)', f'**버전**: {new_version}'),
            (r'- \*\*Version\*\*: (\d+\.\d+\.\d+)', f'- **Version**: {new_version}')
        ]
        
        updated = False
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                updated = True
        
        if updated:
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ README.md 버전 업데이트: {new_version}")
        else:
            print("⚠️ README.md에서 버전 정보를 찾을 수 없습니다.")
    
    def create_version_file(self, new_version):
        """VERSION 파일 생성/업데이트"""
        version_info = {
            "version": new_version,
            "build_date": datetime.datetime.now().isoformat(),
            "git_commit": self.get_git_commit(),
            "developer": "SPsystems 연구소 개발팀"
        }
        
        with open(self.version_file_path, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ VERSION 파일 생성: {new_version}")
    
    def get_git_commit(self):
        """현재 Git 커밋 해시 가져오기"""
        try:
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except:
            return "unknown"
    
    def create_git_tag(self, version, message=None):
        """Git 태그 생성"""
        try:
            tag_message = message or f"Release v{version}"
            subprocess.run(['git', 'tag', '-a', f'v{version}', '-m', tag_message], 
                          cwd=self.project_root, check=True)
            print(f"✅ Git 태그 생성: v{version}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Git 태그 생성 실패: v{version}")
        except FileNotFoundError:
            print("⚠️ Git이 설치되지 않았거나 Git 저장소가 아닙니다.")
    
    def update_version(self, version_type='patch', changelog=None, create_tag=False):
        """전체 버전 업데이트 프로세스"""
        current_version = self.get_current_version()
        new_version = self.increment_version(version_type)
        
        print(f"🚀 버전 업데이트: {current_version} → {new_version}")
        print(f"📅 업데이트 일시: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 각 파일 업데이트
        self.update_package_json(new_version, changelog)
        self.update_streamlit_app(new_version)
        self.update_readme(new_version)
        self.create_version_file(new_version)
        
        if create_tag:
            tag_message = f"Release v{new_version}"
            if changelog:
                tag_message += f"\n\n변경사항:\n" + "\n".join(f"- {change}" for change in changelog)
            self.create_git_tag(new_version, tag_message)
        
        print(f"🎉 버전 업데이트 완료: v{new_version}")
        return new_version

def main():
    parser = argparse.ArgumentParser(description='SPsystems 다기능 분석 도구 버전 관리')
    parser.add_argument('--type', choices=['major', 'minor', 'patch'], default='patch',
                       help='업데이트할 버전 타입 (기본값: patch)')
    parser.add_argument('--changelog', nargs='+', 
                       help='변경사항 설명 (여러 개 가능)')
    parser.add_argument('--tag', action='store_true',
                       help='Git 태그 생성')
    parser.add_argument('--current', action='store_true',
                       help='현재 버전만 표시')
    
    args = parser.parse_args()
    
    vm = VersionManager()
    
    if args.current:
        current_version = vm.get_current_version()
        print(f"현재 버전: v{current_version}")
        return
    
    try:
        new_version = vm.update_version(
            version_type=args.type,
            changelog=args.changelog,
            create_tag=args.tag
        )
        
        print(f"\n📋 다음 단계:")
        print(f"1. 변경사항 커밋: git add . && git commit -m 'chore: bump version to {new_version}'")
        if args.tag:
            print(f"2. 태그 푸시: git push origin v{new_version}")
        print(f"3. 메인 브랜치 푸시: git push")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
