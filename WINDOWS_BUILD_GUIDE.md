# Windows EXE 성능 최적화 가이드

## 🚀 시작 속도 개선 방법

### 1. 빌드 최적화
- `--onedir` 옵션 사용 (--onefile 대신)
- 불필요한 모듈 제외
- Python 최적화 레벨 2 적용
- 디버그 심볼 제거

### 2. 실행 파일 최적화
```cmd
# 최적화된 빌드
python build_executable.py --windows

# 또는 배치 파일 사용
build_windows.bat
```

### 3. 시스템 최적화
- SSD에 설치
- Windows Defender 예외 추가
- 불필요한 백그라운드 프로그램 종료
- 가상 메모리 최적화

## 📊 성능 비교

| 옵션 | 시작 시간 | 파일 크기 | 메모리 사용량 |
|------|-----------|-----------|---------------|
| --onefile | 15-30초 | 200-300MB | 높음 |
| --onedir (최적화) | 3-8초 | 150-200MB | 낮음 |

## 🔧 추가 최적화 팁

### 1. 가상환경 사용
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 의존성 최소화
- 필요한 패키지만 설치
- 개발용 패키지 제외
- 버전 고정

### 3. Windows 특화 설정
- Windows 경로 구분자 사용 (;)
- Windows 호환성 모드 설정
- 관리자 권한으로 실행

## 🐛 문제 해결

### 느린 시작
1. `--onedir` 옵션 확인
2. 불필요한 모듈 제외 확인
3. 시스템 리소스 확인

### 실행 오류
1. Visual C++ Redistributable 설치
2. .NET Framework 확인
3. Windows Defender 예외 추가

### 메모리 부족
1. 가상 메모리 증가
2. 백그라운드 프로그램 종료
3. 시스템 재부팅

## 📈 성능 모니터링

```python
import time
import psutil

start_time = time.time()
# 애플리케이션 시작
end_time = time.time()

print(f"시작 시간: {end_time - start_time:.2f}초")
print(f"메모리 사용량: {psutil.Process().memory_info().rss / 1024 / 1024:.1f}MB")
```

## 🎯 최적화 체크리스트

- [ ] `--onedir` 옵션 사용
- [ ] 불필요한 모듈 제외
- [ ] Python 최적화 레벨 2
- [ ] 디버그 심볼 제거
- [ ] Windows 경로 구분자 사용
- [ ] 가상환경 사용
- [ ] 의존성 최소화
- [ ] 시스템 최적화
