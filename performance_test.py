#!/usr/bin/env python3
"""
Java Search Tool 성능 테스트 스크립트
Windows EXE 시작 속도와 메모리 사용량을 측정합니다.
"""

import time
import psutil
import os
import sys
from pathlib import Path

def test_startup_performance():
    """애플리케이션 시작 성능을 테스트합니다."""
    print("🚀 Java Search Tool 성능 테스트")
    print("=" * 50)
    
    # 시작 시간 측정
    start_time = time.time()
    
    try:
        # 모듈 로딩 시간 측정
        print("📦 모듈 로딩 중...")
        module_start = time.time()
        
        from src.gui.main_window import JavaSearchApp
        
        module_load_time = time.time() - module_start
        print(f"✅ 모듈 로딩 완료: {module_load_time:.2f}초")
        
        # GUI 초기화 시간 측정
        print("🖥️ GUI 초기화 중...")
        gui_start = time.time()
        
        app = JavaSearchApp()
        
        gui_init_time = time.time() - gui_start
        print(f"✅ GUI 초기화 완료: {gui_init_time:.2f}초")
        
        # 전체 시작 시간
        total_time = time.time() - start_time
        
        # 메모리 사용량 측정
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        print("\n📊 성능 결과:")
        print(f"   모듈 로딩: {module_load_time:.2f}초")
        print(f"   GUI 초기화: {gui_init_time:.2f}초")
        print(f"   전체 시작: {total_time:.2f}초")
        print(f"   메모리 사용: {memory_mb:.1f}MB")
        
        # 성능 등급 평가
        if total_time < 3:
            grade = "🟢 우수"
        elif total_time < 8:
            grade = "🟡 양호"
        elif total_time < 15:
            grade = "🟠 보통"
        else:
            grade = "🔴 개선 필요"
        
        print(f"   성능 등급: {grade}")
        
        # 최적화 권장사항
        print("\n💡 최적화 권장사항:")
        if total_time > 8:
            print("   - --onedir 옵션 사용 확인")
            print("   - 불필요한 모듈 제외 확인")
            print("   - Python 최적화 레벨 2 적용")
        
        if memory_mb > 200:
            print("   - 메모리 사용량이 높습니다")
            print("   - 가상환경 사용 권장")
            print("   - 불필요한 의존성 제거")
        
        return True
        
    except ImportError as e:
        print(f"❌ 모듈 로딩 실패: {e}")
        return False
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False

def test_file_operations():
    """파일 작업 성능을 테스트합니다."""
    print("\n📁 파일 작업 성능 테스트")
    print("-" * 30)
    
    try:
        # 설정 파일 읽기 테스트
        config_start = time.time()
        from src.core.config_manager import ConfigManager
        config = ConfigManager()
        config_load_time = time.time() - config_start
        
        print(f"설정 로딩: {config_load_time:.3f}초")
        
        # 검색 엔진 초기화 테스트
        engine_start = time.time()
        from src.core.search_engine import SearchEngine
        engine = SearchEngine()
        engine_init_time = time.time() - engine_start
        
        print(f"검색 엔진 초기화: {engine_init_time:.3f}초")
        
        return True
        
    except Exception as e:
        print(f"❌ 파일 작업 테스트 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🔍 성능 테스트를 시작합니다...")
    
    # 시스템 정보 출력
    print(f"💻 시스템: {sys.platform}")
    print(f"🐍 Python: {sys.version}")
    print(f"💾 메모리: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f}GB")
    
    # 성능 테스트 실행
    if test_startup_performance():
        test_file_operations()
    
    print("\n✅ 성능 테스트 완료!")

if __name__ == "__main__":
    main()
