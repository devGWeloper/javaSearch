import json
import os
from pathlib import Path
from typing import Dict, Any, List


class ConfigManager:
    """설정 관리 클래스 (최적화된 버전)"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self._config = None  # 지연 로딩을 위한 캐시
        self._config_loaded = False
        self.default_config = {
            "search_directory": "",
            "keyword": "",
            "use_regex": True,
            "case_sensitive": False,
            "whole_word": False,
            "file_extensions": [".java", ".xml", ".properties"],
            "exclude_patterns": ["*/target/*", "*/build/*", "*/.git/*", "*/node_modules/*"],
            "file_encoding": "utf-8",
            "output_file": "search_results.xlsx",
            "recent_searches": [],
            "recent_directories": [],
            "window_geometry": "800x600+100+100",
            "theme": "dark"
        }
    
    @property
    def config(self) -> Dict[str, Any]:
        """설정을 지연 로딩으로 가져옵니다."""
        if not self._config_loaded:
            self._config = self.load_config()
            self._config_loaded = True
        return self._config
    
    def load_config(self) -> Dict[str, Any]:
        """설정 파일을 로드합니다."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # 기본 설정과 병합
                config = self.default_config.copy()
                config.update(loaded_config)
                return config
                
            except (json.JSONDecodeError, IOError) as e:
                print(f"설정 파일 로드 오류: {e}")
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self) -> bool:
        """설정을 파일에 저장합니다."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"설정 파일 저장 오류: {e}")
            return False
    
    def get(self, key: str, default=None):
        """설정 값을 가져옵니다."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """설정 값을 설정합니다."""
        self.config[key] = value
    
    def add_recent_search(self, keyword: str, max_items: int = 10):
        """최근 검색어를 추가합니다."""
        recent_searches = self.config.get("recent_searches", [])
        
        # 중복 제거
        if keyword in recent_searches:
            recent_searches.remove(keyword)
        
        # 맨 앞에 추가
        recent_searches.insert(0, keyword)
        
        # 최대 개수 제한
        recent_searches = recent_searches[:max_items]
        
        self.config["recent_searches"] = recent_searches
    
    def add_recent_directory(self, directory: str, max_items: int = 10):
        """최근 검색 디렉토리를 추가합니다."""
        recent_directories = self.config.get("recent_directories", [])
        
        # 중복 제거
        if directory in recent_directories:
            recent_directories.remove(directory)
        
        # 맨 앞에 추가
        recent_directories.insert(0, directory)
        
        # 최대 개수 제한
        recent_directories = recent_directories[:max_items]
        
        self.config["recent_directories"] = recent_directories
    
    def get_recent_searches(self) -> List[str]:
        """최근 검색어 목록을 반환합니다."""
        return self.config.get("recent_searches", [])
    
    def get_recent_directories(self) -> List[str]:
        """최근 검색 디렉토리 목록을 반환합니다."""
        return self.config.get("recent_directories", [])
    
    def reset_to_default(self):
        """설정을 기본값으로 초기화합니다."""
        self.config = self.default_config.copy()
    
    def export_config(self, export_file: str) -> bool:
        """설정을 다른 파일로 내보냅니다."""
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"설정 내보내기 오류: {e}")
            return False
    
    def import_config(self, import_file: str) -> bool:
        """다른 파일에서 설정을 가져옵니다."""
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # 기본 설정과 병합
            config = self.default_config.copy()
            config.update(imported_config)
            self.config = config
            return True
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"설정 가져오기 오류: {e}")
            return False

