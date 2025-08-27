# Java Search Tool 🔍

Eclipse의 검색 기능(Ctrl+H)과 유사한 GUI를 제공하는 Java 프로젝트 검색 도구입니다.

## ✨ 주요 기능

- **🔍 강력한 검색**: 정규표현식, 대소문자 구분, 단어 단위 검색 지원
- **📁 스마트 필터링**: 파일 확장자 및 제외 패턴 설정
- **📊 Excel 내보내기**: 검색 결과를 Excel 파일로 저장
- **⚡ 실시간 검색**: 진행률 표시와 함께 실시간 결과 업데이트
- **💾 설정 저장**: 검색 옵션과 최근 검색 기록 자동 저장
- **🌙 다크 테마**: 현대적인 다크 모드 UI

## 🚀 빠른 시작

### 1. 필요 조건

- Python 3.7 이상
- pip (Python 패키지 관리자)

### 2. 설치

```bash
# 저장소 클론
git clone https://github.com/devGWeloper/javaSearch.git
cd javaSearch

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 3. 실행

```bash
python main.py
```

## 📁 프로젝트 구조

```
javaSearch/
├── main.py                 # 메인 실행 파일
├── requirements.txt        # 필요한 패키지 목록
├── README.md              # 프로젝트 설명서
├── config.json            # 설정 파일 (자동 생성)
├── src/
│   ├── core/              # 핵심 로직
│   │   ├── search_engine.py    # 검색 엔진
│   │   └── config_manager.py   # 설정 관리
│   └── gui/               # GUI 모듈
│       └── main_window.py      # 메인 윈도우
└── assets/                # 리소스 파일
```

## 🔧 사용 방법

### 기본 검색

1. **검색 디렉토리 설정**: "찾아보기" 버튼을 클릭하여 Java 프로젝트 폴더를 선택
2. **키워드 입력**: 검색할 키워드나 정규표현식을 입력
3. **검색 시작**: "🔍 검색 시작" 버튼 클릭

### 고급 검색 옵션

#### 검색 옵션
- **정규표현식 사용**: 복잡한 패턴 검색 (예: `['"]DCOL['"]`)
- **대소문자 구분**: 정확한 대소문자 매칭
- **단어 단위 검색**: 완전한 단어만 검색

#### 파일 필터링
- **파일 확장자**: 검색할 파일 형식 지정 (예: `.java, .xml, .properties`)
- **제외 패턴**: 검색에서 제외할 폴더나 파일 패턴 (예: `*/target/*, */build/*`)

#### 고급 설정
- **파일 인코딩**: 파일 읽기 인코딩 (UTF-8, CP949, EUC-KR 등)
- **출력 파일**: Excel 내보내기 파일명 설정

### 결과 활용

- **더블클릭**: 파일을 기본 에디터로 열기
- **우클릭 메뉴**: 
  - 파일 열기
  - 폴더 열기  
  - 경로 복사
- **Excel 내보내기**: 검색 결과를 Excel 파일로 저장

## ⚙️ 설정

애플리케이션은 자동으로 설정을 `config.json` 파일에 저장합니다:

- 검색 옵션
- 최근 검색 키워드 (최대 10개)
- 최근 검색 디렉토리 (최대 10개)
- 윈도우 크기 및 위치
- 테마 설정

## 📝 정규표현식 예제

| 패턴 | 설명 | 예제 |
|------|------|------|
| `DCOL` | 단순 문자열 검색 | `DCOL` |
| `['"]DCOL['"]` | 따옴표로 둘러싸인 DCOL | `"DCOL"`, `'DCOL'` |
| `\bgetUser\b` | 단어 경계를 가진 getUser | `getUser()`, `getUser ` |
| `public\s+class` | public 다음에 공백과 class | `public class MyClass` |
| `@\w+` | 어노테이션 검색 | `@Override`, `@Service` |

## 🛠️ 기술 스택

- **Python 3.7+**: 메인 언어
- **CustomTkinter**: 모던 GUI 프레임워크  
- **Pandas**: 데이터 처리 및 Excel 내보내기
- **OpenPyXL**: Excel 파일 생성

## 🐛 문제 해결

### 자주 발생하는 문제

1. **모듈을 찾을 수 없음**
   ```bash
   pip install -r requirements.txt
   ```

2. **파일 인코딩 오류**
   - 파일 인코딩을 CP949나 EUC-KR로 변경해보세요

3. **검색이 너무 느림**
   - 제외 패턴에 `*/target/*`, `*/build/*` 등을 추가하세요
   - 검색 디렉토리를 더 구체적으로 지정하세요

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

---

**Eclipse 스타일의 강력한 검색 도구로 Java 개발 생산성을 높여보세요! 🚀**

