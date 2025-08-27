import tkinter as tk


class UISettingsManager:
    """UI 관련 설정 관리 클래스"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def load_settings_to_ui(self, search_panel, root):
        """설정을 UI에 로드"""
        # 검색 설정 로드
        config = {
            'search_directory': self.config_manager.get("search_directory", ""),
            'keyword': self.config_manager.get("keyword", ""),
            'use_regex': self.config_manager.get("use_regex", True),
            'case_sensitive': self.config_manager.get("case_sensitive", False),
            'whole_word': self.config_manager.get("whole_word", False),
            'file_extensions': self.config_manager.get("file_extensions", [".java", ".xml", ".properties"]),
            'exclude_patterns': self.config_manager.get("exclude_patterns", []),
            'file_encoding': self.config_manager.get("file_encoding", "utf-8"),
            'output_file': self.config_manager.get("output_file", "search_results.xlsx")
        }
        
        search_panel.set_search_config(config)
        
        # 윈도우 크기 복원
        geometry = self.config_manager.get("window_geometry", "1200x800+100+100")
        root.geometry(geometry)
    
    def save_settings_from_ui(self, search_panel, root):
        """UI에서 설정을 저장"""
        config = search_panel.get_search_config()
        
        self.config_manager.set("search_directory", config['search_dir'])
        self.config_manager.set("keyword", config['keyword'])
        self.config_manager.set("use_regex", config['use_regex'])
        self.config_manager.set("case_sensitive", config['case_sensitive'])
        self.config_manager.set("whole_word", config['whole_word'])
        self.config_manager.set("file_extensions", config['extensions'])
        self.config_manager.set("exclude_patterns", config['exclude_patterns'])
        self.config_manager.set("file_encoding", config['encoding'])
        self.config_manager.set("output_file", config['output_file'])
        self.config_manager.set("window_geometry", root.geometry())
        
        self.config_manager.save_config()
    
    def update_recent_combos(self, search_panel):
        """최근 검색 콤보박스 업데이트"""
        recent_searches = self.config_manager.get_recent_searches()
        recent_directories = self.config_manager.get_recent_directories()
        
        search_panel.update_recent_combos(recent_searches, recent_directories)
