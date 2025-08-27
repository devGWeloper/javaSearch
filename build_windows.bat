@echo off
chcp 65001 >nul
echo 🪟 Windows용 Java Search Tool 실행 파일 빌더
echo ================================================

REM Python이 설치되어 있는지 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo Python 3.8+를 먼저 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python 환경 확인 완료

REM pip가 설치되어 있는지 확인
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip가 설치되어 있지 않습니다.
    echo pip를 설치해주세요.
    pause
    exit /b 1
)

echo ✅ pip 환경 확인 완료

REM 필요한 패키지 설치
echo 📦 필요한 패키지를 설치합니다...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 패키지 설치에 실패했습니다.
    pause
    exit /b 1
)

echo ✅ 패키지 설치 완료

REM Windows용 실행 파일 생성
echo 🪟 Windows용 실행 파일을 생성합니다...
python build_executable.py --windows
if errorlevel 1 (
    echo ❌ Windows용 실행 파일 생성에 실패했습니다.
    pause
    exit /b 1
)

echo ✅ Windows용 실행 파일 생성 완료!

REM Windows용 배포 패키지 생성
echo 📦 Windows용 배포 패키지를 생성합니다...
python create_package.py --windows
if errorlevel 1 (
    echo ❌ Windows용 배포 패키지 생성에 실패했습니다.
    pause
    exit /b 1
)

echo 🎉 Windows용 빌드가 완료되었습니다!
echo.
echo 📁 생성된 파일들:
echo   - dist\JavaSearchTool.exe (Windows 실행 파일)
echo   - deploy_windows\ (Windows용 배포 폴더)
echo   - JavaSearchTool_Windows_*.zip (배포 패키지)
echo.
echo 🚀 이제 Windows 사용자들과 공유할 수 있습니다!
echo.
pause
