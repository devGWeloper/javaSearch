#!/usr/bin/env python3
"""
Java Search Tool 실행 파일 생성 스크립트
PyInstaller를 사용하여 독립 실행 파일을 생성합니다.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable(target_platform=None):
    """실행 파일을 생성합니다."""
    
    # 프로젝트 루트 디렉토리
    project_root = Path(__file__).parent
    main_file = project_root / "main.py"
    
    # 빌드 디렉토리
    build_dir = project_root / "build"
    dist_dir = project_root / "dist"
    
    # 기존 빌드 파일 정리
    if build_dir.exists():
        print("기존 빌드 파일을 정리합니다...")
        shutil.rmtree(build_dir)
    
    if dist_dir.exists():
        print("기존 배포 파일을 정리합니다...")
        shutil.rmtree(dist_dir)
    
    # PyInstaller 명령어 구성
    cmd = [
        "pyinstaller",
        "--onefile",                    # 단일 실행 파일로 생성
        "--windowed",                   # GUI 모드 (콘솔 창 숨김)
        "--name=JavaSearchTool",        # 실행 파일 이름
        "--add-data=assets:assets",    # assets 폴더 포함
        "--hidden-import=customtkinter",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=PIL",
        "--hidden-import=src.gui.main_window",
        "--hidden-import=src.gui.search_panel",
        "--hidden-import=src.gui.results_panel",
        "--hidden-import=src.gui.event_handlers",
        "--hidden-import=src.gui.settings_manager",
        "--hidden-import=src.core.search_engine",
        "--hidden-import=src.core.config_manager",
        "--clean",                      # 임시 파일 정리
        str(main_file)
    ]
    
    # 아이콘 추가 (있는 경우)
    icon_path = project_root / "assets" / "icon.ico"
    if icon_path.exists():
        cmd.append(f"--icon={icon_path}")
    
    # 크로스 플랫폼 빌드 옵션 (Windows에서만 사용)
    if target_platform and target_platform == "windows":
        print("🪟 Windows용 실행 파일을 생성합니다...")
        # Windows에서는 x86_64 타겟 아키텍처 사용
        cmd.extend(["--target-arch=x86_64"])
    elif target_platform and target_platform == "macos":
        print("🍎 macOS용 실행 파일을 생성합니다...")
        # macOS에서는 현재 아키텍처 사용 (arm64 또는 x86_64)
        # 타겟 아키텍처 옵션 제거하여 자동 감지
    else:
        # 현재 플랫폼 감지
        if sys.platform.startswith('darwin'):
            print("🍎 macOS용 실행 파일을 생성합니다...")
        else:
            print("🪟 Windows용 실행 파일을 생성합니다...")
    
    print("PyInstaller로 실행 파일을 생성합니다...")
    print(f"명령어: {' '.join(cmd)}")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 실행 파일 생성 완료!")
            
            # 생성된 파일 확인
            if sys.platform.startswith('darwin'):  # macOS
                executable_path = dist_dir / "JavaSearchTool"
                if executable_path.exists():
                    print(f"📁 실행 파일 위치: {executable_path}")
                    print("🚀 실행 방법: Finder에서 더블클릭하거나 터미널에서 ./dist/JavaSearchTool 실행")
                else:
                    print("❌ 실행 파일을 찾을 수 없습니다.")
            else:  # Windows
                executable_path = dist_dir / "JavaSearchTool.exe"
                if executable_path.exists():
                    print(f"📁 실행 파일 위치: {executable_path}")
                    print("🚀 실행 방법: 더블클릭으로 실행")
                else:
                    print("❌ 실행 파일을 찾을 수 없습니다.")
            
            # 배포용 폴더 생성
            platform_name = "Windows" if target_platform == "windows" else "macOS"
            deploy_dir = project_root / f"deploy_{platform_name.lower()}"
            if deploy_dir.exists():
                shutil.rmtree(deploy_dir)
            
            deploy_dir.mkdir(exist_ok=True)
            
            # 실행 파일을 배포 폴더로 복사
            if executable_path.exists():
                shutil.copy2(executable_path, deploy_dir)
                print(f"📦 배포 폴더에 복사됨: {deploy_dir}")
            
            # README 파일 생성
            readme_content = f"""# Java Search Tool 실행 파일 ({platform_name})

## 실행 방법
1. `JavaSearchTool{' (macOS)' if platform_name == 'macOS' else '.exe (Windows)'}` 파일을 더블클릭하여 실행
2. Python 설치가 필요하지 않습니다

## 시스템 요구사항
- {platform_name} 10+
- 최소 4GB RAM
- 100MB 이상의 디스크 공간

## 주의사항
- 처음 실행 시 보안 경고가 나타날 수 있습니다
- {platform_name}에서는 보안 설정에서 실행을 허용해야 할 수 있습니다

## 문제 해결
- 실행이 안 되는 경우: 터미널/명령 프롬프트에서 실행하여 오류 메시지 확인
- 권한 문제: 파일 속성에서 실행 권한 확인

생성일: {Path(__file__).stat().st_mtime}
"""
            
            readme_path = deploy_dir / "README.txt"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"📖 README 파일 생성됨: {readme_path}")
            
        else:
            print("❌ 실행 파일 생성 실패!")
            print("오류 출력:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 빌드 중 오류 발생: {e}")
        return False
    
    return True

def build_cross_platform():
    """크로스 플랫폼 실행 파일을 생성합니다."""
    print("🌍 크로스 플랫폼 실행 파일을 생성합니다...")
    
    # 현재 플랫폼용 실행 파일 생성
    current_platform = "macos" if sys.platform.startswith('darwin') else "windows"
    print(f"현재 플랫폼: {current_platform}")
    
    # 현재 플랫폼용 빌드
    if build_executable(current_platform):
        print(f"✅ {current_platform}용 실행 파일 생성 완료!")
    
    # Windows용 빌드 (macOS에서 실행 중인 경우)
    if sys.platform.startswith('darwin'):
        print("\n🪟 Windows용 실행 파일을 생성합니다...")
        print("⚠️  주의: macOS에서 Windows용 실행 파일을 생성할 수 없습니다.")
        print("Windows 환경에서 직접 빌드하거나, Docker를 사용해야 합니다.")
        
        # Windows용 빌드 가이드 생성
        create_windows_build_guide()
    
    return True

def create_windows_build_guide():
    """Windows용 빌드 가이드를 생성합니다."""
    guide_content = """# Windows용 실행 파일 빌드 가이드

## Windows 환경에서 빌드하기

### 1. 필요 조건
- Windows 10/11
- Python 3.8+
- pip

### 2. 설치 및 빌드
```cmd
# 저장소 클론
git clone <repository-url>
cd javaSearch

# 의존성 설치
pip install -r requirements.txt

# Windows용 실행 파일 생성
python build_executable.py --windows

# 배포 패키지 생성
python create_package.py --windows
```

### 3. 생성된 파일
- `dist/JavaSearchTool.exe` - Windows 실행 파일
- `deploy_windows/` - Windows용 배포 폴더
- `JavaSearchTool_Windows_YYYYMMDD_HHMMSS.zip` - 배포 패키지

## Docker를 사용한 크로스 컴파일 (고급)

### 1. Dockerfile 생성
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python build_executable.py --windows
```

### 2. Docker 빌드
```bash
docker build -t java-search-builder .
docker run -v $(pwd):/app java-search-builder
```

## 문제 해결

### 빌드 실패 시
1. Python 버전 확인 (3.8+ 필요)
2. 의존성 패키지 재설치
3. 관리자 권한으로 실행
4. 바이러스 백신 비활성화 (일시적)

### 실행 파일이 작동하지 않는 경우
1. Visual C++ Redistributable 설치
2. .NET Framework 확인
3. Windows Defender 예외 추가
"""
    
    guide_path = Path(__file__).parent / "WINDOWS_BUILD_GUIDE.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"📖 Windows 빌드 가이드 생성됨: {guide_path}")

def clean_build_files():
    """빌드 관련 임시 파일들을 정리합니다."""
    project_root = Path(__file__).parent
    
    # 정리할 파일/폴더들
    cleanup_items = [
        "build",
        "dist", 
        "*.spec"
    ]
    
    print("빌드 임시 파일을 정리합니다...")
    
    for item in cleanup_items:
        if "*" in item:
            # 와일드카드 패턴
            for file_path in project_root.glob(item):
                if file_path.is_file():
                    file_path.unlink()
                    print(f"삭제됨: {file_path}")
        else:
            # 단일 폴더/파일
            path = project_root / item
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"삭제됨: {path}")

if __name__ == "__main__":
    print("🔨 Java Search Tool 실행 파일 빌더")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--clean":
            clean_build_files()
        elif sys.argv[1] == "--windows":
            build_executable("windows")
        elif sys.argv[1] == "--macos":
            build_executable("macos")
        elif sys.argv[1] == "--cross-platform":
            build_cross_platform()
        else:
            print("사용법:")
            print("  python build_executable.py              # 현재 플랫폼용 빌드")
            print("  python build_executable.py --windows    # Windows용 빌드")
            print("  python build_executable.py --macos      # macOS용 빌드")
            print("  python build_executable.py --cross-platform  # 크로스 플랫폼 빌드")
            print("  python build_executable.py --clean      # 빌드 파일 정리")
    else:
        # 기본: 현재 플랫폼용 빌드
        current_platform = "macos" if sys.platform.startswith('darwin') else "windows"
        build_executable(current_platform)
        
        print("\n" + "=" * 50)
        print("빌드 완료! 다른 사람과 공유할 수 있는 실행 파일이 생성되었습니다.")
        print("정리하려면: python build_executable.py --clean")
        print("Windows용 빌드: python build_executable.py --windows")
        print("크로스 플랫폼: python build_executable.py --cross-platform")
