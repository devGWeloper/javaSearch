import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from pathlib import Path
import sys
import webbrowser

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.search_engine import SearchEngine, SearchResult
from src.core.config_manager import ConfigManager


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
        self.search_results = []
        self.is_searching = False
        
        # UI 구성
        self.setup_ui()
        self.load_settings()
        
        # 윈도우 닫기 이벤트
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """UI 구성"""
        # 메인 컨테이너
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 상단 검색 설정 패널
        self.setup_search_panel()
        
        # 하단 결과 패널
        self.setup_results_panel()
    
    def setup_search_panel(self):
        """검색 설정 패널 구성"""
        # 검색 패널 프레임
        search_frame = ctk.CTkFrame(self.main_container)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        # 제목
        title_label = ctk.CTkLabel(search_frame, text="🔍 Java Project Search", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        # 메인 검색 설정
        main_search_frame = ctk.CTkFrame(search_frame)
        main_search_frame.pack(fill="x", padx=10, pady=5)
        
        # 검색 디렉토리
        dir_frame = ctk.CTkFrame(main_search_frame)
        dir_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(dir_frame, text="검색 디렉토리:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        dir_input_frame = ctk.CTkFrame(dir_frame)
        dir_input_frame.pack(fill="x", padx=10, pady=(5,10))
        
        self.dir_entry = ctk.CTkEntry(dir_input_frame, placeholder_text="검색할 프로젝트 경로를 선택하세요...")
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(5,5))
        
        self.browse_btn = ctk.CTkButton(dir_input_frame, text="찾아보기", width=100,
                                       command=self.browse_directory)
        self.browse_btn.pack(side="right", padx=(5,5))
        
        # 최근 디렉토리 콤보박스
        self.recent_dir_combo = ctk.CTkComboBox(dir_input_frame, width=120,
                                               command=self.on_recent_dir_selected,
                                               values=["최근 디렉토리"])
        self.recent_dir_combo.set("최근 디렉토리")
        self.recent_dir_combo.pack(side="right", padx=(5,5))
        
        # 검색 키워드
        keyword_frame = ctk.CTkFrame(main_search_frame)
        keyword_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(keyword_frame, text="검색 키워드:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        keyword_input_frame = ctk.CTkFrame(keyword_frame)
        keyword_input_frame.pack(fill="x", padx=10, pady=(5,10))
        
        self.keyword_entry = ctk.CTkEntry(keyword_input_frame, placeholder_text="검색할 키워드를 입력하세요...")
        self.keyword_entry.pack(side="left", fill="x", expand=True, padx=(5,5))
        self.keyword_entry.bind("<Return>", lambda e: self.start_search())
        
        # 최근 검색어 콤보박스
        self.recent_search_combo = ctk.CTkComboBox(keyword_input_frame, width=120,
                                                  command=self.on_recent_search_selected,
                                                  values=["최근 검색"])
        self.recent_search_combo.set("최근 검색")
        self.recent_search_combo.pack(side="right", padx=(5,5))
        
        # 검색 옵션
        options_frame = ctk.CTkFrame(main_search_frame)
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
        
        # 파일 확장자
        ext_frame = ctk.CTkFrame(main_search_frame)
        ext_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(ext_frame, text="파일 확장자:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        self.extensions_entry = ctk.CTkEntry(ext_frame, placeholder_text=".java, .xml, .properties")
        self.extensions_entry.pack(fill="x", padx=10, pady=(5,10))
        
        # 제외 패턴
        exclude_frame = ctk.CTkFrame(main_search_frame)
        exclude_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(exclude_frame, text="제외 패턴:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        self.exclude_entry = ctk.CTkEntry(exclude_frame, placeholder_text="*/target/*, */build/*, */.git/*")
        self.exclude_entry.pack(fill="x", padx=10, pady=(5,10))
        
        # 고급 옵션
        advanced_frame = ctk.CTkFrame(main_search_frame)
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
        
        # 검색 버튼
        button_frame = ctk.CTkFrame(search_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.search_btn = ctk.CTkButton(button_frame, text="🔍 검색 시작", 
                                       command=self.start_search,
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       height=40)
        self.search_btn.pack(side="left", padx=5)
        
        self.cancel_btn = ctk.CTkButton(button_frame, text="❌ 취소", 
                                       command=self.cancel_search,
                                       state="disabled",
                                       height=40)
        self.cancel_btn.pack(side="left", padx=5)
        
        self.export_btn = ctk.CTkButton(button_frame, text="📊 Excel 내보내기", 
                                       command=self.export_results,
                                       state="disabled",
                                       height=40)
        self.export_btn.pack(side="right", padx=5)
        
        self.clear_btn = ctk.CTkButton(button_frame, text="🗑️ 결과 지우기", 
                                      command=self.clear_results,
                                      height=40)
        self.clear_btn.pack(side="right", padx=5)
    
    def setup_results_panel(self):
        """결과 패널 구성"""
        # 결과 패널 프레임
        results_frame = ctk.CTkFrame(self.main_container)
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 결과 헤더
        header_frame = ctk.CTkFrame(results_frame)
        header_frame.pack(fill="x", padx=10, pady=(10,5))
        
        self.results_label = ctk.CTkLabel(header_frame, text="검색 결과", 
                                         font=ctk.CTkFont(size=16, weight="bold"))
        self.results_label.pack(side="left", padx=10)
        
        self.count_label = ctk.CTkLabel(header_frame, text="0건")
        self.count_label.pack(side="right", padx=10)
        
        # 진행률 표시
        self.progress_frame = ctk.CTkFrame(results_frame)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        self.progress_frame.pack_forget()  # 초기에는 숨김
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="")
        self.progress_label.pack(padx=10, pady=(0,5))
        
        # 결과 트리뷰
        tree_frame = ctk.CTkFrame(results_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(5,10))
        
        # Treeview 스타일 설정
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", 
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#404040", foreground="white", 
                       borderwidth=1)
        style.map("Treeview", background=[("selected", "#1f538d")])
        
        # 트리뷰 생성
        columns = ("file", "line", "content", "match")
        self.results_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # 컬럼 설정
        self.results_tree.heading("file", text="파일")
        self.results_tree.heading("line", text="라인")
        self.results_tree.heading("content", text="내용")
        self.results_tree.heading("match", text="매칭")
        
        self.results_tree.column("file", width=300, anchor="w")
        self.results_tree.column("line", width=60, anchor="center")
        self.results_tree.column("content", width=500, anchor="w")
        self.results_tree.column("match", width=150, anchor="w")
        
        # 스크롤바
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.results_tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 패킹
        self.results_tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # 더블클릭 이벤트
        self.results_tree.bind("<Double-1>", self.on_result_double_click)
        
        # 컨텍스트 메뉴
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="파일 열기", command=self.open_selected_file)
        self.context_menu.add_command(label="폴더 열기", command=self.open_selected_folder)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="경로 복사", command=self.copy_selected_path)
        
        self.results_tree.bind("<Button-3>", self.show_context_menu)
    
    def browse_directory(self):
        """디렉토리 선택"""
        directory = filedialog.askdirectory(title="검색할 프로젝트 디렉토리를 선택하세요")
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def on_recent_dir_selected(self, selection):
        """최근 디렉토리 선택"""
        if selection and selection != "최근 디렉토리":
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, selection)
    
    def on_recent_search_selected(self, selection):
        """최근 검색어 선택"""
        if selection and selection != "최근 검색":
            self.keyword_entry.delete(0, tk.END)
            self.keyword_entry.insert(0, selection)
    
    def start_search(self):
        """검색 시작"""
        if self.is_searching:
            return
        
        # 입력 검증
        search_dir = self.dir_entry.get().strip()
        keyword = self.keyword_entry.get().strip()
        
        if not search_dir:
            messagebox.showerror("오류", "검색 디렉토리를 선택해주세요.")
            return
        
        if not keyword:
            messagebox.showerror("오류", "검색할 키워드를 입력해주세요.")
            return
        
        if not os.path.exists(search_dir):
            messagebox.showerror("오류", f"디렉토리가 존재하지 않습니다: {search_dir}")
            return
        
        # UI 상태 변경
        self.is_searching = True
        self.search_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_frame.pack(fill="x", padx=10, pady=5, before=self.results_tree.master)
        
        # 결과 초기화
        self.clear_results()
        
        # 검색 설정
        extensions = [ext.strip() for ext in self.extensions_entry.get().split(",") if ext.strip()]
        if not extensions:
            extensions = [".java", ".xml", ".properties"]
        
        exclude_patterns = [pattern.strip() for pattern in self.exclude_entry.get().split(",") if pattern.strip()]
        
        # 최근 검색 기록 추가
        self.config_manager.add_recent_search(keyword)
        self.config_manager.add_recent_directory(search_dir)
        self.update_recent_combos()
        
        # 비동기 검색 시작
        search_thread = threading.Thread(
            target=self._search_worker,
            args=(search_dir, keyword, extensions, exclude_patterns)
        )
        search_thread.daemon = True
        search_thread.start()
    
    def _search_worker(self, search_dir, keyword, extensions, exclude_patterns):
        """검색 워커 스레드"""
        try:
            results = self.search_engine.search(
                search_dir=search_dir,
                keyword=keyword,
                use_regex=self.regex_var.get(),
                case_sensitive=self.case_var.get(),
                whole_word=self.word_var.get(),
                file_extensions=tuple(extensions),
                exclude_patterns=exclude_patterns,
                file_encoding=self.encoding_combo.get(),
                progress_callback=self.update_progress,
                result_callback=self.add_result_batch
            )
            
            # 검색 완료
            self.root.after(0, self._search_completed, results)
            
        except Exception as e:
            self.root.after(0, self._search_error, str(e))
    
    def update_progress(self, current, total, current_file):
        """진행률 업데이트"""
        def update_ui():
            if total > 0:
                progress = current / total
                self.progress_bar.set(progress)
                self.progress_label.configure(text=f"검색 중... ({current}/{total}) {Path(current_file).name}")
        
        self.root.after(0, update_ui)
    
    def add_result_batch(self, results):
        """결과 배치 추가"""
        def update_ui():
            for result in results:
                self.results_tree.insert("", "end", values=(
                    result.file_name,
                    result.line_number,
                    result.content[:100] + "..." if len(result.content) > 100 else result.content,
                    result.match_text
                ))
                self.search_results.append(result)
            
            self.count_label.configure(text=f"{len(self.search_results)}건")
        
        self.root.after(0, update_ui)
    
    def _search_completed(self, results):
        """검색 완료"""
        self.is_searching = False
        self.search_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.progress_frame.pack_forget()
        
        if results:
            self.export_btn.configure(state="normal")
            messagebox.showinfo("검색 완료", f"검색이 완료되었습니다.\n총 {len(results)}건의 결과를 찾았습니다.")
        else:
            messagebox.showinfo("검색 완료", "검색 결과가 없습니다.")
    
    def _search_error(self, error_message):
        """검색 오류"""
        self.is_searching = False
        self.search_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.progress_frame.pack_forget()
        
        messagebox.showerror("검색 오류", f"검색 중 오류가 발생했습니다:\n{error_message}")
    
    def cancel_search(self):
        """검색 취소"""
        self.search_engine.cancel_current_search()
        self.is_searching = False
        self.search_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.progress_frame.pack_forget()
    
    def clear_results(self):
        """결과 지우기"""
        self.results_tree.delete(*self.results_tree.get_children())
        self.search_results.clear()
        self.count_label.configure(text="0건")
        self.export_btn.configure(state="disabled")
    
    def export_results(self):
        """Excel로 내보내기"""
        if not self.search_results:
            messagebox.showwarning("경고", "내보낼 결과가 없습니다.")
            return
        
        output_file = self.output_entry.get().strip()
        if not output_file:
            output_file = "search_results.xlsx"
        
        # 파일 저장 대화상자
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialvalue=output_file
        )
        
        if file_path:
            if self.search_engine.export_to_excel(self.search_results, file_path):
                messagebox.showinfo("내보내기 완료", f"결과가 성공적으로 저장되었습니다:\n{file_path}")
            else:
                messagebox.showerror("오류", "Excel 파일 저장 중 오류가 발생했습니다.")
    
    def on_result_double_click(self, event):
        """결과 더블클릭"""
        self.open_selected_file()
    
    def show_context_menu(self, event):
        """컨텍스트 메뉴 표시"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def open_selected_file(self):
        """선택된 파일 열기"""
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = self.results_tree.item(selection[0])
        file_name = item["values"][0]
        
        # 전체 경로 찾기
        for result in self.search_results:
            if result.file_name == file_name:
                try:
                    if sys.platform.startswith('darwin'):  # macOS
                        os.system(f'open "{result.file_path}"')
                    elif sys.platform.startswith('win'):  # Windows
                        os.startfile(result.file_path)
                    else:  # Linux
                        os.system(f'xdg-open "{result.file_path}"')
                except Exception as e:
                    messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{e}")
                break
    
    def open_selected_folder(self):
        """선택된 파일의 폴더 열기"""
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = self.results_tree.item(selection[0])
        file_name = item["values"][0]
        
        # 전체 경로 찾기
        for result in self.search_results:
            if result.file_name == file_name:
                folder_path = os.path.dirname(result.file_path)
                try:
                    if sys.platform.startswith('darwin'):  # macOS
                        os.system(f'open "{folder_path}"')
                    elif sys.platform.startswith('win'):  # Windows
                        os.startfile(folder_path)
                    else:  # Linux
                        os.system(f'xdg-open "{folder_path}"')
                except Exception as e:
                    messagebox.showerror("오류", f"폴더를 열 수 없습니다:\n{e}")
                break
    
    def copy_selected_path(self):
        """선택된 파일 경로 복사"""
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = self.results_tree.item(selection[0])
        file_name = item["values"][0]
        
        # 전체 경로 찾기
        for result in self.search_results:
            if result.file_name == file_name:
                self.root.clipboard_clear()
                self.root.clipboard_append(result.file_path)
                messagebox.showinfo("복사 완료", "파일 경로가 클립보드에 복사되었습니다.")
                break
    
    def load_settings(self):
        """설정 로드"""
        self.dir_entry.insert(0, self.config_manager.get("search_directory", ""))
        self.keyword_entry.insert(0, self.config_manager.get("keyword", ""))
        
        self.regex_var.set(self.config_manager.get("use_regex", True))
        self.case_var.set(self.config_manager.get("case_sensitive", False))
        self.word_var.set(self.config_manager.get("whole_word", False))
        
        extensions = self.config_manager.get("file_extensions", [".java", ".xml", ".properties"])
        self.extensions_entry.insert(0, ", ".join(extensions))
        
        exclude_patterns = self.config_manager.get("exclude_patterns", [])
        self.exclude_entry.insert(0, ", ".join(exclude_patterns))
        
        self.encoding_combo.set(self.config_manager.get("file_encoding", "utf-8"))
        self.output_entry.insert(0, self.config_manager.get("output_file", "search_results.xlsx"))
        
        # 윈도우 크기 복원
        geometry = self.config_manager.get("window_geometry", "1200x800+100+100")
        self.root.geometry(geometry)
        
        self.update_recent_combos()
    
    def update_recent_combos(self):
        """최근 검색 콤보박스 업데이트"""
        recent_searches = self.config_manager.get_recent_searches()
        if recent_searches:
            self.recent_search_combo.configure(values=["최근 검색"] + recent_searches)
            self.recent_search_combo.set("최근 검색")
        
        recent_directories = self.config_manager.get_recent_directories()
        if recent_directories:
            self.recent_dir_combo.configure(values=["최근 디렉토리"] + recent_directories)
            self.recent_dir_combo.set("최근 디렉토리")
    
    def save_settings(self):
        """설정 저장"""
        self.config_manager.set("search_directory", self.dir_entry.get())
        self.config_manager.set("keyword", self.keyword_entry.get())
        self.config_manager.set("use_regex", self.regex_var.get())
        self.config_manager.set("case_sensitive", self.case_var.get())
        self.config_manager.set("whole_word", self.word_var.get())
        
        extensions = [ext.strip() for ext in self.extensions_entry.get().split(",") if ext.strip()]
        self.config_manager.set("file_extensions", extensions)
        
        exclude_patterns = [pattern.strip() for pattern in self.exclude_entry.get().split(",") if pattern.strip()]
        self.config_manager.set("exclude_patterns", exclude_patterns)
        
        self.config_manager.set("file_encoding", self.encoding_combo.get())
        self.config_manager.set("output_file", self.output_entry.get())
        self.config_manager.set("window_geometry", self.root.geometry())
        
        self.config_manager.save_config()
    
    def on_closing(self):
        """윈도우 닫기"""
        if self.is_searching:
            self.cancel_search()
        
        self.save_settings()
        self.root.destroy()
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()


if __name__ == "__main__":
    app = JavaSearchApp()
    app.run()
