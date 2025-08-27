import customtkinter as ctk
import tkinter as tk
import os
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.search_engine import SearchEngine, SearchResult
from src.core.config_manager import ConfigManager
from src.gui.search_panel import SearchPanel
from src.gui.results_panel import ResultsPanel
from src.gui.event_handlers import SearchEventHandler, ExportEventHandler, FileEventHandler
from src.gui.settings_manager import UISettingsManager


class JavaSearchApp:
    """Java 검색 도구 메인 애플리케이션"""
    
    def __init__(self):
        # CustomTkinter 설정
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 메인 윈도우 생성
        self.root = ctk.CTk()
        self.root.title("Java Search Tool - Eclipse Style")
        self.root.geometry("1200x800")
        
        # 아이콘 설정 (선택사항)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # 컴포넌트 초기화
        self.search_engine = SearchEngine()
        self.config_manager = ConfigManager()
        self.ui_settings_manager = UISettingsManager(self.config_manager)
        
        # UI 구성
        self.setup_ui()
        
        # 이벤트 핸들러 초기화
        self.setup_event_handlers()
        
        # 설정 로드
        self.load_settings()
        
        # 윈도우 닫기 이벤트
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """UI 구성"""
        # 메인 컨테이너
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 검색 패널
        self.search_panel = SearchPanel(self.main_container, self.config_manager)
        
        # 결과 패널
        self.results_panel = ResultsPanel(self.main_container)
    
    def setup_event_handlers(self):
        """이벤트 핸들러 설정"""
        # 검색 이벤트 핸들러
        self.search_handler = SearchEventHandler(self, self.search_panel, self.results_panel)
        
        # 내보내기 이벤트 핸들러
        self.export_handler = ExportEventHandler(self, self.search_panel, self.results_panel)
        
        # 파일 이벤트 핸들러
        self.file_handler = FileEventHandler(self, self.results_panel)
    
    def load_settings(self):
        """설정 로드"""
        self.ui_settings_manager.load_settings_to_ui(self.search_panel, self.root)
        self.update_recent_combos()
    
    def update_recent_combos(self):
        """최근 검색 콤보박스 업데이트"""
        self.ui_settings_manager.update_recent_combos(self.search_panel)
    
    def save_settings(self):
        """설정 저장"""
        self.ui_settings_manager.save_settings_from_ui(self.search_panel, self.root)
    
    def on_closing(self):
        """윈도우 닫기"""
        if hasattr(self.search_handler, 'is_searching') and self.search_handler.is_searching:
            self.search_handler.cancel_search()
        
        self.save_settings()
        self.root.destroy()
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()


if __name__ == "__main__":
    app = JavaSearchApp()
    app.run()
