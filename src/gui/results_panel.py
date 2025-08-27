import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from pathlib import Path


class ResultsPanel:
    """검색 결과 표시 패널 UI 컴포넌트"""
    
    def __init__(self, parent):
        self.parent = parent
        self.search_results = []
        self.setup_ui()
    
    def setup_ui(self):
        """결과 패널 UI 구성"""
        # 결과 패널 프레임
        self.results_frame = ctk.CTkFrame(self.parent)
        self.results_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 결과 헤더
        self.setup_header_frame()
        
        # 진행률 표시
        self.setup_progress_frame()
        
        # 결과 트리뷰
        self.setup_tree_frame()
        
        # 컨텍스트 메뉴
        self.setup_context_menu()
    
    def setup_header_frame(self):
        """결과 헤더 프레임"""
        header_frame = ctk.CTkFrame(self.results_frame)
        header_frame.pack(fill="x", padx=10, pady=(10,5))
        
        self.results_label = ctk.CTkLabel(header_frame, text="검색 결과", 
                                         font=ctk.CTkFont(size=16, weight="bold"))
        self.results_label.pack(side="left", padx=10)
        
        self.count_label = ctk.CTkLabel(header_frame, text="0건")
        self.count_label.pack(side="right", padx=10)
    
    def setup_progress_frame(self):
        """진행률 표시 프레임"""
        self.progress_frame = ctk.CTkFrame(self.results_frame)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        self.progress_frame.pack_forget()  # 초기에는 숨김
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="")
        self.progress_label.pack(padx=10, pady=(0,5))
    
    def setup_tree_frame(self):
        """결과 트리뷰 프레임"""
        tree_frame = ctk.CTkFrame(self.results_frame)
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
    
    def setup_context_menu(self):
        """컨텍스트 메뉴 설정"""
        self.context_menu = tk.Menu(self.parent, tearoff=0)
        self.context_menu.add_command(label="파일 열기")
        self.context_menu.add_command(label="폴더 열기")
        self.context_menu.add_separator()
        self.context_menu.add_command(label="경로 복사")
    
    def show_progress(self):
        """진행률 표시"""
        self.progress_frame.pack(fill="x", padx=10, pady=5, before=self.results_tree.master)
    
    def hide_progress(self):
        """진행률 숨김"""
        self.progress_frame.pack_forget()
    
    def update_progress(self, current, total, current_file):
        """진행률 업데이트"""
        if total > 0:
            progress = current / total
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"검색 중... ({current}/{total}) {Path(current_file).name}")
    
    def add_result_batch(self, results):
        """결과 배치 추가"""
        for result in results:
            self.results_tree.insert("", "end", values=(
                result.file_name,
                result.line_number,
                result.content[:100] + "..." if len(result.content) > 100 else result.content,
                result.match_text
            ))
            self.search_results.append(result)
        
        self.count_label.configure(text=f"{len(self.search_results)}건")
    
    def clear_results(self):
        """결과 지우기"""
        self.results_tree.delete(*self.results_tree.get_children())
        self.search_results.clear()
        self.count_label.configure(text="0건")
    
    def get_selected_result(self):
        """선택된 결과 반환"""
        selection = self.results_tree.selection()
        if not selection:
            return None
        
        item = self.results_tree.item(selection[0])
        file_name = item["values"][0]
        
        # 전체 경로 찾기
        for result in self.search_results:
            if result.file_name == file_name:
                return result
        
        return None
    
    def bind_double_click(self, callback):
        """더블클릭 이벤트 바인딩"""
        self.results_tree.bind("<Double-1>", callback)
    
    def bind_right_click(self, callback):
        """우클릭 이벤트 바인딩"""
        self.results_tree.bind("<Button-3>", callback)
    
    def get_results_count(self):
        """결과 개수 반환"""
        return len(self.search_results)
    
    def get_all_results(self):
        """모든 결과 반환"""
        return self.search_results.copy()
