#!/usr/bin/env python3
"""
Java Search Tool 배포 패키지 생성 스크립트
실행 파일과 필요한 파일들을 압축하여 배포용 패키지를 만듭니다.
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_package(target_platform=None):
    """배포용 패키지를 생성합니다."""
    
    project_root = Path(__file__).parent
    
    # 플랫폼별 배포 폴더 결정
    if target_platform:
        deploy_dir = project_root / f"deploy_{target_platform.lower()}"
        platform_name = "Windows" if target_platform == "windows" else "macOS"
    else:
        # 현재 플랫폼 감지
        current_platform = "macos" if sys.platform.startswith('darwin') else "windows"
        deploy_dir = project_root / f"deploy_{current_platform.lower()}"
        platform_name = "Windows" if current_platform == "windows" else "macOS"
    
    if not deploy_dir.exists():
        print(f"❌ {platform_name}용 배포 폴더가 없습니다.")
        print(f"먼저 다음 명령어로 실행 파일을 생성해주세요:")
        if target_platform:
            print(f"python build_executable.py --{target_platform}")
        else:
            print("python build_executable.py")
        return False
    
    # 패키지 이름 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"JavaSearchTool_{platform_name}_{timestamp}"
    package_path = project_root / f"{package_name}.zip"
    
    print(f"📦 {platform_name}용 배포 패키지를 생성합니다: {package_name}")
    
    try:
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # deploy 폴더의 모든 파일을 압축
            for file_path in deploy_dir.rglob('*'):
                if file_path.is_file():
                    # 상대 경로로 압축
                    arcname = file_path.relative_to(deploy_dir)
                    zipf.write(file_path, arcname)
                    print(f"  📁 압축됨: {arcname}")
        
        print(f"✅ {platform_name}용 패키지 생성 완료: {package_path}")
        
        # 파일 크기 표시
        size_mb = package_path.stat().st_size / (1024 * 1024)
        print(f"📊 패키지 크기: {size_mb:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ 패키지 생성 실패: {e}")
        return False

def create_cross_platform_packages():
    """모든 플랫폼용 배포 패키지를 생성합니다."""
    print("🌍 크로스 플랫폼 배포 패키지를 생성합니다...")
    
    # 현재 플랫폼용 패키지 생성
    current_platform = "macos" if sys.platform.startswith('darwin') else "windows"
    print(f"현재 플랫폼: {current_platform}")
    
    if create_package(current_platform):
        print(f"✅ {current_platform}용 패키지 생성 완료!")
    
    # Windows용 패키지 (macOS에서 실행 중인 경우)
    if sys.platform.startswith('darwin'):
        print("\n🪟 Windows용 패키지를 생성합니다...")
        if create_package("windows"):
            print("✅ Windows용 패키지 생성 완료!")
        else:
            print("⚠️  Windows용 실행 파일이 없습니다.")
            print("Windows 환경에서 직접 빌드하거나, Docker를 사용해야 합니다.")
    
    return True

def clean_packages():
    """생성된 패키지 파일들을 정리합니다."""
    project_root = Path(__file__).parent
    
    # .zip 파일들 찾기
    zip_files = list(project_root.glob("JavaSearchTool_*.zip"))
    
    if not zip_files:
        print("정리할 패키지 파일이 없습니다.")
        return
    
    print("생성된 패키지 파일들을 정리합니다...")
    
    for zip_file in zip_files:
        zip_file.unlink()
        print(f"삭제됨: {zip_file.name}")

def list_packages():
    """생성된 패키지 파일들을 나열합니다."""
    project_root = Path(__file__).parent
    
    # .zip 파일들 찾기
    zip_files = list(project_root.glob("JavaSearchTool_*.zip"))
    
    if not zip_files:
        print("생성된 패키지 파일이 없습니다.")
        return
    
    print("생성된 패키지 파일들:")
    print("-" * 50)
    
    for zip_file in sorted(zip_files, key=lambda x: x.stat().st_mtime, reverse=True):
        size_mb = zip_file.stat().st_size / (1024 * 1024)
        mtime = datetime.fromtimestamp(zip_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"📦 {zip_file.name}")
        print(f"   크기: {size_mb:.1f} MB")
        print(f"   생성일: {mtime}")
        print()

if __name__ == "__main__":
    print("📦 Java Search Tool 배포 패키지 생성기")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--clean":
            clean_packages()
        elif sys.argv[1] == "--windows":
            create_package("windows")
        elif sys.argv[1] == "--macos":
            create_package("macos")
        elif sys.argv[1] == "--cross-platform":
            create_cross_platform_packages()
        elif sys.argv[1] == "--list":
            list_packages()
        else:
            print("사용법:")
            print("  python create_package.py              # 현재 플랫폼용 패키지 생성")
            print("  python create_package.py --windows    # Windows용 패키지 생성")
            print("  python create_package.py --macos      # macOS용 패키지 생성")
            print("  python create_package.py --cross-platform  # 크로스 플랫폼 패키지 생성")
            print("  python create_package.py --list       # 패키지 목록 표시")
            print("  python create_package.py --clean      # 패키지 파일 정리")
    else:
        # 기본: 현재 플랫폼용 패키지 생성
        if create_package():
            print("\n" + "=" * 50)
            print("🎉 배포 패키지가 성공적으로 생성되었습니다!")
            print("이제 다른 사람과 공유할 수 있습니다.")
            print("\n추가 옵션:")
            print("  정리: python create_package.py --clean")
            print("  Windows용: python create_package.py --windows")
            print("  크로스 플랫폼: python create_package.py --cross-platform")
            print("  목록 보기: python create_package.py --list")
        else:
            print("\n❌ 패키지 생성에 실패했습니다.")
