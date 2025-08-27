#!/usr/bin/env python3
"""
Java Search Tool - Eclipse Style
메인 실행 파일

Eclipse의 검색 기능과 유사한 GUI를 제공하는 Java 프로젝트 검색 도구입니다.
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.gui.main_window import JavaSearchApp
except ImportError as e:
    print(f"필요한 모듈을 가져올 수 없습니다: {e}")
    print("다음 명령어로 필요한 패키지를 설치해주세요:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """메인 함수"""
    try:
        # GUI 애플리케이션 시작
        app = JavaSearchApp()
        app.run()
    except KeyboardInterrupt:
        print("\n프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"애플리케이션 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

