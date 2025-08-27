import os
import re
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class SearchResult:
    """검색 결과를 담는 데이터 클래스"""
    def __init__(self, file_path: str, file_name: str, line_number: int, content: str, match_text: str):
        self.file_path = file_path
        self.file_name = file_name
        self.line_number = line_number
        self.content = content
        self.match_text = match_text


class SearchEngine:
    """Java 프로젝트 검색 엔진 (최적화된 버전)"""
    
    def __init__(self, max_workers: int = None):
        self.is_searching = False
        self.search_thread = None
        self.cancel_search = False
        # CPU 코어 수에 따른 최적 워커 수 설정
        self.max_workers = max_workers or min(8, (os.cpu_count() or 1) + 4)
        # 정규식 패턴 캐시
        self.pattern_cache = {}
        self.cache_size_limit = 100
        
    def _get_cached_pattern(self, keyword: str, flags: int) -> re.Pattern:
        """정규식 패턴을 캐시에서 가져오거나 컴파일"""
        cache_key = f"{keyword}_{flags}"
        
        if cache_key in self.pattern_cache:
            return self.pattern_cache[cache_key]
        
        try:
            pattern = re.compile(keyword, flags)
            # 캐시 크기 제한
            if len(self.pattern_cache) >= self.cache_size_limit:
                # 가장 오래된 항목 제거
                oldest_key = next(iter(self.pattern_cache))
                del self.pattern_cache[oldest_key]
            
            self.pattern_cache[cache_key] = pattern
            return pattern
        except re.error as e:
            raise ValueError(f"정규식 에러: {e}")
    
    def _should_skip_file(self, file_path: Path, exclude_patterns: List[re.Pattern]) -> bool:
        """파일이 제외 패턴에 해당하는지 빠르게 확인"""
        file_str = str(file_path)
        file_name = file_path.name
        
        for pattern in exclude_patterns:
            if pattern.search(file_str) or pattern.search(file_name):
                return True
        return False
    
    def _search_single_file(self, file_path: Path, pattern: re.Pattern, 
                           file_encoding: str) -> List[SearchResult]:
        """단일 파일에서 검색 수행 (최적화된 버전)"""
        results = []
        
        try:
            # 파일을 한 번에 읽기 (메모리 효율적)
            with open(file_path, "r", encoding=file_encoding, errors="ignore") as f:
                # 모든 파일을 한 번에 읽기
                content = f.read()
                lines = content.splitlines()
                
                # 라인별 검색 (최적화된 버전)
                for line_num, line in enumerate(lines, start=1):
                    if self.cancel_search:
                        break
                    
                    # 정규식 매칭
                    matches = pattern.finditer(line)
                    for match in matches:
                        result = SearchResult(
                            file_path=str(file_path),
                            file_name=file_path.name,
                            line_number=line_num,
                            content=line.strip(),
                            match_text=match.group()
                        )
                        results.append(result)
                        
        except Exception as e:
            # 파일 읽기 오류는 무시하고 계속 진행
            print(f"파일 읽기 오류: {file_path} ({e})")
        
        return results
    
    def _collect_target_files_optimized(self, search_path: Path, file_extensions: tuple,
                                      exclude_patterns: List[re.Pattern]) -> List[Path]:
        """대상 파일 목록을 효율적으로 수집"""
        target_files = []
        
        # 파일 확장자 세트로 변환 (검색 속도 향상)
        ext_set = set(file_extensions)
        
        for root, dirs, files in os.walk(search_path):
            if self.cancel_search:
                break
            
            # 디렉토리 제외 패턴 체크 (최적화)
            dirs[:] = [d for d in dirs if not self._should_skip_file(Path(root) / d, exclude_patterns)]
            
            # 파일 필터링 및 수집
            for file in files:
                if not file.endswith(file_extensions):
                    continue
                
                file_path = Path(root) / file
                
                # 제외 패턴 체크
                if not self._should_skip_file(file_path, exclude_patterns):
                    target_files.append(file_path)
        
        return target_files
    
    def search(self, 
               search_dir: str,
               keyword: str,
               use_regex: bool = True,
               case_sensitive: bool = False,
               whole_word: bool = False,
               file_extensions: tuple = (".java", ".xml", ".properties"),
               exclude_patterns: List[str] = None,
               file_encoding: str = "utf-8",
               progress_callback: Callable[[int, int, str], None] = None,
               result_callback: Callable[[List[SearchResult]], None] = None) -> List[SearchResult]:
        """
        파일 검색을 수행합니다. (최적화된 버전)
        
        Args:
            search_dir: 검색할 디렉토리 경로
            keyword: 검색할 키워드
            use_regex: 정규식 사용 여부
            case_sensitive: 대소문자 구분 여부
            whole_word: 단어 단위 검색 여부
            file_extensions: 검색할 파일 확장자 튜플
            exclude_patterns: 제외할 파일/폴더 패턴 리스트
            file_encoding: 파일 인코딩
            progress_callback: 진행률 콜백 함수 (current, total, current_file)
            result_callback: 결과 콜백 함수 (results)
            
        Returns:
            검색 결과 리스트
        """
        start_time = time.time()
        search_path = Path(search_dir)
        
        # 경로 검증
        if not search_path.exists() or not search_path.is_dir():
            raise ValueError(f"경로 {search_dir} 가 존재하지 않습니다.")
        
        if not keyword.strip():
            raise ValueError("검색할 키워드를 입력해주세요.")
        
        results = []
        self.cancel_search = False
        
        # 대소문자 옵션
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # 패턴 준비 (캐시 사용)
        if use_regex:
            pattern = self._get_cached_pattern(keyword, flags)
        else:
            if whole_word:
                pattern = self._get_cached_pattern(rf"\b{re.escape(keyword)}\b", flags)
            else:
                pattern = self._get_cached_pattern(re.escape(keyword), flags)
        
        # 제외 패턴 컴파일 (최적화)
        exclude_compiled = []
        if exclude_patterns:
            for exclude_pattern in exclude_patterns:
                if exclude_pattern.strip():
                    try:
                        exclude_compiled.append(re.compile(exclude_pattern, re.IGNORECASE))
                    except re.error:
                        # 정규식이 아닌 경우 일반 문자열로 처리
                        exclude_compiled.append(re.compile(re.escape(exclude_pattern), re.IGNORECASE))
        
        # 대상 파일 목록 수집 (최적화)
        target_files = self._collect_target_files_optimized(search_path, file_extensions, exclude_compiled)
        total_files = len(target_files)
        
        if total_files == 0:
            return results
        
        # 병렬 처리를 위한 청크 분할
        chunk_size = max(1, total_files // self.max_workers)
        file_chunks = [target_files[i:i + chunk_size] for i in range(0, total_files, chunk_size)]
        
        # 병렬 검색 실행
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 각 청크를 병렬로 처리
            future_to_chunk = {
                executor.submit(self._process_file_chunk, chunk, pattern, file_encoding, 
                              progress_callback, total_files): chunk 
                for chunk in file_chunks
            }
            
            for future in as_completed(future_to_chunk):
                if self.cancel_search:
                    break
                
                try:
                    chunk_results = future.result()
                    results.extend(chunk_results)
                    
                    # 실시간 결과 업데이트
                    if result_callback and chunk_results:
                        result_callback(chunk_results)
                        
                except Exception as e:
                    print(f"청크 처리 오류: {e}")
                    continue
        
        # 성능 통계
        elapsed_time = time.time() - start_time
        print(f"검색 완료: {len(results)}건, {total_files}개 파일, {elapsed_time:.2f}초")
        
        return results
    
    def _process_file_chunk(self, file_chunk: List[Path], pattern: re.Pattern, 
                           file_encoding: str, progress_callback, total_files: int) -> List[SearchResult]:
        """파일 청크를 처리하는 워커 함수"""
        chunk_results = []
        
        for file_path in file_chunk:
            if self.cancel_search:
                break
            
            if progress_callback:
                progress_callback(len(chunk_results), total_files, str(file_path))
            
            # 단일 파일 검색
            file_results = self._search_single_file(file_path, pattern, file_encoding)
            chunk_results.extend(file_results)
        
        return chunk_results
    
    def search_async(self, *args, **kwargs):
        """비동기 검색 실행 (최적화된 버전)"""
        if self.is_searching:
            return False
        
        self.is_searching = True
        self.search_thread = threading.Thread(
            target=self._search_thread_worker,
            args=args,
            kwargs=kwargs
        )
        self.search_thread.daemon = True
        self.search_thread.start()
        return True
    
    def _search_thread_worker(self, *args, **kwargs):
        """검색 스레드 워커 (최적화된 버전)"""
        try:
            self.search(*args, **kwargs)
        except Exception as e:
            print(f"검색 오류: {e}")
        finally:
            self.is_searching = False
    
    def cancel_current_search(self):
        """현재 검색 취소 (최적화된 버전)"""
        self.cancel_search = True
        if self.search_thread and self.search_thread.is_alive():
            self.search_thread.join(timeout=1.0)
        self.is_searching = False
    
    def export_to_excel(self, results: List[SearchResult], output_file: str) -> bool:
        """검색 결과를 Excel 파일로 내보내기 (최적화된 버전)"""
        try:
            if not results:
                return False
            
            # 데이터 변환을 최적화
            data = [
                [result.file_path, result.file_name, result.line_number, 
                 result.content, result.match_text]
                for result in results
            ]
            
            df = pd.DataFrame(data, columns=["File Path", "File Name", "Line", "Content", "Match"])
            df.to_excel(output_file, index=False, engine='openpyxl')
            return True
            
        except Exception as e:
            print(f"Excel 내보내기 오류: {e}")
            return False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """성능 통계 정보 반환"""
        return {
            "max_workers": self.max_workers,
            "pattern_cache_size": len(self.pattern_cache),
            "cache_size_limit": self.cache_size_limit
        }
    
    def clear_pattern_cache(self):
        """정규식 패턴 캐시 정리"""
        self.pattern_cache.clear()
    
    def set_max_workers(self, max_workers: int):
        """최대 워커 수 설정"""
        self.max_workers = max(1, max_workers)

