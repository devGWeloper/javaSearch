# 🪟 Windows용 실행 파일 빌드 가이드

Windows PC에서 Java Search Tool의 실행 파일(.exe)을 생성하는 방법입니다.

## 🚀 빠른 시작 (권장)

### 1. 자동 빌드 (가장 간단)
```cmd
# 배치 파일 실행
build_windows.bat
```
- 이 파일을 더블클릭하면 자동으로 모든 과정이 진행됩니다
- Python 설치부터 실행 파일 생성까지 자동 처리

### 2. 수동 빌드
```cmd
# 1. Python 설치 확인
python --version

# 2. 의존성 설치
pip install -r requirements.txt

# 3. Windows용 실행 파일 생성
python build_executable.py --windows

# 4. 배포 패키지 생성
python create_package.py --windows
```

## 📋 필요 조건

- **Windows 10/11**
- **Python 3.8+** ([다운로드](https://www.python.org/downloads/))
- **pip** (Python과 함께 설치됨)
- **Git** (저장소 클론용, 선택사항)

## 🔧 상세 단계

### 1단계: Python 설치
1. [Python 공식 사이트](https://www.python.org/downloads/)에서 최신 버전 다운로드
2. 설치 시 **"Add Python to PATH"** 체크박스 선택
3. 설치 완료 후 명령 프롬프트에서 `python --version` 확인

### 2단계: 프로젝트 다운로드
```cmd
# Git 사용
git clone <repository-url>
cd javaSearch

# 또는 ZIP 다운로드 후 압축 해제
```

### 3단계: 의존성 설치
```cmd
pip install -r requirements.txt
```

### 4단계: 실행 파일 생성
```cmd
python build_executable.py --windows
```

### 5단계: 배포 패키지 생성
```cmd
python create_package.py --windows
```

## 📁 생성된 파일들

빌드가 완료되면 다음 파일들이 생성됩니다:

- **`dist/JavaSearchTool.exe`** - Windows 실행 파일 (약 30-40MB)
- **`deploy_windows/`** - Windows용 배포 폴더
- **`JavaSearchTool_Windows_YYYYMMDD_HHMMSS.zip`** - 배포 패키지

## 🚨 문제 해결

### Python이 인식되지 않는 경우
1. Python 재설치 시 "Add Python to PATH" 선택
2. 시스템 환경 변수에서 Python 경로 확인
3. 명령 프롬프트 재시작

### 패키지 설치 실패
```cmd
# pip 업그레이드
python -m pip install --upgrade pip

# 개별 패키지 설치
pip install customtkinter pandas openpyxl Pillow pyinstaller
```

### PyInstaller 오류
```cmd
# PyInstaller 재설치
pip uninstall pyinstaller
pip install pyinstaller

# 또는 특정 버전 설치
pip install pyinstaller==6.15.0
```

### 바이러스 백신 경고
- Windows Defender나 다른 백신에서 실행 파일을 차단할 수 있습니다
- 임시로 백신을 비활성화하거나 예외 목록에 추가

## 🎯 사용법

### 실행 파일 테스트
```cmd
# dist 폴더에서 실행
cd dist
JavaSearchTool.exe
```

### 배포
- `JavaSearchTool_Windows_*.zip` 파일을 다른 Windows 사용자에게 공유
- 수신자는 압축 해제 후 `JavaSearchTool.exe` 더블클릭으로 실행

## 💡 팁

1. **관리자 권한**: 일부 경우 관리자 권한으로 명령 프롬프트 실행
2. **안티바이러스**: 빌드 중 일시적으로 비활성화
3. **디스크 공간**: 최소 2GB 여유 공간 확보
4. **인터넷**: 의존성 다운로드를 위해 안정적인 연결 필요

## 🔗 관련 링크

- [Python 공식 사이트](https://www.python.org/downloads/)
- [PyInstaller 문서](https://pyinstaller.org/en/stable/)
- [CustomTkinter 문서](https://github.com/TomSchimansky/CustomTkinter)

---

**Windows에서 실행 파일을 생성한 후, 다른 Windows 사용자들과 쉽게 공유할 수 있습니다!** 🚀
