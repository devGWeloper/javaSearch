# Java Search Tool - Eclipse Style

Eclipse의 검색 기능과 유사한 GUI를 제공하는 Java 프로젝트 검색 도구입니다.

## 🚀 주요 기능

- **강력한 검색**: 정규표현식, 대소문자 구분, 단어 단위 검색 지원
- **다양한 파일 형식**: Java, XML, Properties 등 다양한 파일 형식 검색
- **빠른 성능**: 멀티스레딩을 통한 최적화된 검색 성능
- **사용자 친화적**: 직관적인 GUI 인터페이스
- **Excel 내보내기**: 검색 결과를 Excel 파일로 저장
- **파일명 중복 방지**: 자동으로 번호를 붙인 파일명 생성

## 📋 시스템 요구사항

- **Python 3.8+** (개발용)
- **macOS 10.13+** 또는 **Windows 10+** (실행 파일)
- **최소 4GB RAM**
- **100MB 이상의 디스크 공간**

## 🎯 사용 방법

### 1. Python으로 실행 (개발자용)

```bash
# 의존성 설치
pip install -r requirements.txt

# 프로그램 실행
python main.py
```

### 2. 실행 파일로 실행 (일반 사용자용)

**macOS:**
- `JavaSearchTool` 파일을 더블클릭
- 또는 터미널에서 `./JavaSearchTool` 실행

**Windows:**
- `JavaSearchTool.exe` 파일을 더블클릭

## 🔧 실행 파일 생성

다른 사람과 공유할 수 있는 독립 실행 파일을 생성할 수 있습니다.

### 1. macOS용 실행 파일 빌드

```bash
# 실행 파일 생성
python build_executable.py

# 빌드 파일 정리
python build_executable.py --clean
```

### 2. Windows용 실행 파일 빌드

**Windows PC에서 실행:**

```cmd
# 자동 빌드 (권장)
build_windows.bat

# 또는 수동 빌드
python build_executable.py --windows
python create_package.py --windows
```

**자세한 가이드:** `WINDOWS_BUILD_GUIDE.md` 파일 참조

### 3. 배포 패키지 생성

```bash
# 현재 플랫폼용 패키지 생성
python create_package.py

# Windows용 패키지 생성 (Windows에서)
python create_package.py --windows

# 크로스 플랫폼 패키지 생성
python create_package.py --cross-platform

# 패키지 목록 표시
python create_package.py --list

# 패키지 파일 정리
python create_package.py --clean
```

## 📁 프로젝트 구조

```
javaSearch/
├── main.py                 # 메인 실행 파일
├── build_executable.py     # 실행 파일 빌드 스크립트
├── create_package.py       # 배포 패키지 생성 스크립트
├── requirements.txt        # Python 의존성
├── src/
│   ├── core/              # 핵심 검색 엔진
│   │   ├── search_engine.py
│   │   └── config_manager.py
│   └── gui/               # GUI 인터페이스
│       └── main_window.py
├── assets/                 # 아이콘 및 리소스
├── dist/                   # 생성된 실행 파일
├── deploy/                 # 배포용 파일
└── build/                  # 빌드 임시 파일
```

## 🎨 GUI 기능

- **검색 설정**: 디렉토리, 키워드, 옵션 설정
- **검색 옵션**: 정규표현식, 대소문자 구분, 단어 단위 검색
- **파일 필터링**: 확장자별 검색, 제외 패턴 설정
- **실시간 진행률**: 검색 진행 상황 표시
- **결과 표시**: 파일명, 라인 번호, 내용, 매칭 텍스트
- **Excel 내보내기**: 검색 결과를 Excel 파일로 저장
- **파일 열기**: 검색 결과 파일을 기본 프로그램으로 열기

## 📊 Excel 내보내기

- **컬럼**: File Path, File Name, Line, Content, Match
- **파일명 중복 방지**: 자동으로 번호를 붙인 파일명 생성
- **예시**: `search_results.xlsx` → `search_results_1.xlsx`

## 🔍 검색 옵션

- **정규표현식**: 복잡한 패턴 검색 지원
- **대소문자 구분**: 대소문자 구분 여부 선택
- **단어 단위**: 단어 경계를 고려한 검색
- **파일 확장자**: `.java`, `.xml`, `.properties` 등
- **제외 패턴**: `*/target/*`, `*/build/*`, `*/.git/*`