import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


class SearchPanel:
    """검색 설정 패널 UI 컴포넌트"""
    
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        self.setup_ui()
    
    def setup_ui(self):
        """검색 패널 UI 구성"""
        # 검색 패널 프레임
        self.search_frame = ctk.CTkFrame(self.parent)
        self.search_frame.pack(fill="x", padx=5, pady=5)
        
        # 제목
        title_label = ctk.CTkLabel(self.search_frame, text="🔍 Java Project Search", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        # 메인 검색 설정
        self.setup_main_search_frame()
        
        # 검색 버튼
        self.setup_button_frame()
    
    def setup_main_search_frame(self):
        """메인 검색 설정 프레임"""
        main_search_frame = ctk.CTkFrame(self.search_frame)
        main_search_frame.pack(fill="x", padx=10, pady=5)
        
        # 검색 디렉토리
        self.setup_directory_frame(main_search_frame)
        
        # 검색 키워드
        self.setup_keyword_frame(main_search_frame)
        
        # 검색 옵션
        self.setup_options_frame(main_search_frame)
        
        # 파일 확장자
        self.setup_extensions_frame(main_search_frame)
        
        # 제외 패턴
        self.setup_exclude_frame(main_search_frame)
        
        # 고급 옵션
        self.setup_advanced_frame(main_search_frame)
    
    def setup_directory_frame(self, parent):
        """디렉토리 선택 프레임"""
        dir_frame = ctk.CTkFrame(parent)
        dir_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(dir_frame, text="검색 디렉토리:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        dir_input_frame = ctk.CTkFrame(dir_frame)
        dir_input_frame.pack(fill="x", padx=10, pady=(5,10))
        
        self.dir_entry = ctk.CTkEntry(dir_input_frame, placeholder_text="검색할 프로젝트 경로를 선택하세요...")
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(5,5))
        
        self.browse_btn = ctk.CTkButton(dir_input_frame, text="찾아보기", width=100)
        self.browse_btn.pack(side="right", padx=(5,5))
        
        # 최근 디렉토리 콤보박스
        self.recent_dir_combo = ctk.CTkComboBox(dir_input_frame, width=120,
                                               values=["최근 디렉토리"])
        self.recent_dir_combo.set("최근 디렉토리")
        self.recent_dir_combo.pack(side="right", padx=(5,5))
    
    def setup_keyword_frame(self, parent):
        """키워드 입력 프레임"""
        keyword_frame = ctk.CTkFrame(parent)
        keyword_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(keyword_frame, text="검색 키워드:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        keyword_input_frame = ctk.CTkFrame(keyword_frame)
        keyword_input_frame.pack(fill="x", padx=10, pady=(5,10))
        
        self.keyword_entry = ctk.CTkEntry(keyword_input_frame, placeholder_text="검색할 키워드를 입력하세요...")
        self.keyword_entry.pack(side="left", fill="x", expand=True, padx=(5,5))
        
        # 최근 검색어 콤보박스
        self.recent_search_combo = ctk.CTkComboBox(keyword_input_frame, width=120,
                                                  values=["최근 검색"])
        self.recent_search_combo.set("최근 검색")
        self.recent_search_combo.pack(side="right", padx=(5,5))
    
    def setup_options_frame(self, parent):
        """검색 옵션 프레임"""
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(options_frame, text="검색 옵션:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        # 옵션 체크박스들
        checkbox_frame = ctk.CTkFrame(options_frame)
        checkbox_frame.pack(fill="x", padx=10, pady=(0,10))
        
        # 첫 번째 줄
        first_row = ctk.CTkFrame(checkbox_frame)
        first_row.pack(fill="x", pady=2)
        
        self.regex_var = ctk.BooleanVar(value=True)
        self.regex_check = ctk.CTkCheckBox(first_row, text="정규표현식 사용", variable=self.regex_var)
        self.regex_check.pack(side="left", padx=10)
        
        self.case_var = ctk.BooleanVar(value=False)
        self.case_check = ctk.CTkCheckBox(first_row, text="대소문자 구분", variable=self.case_var)
        self.case_check.pack(side="left", padx=10)
        
        self.word_var = ctk.BooleanVar(value=False)
        self.word_check = ctk.CTkCheckBox(first_row, text="단어 단위 검색", variable=self.word_var)
        self.word_check.pack(side="left", padx=10)
    
    def setup_extensions_frame(self, parent):
        """파일 확장자 프레임"""
        ext_frame = ctk.CTkFrame(parent)
        ext_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(ext_frame, text="파일 확장자:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        self.extensions_entry = ctk.CTkEntry(ext_frame, placeholder_text=".java, .xml, .properties")
        self.extensions_entry.pack(fill="x", padx=10, pady=(5,10))
    
    def setup_exclude_frame(self, parent):
        """제외 패턴 프레임"""
        exclude_frame = ctk.CTkFrame(parent)
        exclude_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(exclude_frame, text="제외 패턴:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        self.exclude_entry = ctk.CTkEntry(exclude_frame, placeholder_text="*/target/*, */build/*, */.git/*")
        self.exclude_entry.pack(fill="x", padx=10, pady=(5,10))
    
    def setup_advanced_frame(self, parent):
        """고급 설정 프레임"""
        advanced_frame = ctk.CTkFrame(parent)
        advanced_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(advanced_frame, text="고급 설정:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        advanced_input_frame = ctk.CTkFrame(advanced_frame)
        advanced_input_frame.pack(fill="x", padx=10, pady=(5,10))
        
        ctk.CTkLabel(advanced_input_frame, text="파일 인코딩:").pack(side="left", padx=(5,5))
        self.encoding_combo = ctk.CTkComboBox(advanced_input_frame, 
                                             values=["utf-8", "cp949", "euc-kr", "ascii"],
                                             width=100)
        self.encoding_combo.pack(side="left", padx=(5,10))
        
        ctk.CTkLabel(advanced_input_frame, text="출력 파일:").pack(side="left", padx=(10,5))
        self.output_entry = ctk.CTkEntry(advanced_input_frame, width=200)
        self.output_entry.pack(side="left", padx=(5,10))
    
    def setup_button_frame(self):
        """버튼 프레임"""
        button_frame = ctk.CTkFrame(self.search_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.search_btn = ctk.CTkButton(button_frame, text="🔍 검색 시작", 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       height=40)
        self.search_btn.pack(side="left", padx=5)
        
        self.cancel_btn = ctk.CTkButton(button_frame, text="❌ 취소", 
                                       state="disabled",
                                       height=40)
        self.cancel_btn.pack(side="left", padx=5)
        
        self.export_btn = ctk.CTkButton(button_frame, text="📊 Excel 내보내기", 
                                       state="disabled",
                                       height=40,
                                       fg_color="#2d5a2d",
                                       hover_color="#1e3a1e")
        self.export_btn.pack(side="right", padx=5)
        
        self.clear_btn = ctk.CTkButton(button_frame, text="🗑️ 결과 지우기", 
                                      height=40)
        self.clear_btn.pack(side="right", padx=5)
    
    def get_search_config(self):
        """검색 설정 반환"""
        return {
            'search_dir': self.dir_entry.get().strip(),
            'keyword': self.keyword_entry.get().strip(),
            'use_regex': self.regex_var.get(),
            'case_sensitive': self.case_var.get(),
            'whole_word': self.word_var.get(),
            'extensions': [ext.strip() for ext in self.extensions_entry.get().split(",") if ext.strip()],
            'exclude_patterns': [pattern.strip() for pattern in self.exclude_entry.get().split(",") if pattern.strip()],
            'encoding': self.encoding_combo.get(),
            'output_file': self.output_entry.get().strip()
        }
    
    def set_search_config(self, config):
        """검색 설정 설정"""
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, config.get('search_directory', ''))
        
        self.keyword_entry.delete(0, tk.END)
        self.keyword_entry.insert(0, config.get('keyword', ''))
        
        self.regex_var.set(config.get('use_regex', True))
        self.case_var.set(config.get('case_sensitive', False))
        self.word_var.set(config.get('whole_word', False))
        
        extensions = config.get('file_extensions', [".java", ".xml", ".properties"])
        self.extensions_entry.delete(0, tk.END)
        self.extensions_entry.insert(0, ", ".join(extensions))
        
        exclude_patterns = config.get('exclude_patterns', [])
        self.exclude_entry.delete(0, tk.END)
        self.exclude_entry.insert(0, ", ".join(exclude_patterns))
        
        self.encoding_combo.set(config.get('file_encoding', 'utf-8'))
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, config.get('output_file', 'search_results.xlsx'))
    
    def update_recent_combos(self, recent_searches, recent_directories):
        """최근 검색 콤보박스 업데이트"""
        if recent_searches:
            self.recent_search_combo.configure(values=["최근 검색"] + recent_searches)
            self.recent_search_combo.set("최근 검색")
        
        if recent_directories:
            self.recent_dir_combo.configure(values=["최근 디렉토리"] + recent_directories)
            self.recent_dir_combo.set("최근 디렉토리")
