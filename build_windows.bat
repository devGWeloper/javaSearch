@echo off
chcp 65001 >nul
echo 🔨 Java Search Tool Windows EXE 빌더
echo ==========================================

REM Python 환경 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo Python 3.8+를 설치해주세요.
    pause
    exit /b 1
)

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 🐍 가상환경을 활성화합니다...
    call venv\Scripts\activate.bat
)

REM 의존성 설치
echo 📦 필요한 패키지를 설치합니다...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ 패키지 설치에 실패했습니다.
    pause
    exit /b 1
)

REM 기존 빌드 파일 정리
echo 🧹 기존 빌드 파일을 정리합니다...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

REM Windows용 최적화된 실행 파일 생성
echo 🪟 Windows용 최적화된 실행 파일을 생성합니다...
python build_executable.py --windows

if errorlevel 1 (
    echo ❌ 빌드에 실패했습니다.
    pause
    exit /b 1
)

REM 배포 패키지 생성
echo 📦 배포 패키지를 생성합니다...
python create_package.py --windows

echo.
echo ✅ Windows EXE 빌드가 완료되었습니다!
echo 📁 실행 파일 위치: dist\JavaSearchTool\
echo 🚀 실행 방법: dist\JavaSearchTool\JavaSearchTool.exe 더블클릭
echo.
echo 💡 성능 최적화 팁:
echo    - 첫 실행 시 Windows Defender가 차단할 수 있습니다
echo    - 실행 파일을 신뢰할 수 있는 항목에 추가하세요
echo    - SSD에 설치하면 더 빠른 시작이 가능합니다
echo.
pause
