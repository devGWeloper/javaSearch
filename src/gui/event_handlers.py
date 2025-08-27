import threading
import os
import sys
import webbrowser
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


class SearchEventHandler:
    """검색 관련 이벤트 핸들러"""
    
    def __init__(self, main_app, search_panel, results_panel):
        self.main_app = main_app
        self.search_panel = search_panel
        self.results_panel = results_panel
        self.is_searching = False
        self.bind_events()
    
    def bind_events(self):
        """이벤트 바인딩"""
        self.search_panel.search_btn.configure(command=self.start_search)
        self.search_panel.cancel_btn.configure(command=self.cancel_search)
        self.search_panel.clear_btn.configure(command=self.clear_results)
        self.search_panel.browse_btn.configure(command=self.browse_directory)
        self.search_panel.recent_dir_combo.configure(command=self.on_recent_dir_selected)
        self.search_panel.recent_search_combo.configure(command=self.on_recent_search_selected)
        self.search_panel.keyword_entry.bind("<Return>", lambda e: self.start_search())
    
    def browse_directory(self):
        """디렉토리 선택"""
        directory = filedialog.askdirectory(title="검색할 프로젝트 디렉토리를 선택하세요")
        if directory:
            self.search_panel.dir_entry.delete(0, tk.END)
            self.search_panel.dir_entry.insert(0, directory)
    
    def on_recent_dir_selected(self, selection):
        """최근 디렉토리 선택"""
        if selection and selection != "최근 디렉토리":
            self.search_panel.dir_entry.delete(0, tk.END)
            self.search_panel.dir_entry.insert(0, selection)
    
    def on_recent_search_selected(self, selection):
        """최근 검색어 선택"""
        if selection and selection != "최근 검색":
            self.search_panel.keyword_entry.delete(0, tk.END)
            self.search_panel.keyword_entry.insert(0, selection)
    
    def start_search(self):
        """검색 시작"""
        if self.is_searching:
            return
        
        # 입력 검증
        config = self.search_panel.get_search_config()
        search_dir = config['search_dir']
        keyword = config['keyword']
        
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
        self.search_panel.search_btn.configure(state="disabled")
        self.search_panel.cancel_btn.configure(state="normal")
        self.results_panel.show_progress()
        
        # 결과 초기화
        self.results_panel.clear_results()
        
        # 검색 설정
        extensions = config['extensions']
        if not extensions:
            extensions = [".java", ".xml", ".properties"]
        
        exclude_patterns = config['exclude_patterns']
        
        # 최근 검색 기록 추가
        self.main_app.config_manager.add_recent_search(keyword)
        self.main_app.config_manager.add_recent_directory(search_dir)
        self.main_app.update_recent_combos()
        
        # 비동기 검색 시작
        search_thread = threading.Thread(
            target=self._search_worker,
            args=(search_dir, keyword, extensions, exclude_patterns, config)
        )
        search_thread.daemon = True
        search_thread.start()
    
    def _search_worker(self, search_dir, keyword, extensions, exclude_patterns, config):
        """검색 워커 스레드"""
        try:
            results = self.main_app.search_engine.search(
                search_dir=search_dir,
                keyword=keyword,
                use_regex=config['use_regex'],
                case_sensitive=config['case_sensitive'],
                whole_word=config['whole_word'],
                file_extensions=tuple(extensions),
                exclude_patterns=exclude_patterns,
                file_encoding=config['encoding'],
                progress_callback=self.results_panel.update_progress,
                result_callback=self.results_panel.add_result_batch
            )
            
            # 검색 완료
            self.main_app.root.after(0, self._search_completed, results)
            
        except Exception as e:
            self.main_app.root.after(0, self._search_error, str(e))
    
    def _search_completed(self, results):
        """검색 완료"""
        self.is_searching = False
        self.search_panel.search_btn.configure(state="normal")
        self.search_panel.cancel_btn.configure(state="disabled")
        self.results_panel.hide_progress()
        
        if results:
            self.search_panel.export_btn.configure(state="normal", text=f"📊 Excel 내보내기 ({len(results)}건)")
            messagebox.showinfo("검색 완료", f"검색이 완료되었습니다.\n총 {len(results)}건의 결과를 찾았습니다.\n\nExcel 내보내기 버튼을 클릭하여 결과를 저장할 수 있습니다.")
        else:
            self.search_panel.export_btn.configure(state="disabled", text="📊 Excel 내보내기")
            messagebox.showinfo("검색 완료", "검색 결과가 없습니다.")
    
    def _search_error(self, error_message):
        """검색 오류"""
        self.is_searching = False
        self.search_panel.search_btn.configure(state="normal")
        self.search_panel.cancel_btn.configure(state="disabled")
        self.results_panel.hide_progress()
        
        messagebox.showerror("검색 오류", f"검색 중 오류가 발생했습니다:\n{error_message}")
    
    def cancel_search(self):
        """검색 취소"""
        self.main_app.search_engine.cancel_current_search()
        self.is_searching = False
        self.search_panel.search_btn.configure(state="normal")
        self.search_panel.cancel_btn.configure(state="disabled")
        self.results_panel.hide_progress()
    
    def clear_results(self):
        """결과 지우기"""
        self.results_panel.clear_results()
        self.search_panel.export_btn.configure(state="disabled", text="📊 Excel 내보내기")


class ExportEventHandler:
    """내보내기 관련 이벤트 핸들러"""
    
    def __init__(self, main_app, search_panel, results_panel):
        self.main_app = main_app
        self.search_panel = search_panel
        self.results_panel = results_panel
        self.is_exporting = False
        self.export_tooltip = None
        self.bind_events()
    
    def bind_events(self):
        """이벤트 바인딩"""
        self.search_panel.export_btn.configure(command=self.export_results)
        self.search_panel.export_btn.bind("<Enter>", self.show_export_tooltip)
        self.search_panel.export_btn.bind("<Leave>", self.hide_export_tooltip)
    
    def export_results(self):
        """Excel로 내보내기"""
        if not self.results_panel.get_all_results():
            messagebox.showwarning("경고", "내보낼 결과가 없습니다.")
            return
        
        # 내보내기 중 중복 실행 방지
        if self.is_exporting:
            messagebox.showwarning("경고", "이미 내보내기가 진행 중입니다.")
            return
        
        # 기본 파일명 설정
        default_filename = "search_results.xlsx"
        output_file = self.search_panel.output_entry.get().strip()
        if not output_file:
            output_file = default_filename
        elif not output_file.endswith('.xlsx'):
            output_file += '.xlsx'
        
        # 파일 저장 대화상자
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=output_file,
            title="Excel 파일로 저장 (중복 시 자동으로 _1, _2 추가)",
            confirmoverwrite=False
        )
        
        if file_path:
            # 파일명 중복 확인 및 사용자 안내
            if Path(file_path).exists():
                info_result = messagebox.askyesno(
                    "파일명 중복 안내",
                    f"📁 '{Path(file_path).name}' 파일이 이미 존재합니다.\n\n"
                    f"💡 기존 파일을 덮어쓰지 않고, 자동으로 '_1', '_2'를 붙여서\n"
                    f"새로운 파일을 생성합니다.\n\n"
                    f"계속 진행하시겠습니까?",
                    icon='info'
                )
                
                if not info_result:
                    return
            
            # 내보내기 상태 설정
            self.is_exporting = True
            self.search_panel.export_btn.configure(state="disabled", text="📊 내보내기 중...")
            
            # 진행률 표시
            self.results_panel.show_progress()
            
            # 비동기로 Excel 내보내기 실행
            export_thread = threading.Thread(
                target=self._export_worker,
                args=(file_path, output_file),
                daemon=True
            )
            export_thread.start()
    
    def _export_worker(self, file_path, output_file):
        """Excel 내보내기 워커 스레드"""
        try:
            # 검색 엔진을 통해 Excel 내보내기 실행
            success = self.main_app.search_engine.export_to_excel(
                self.results_panel.get_all_results(), file_path
            )
            
            # UI 업데이트는 메인 스레드에서 실행
            self.main_app.root.after(0, self._export_completed, success, file_path, output_file)
            
        except Exception as e:
            # 오류 발생 시 UI 업데이트
            self.main_app.root.after(0, self._export_error, str(e))
    
    def _export_completed(self, success, file_path, output_file):
        """Excel 내보내기 완료 처리"""
        try:
            # 진행률 숨김
            self.results_panel.hide_progress()
            
            if success:
                # 실제 저장된 파일 경로 확인
                actual_file_path = self._get_actual_saved_file_path(file_path)
                original_filename = Path(file_path).name
                
                if actual_file_path != file_path:
                    messagebox.showinfo("내보내기 완료", 
                        f"📁 파일명이 중복되어 자동으로 변경되었습니다:\n\n"
                        f"📝 원본 파일명: {original_filename}\n"
                        f"🔄 변경된 파일명: {Path(actual_file_path).name}\n\n"
                        f"💾 저장 위치: {actual_file_path}\n\n"
                        f"💡 기존 파일은 그대로 유지되며, 새로운 파일이 생성되었습니다.")
                else:
                    messagebox.showinfo("내보내기 완료", 
                        f"✅ Excel 내보내기가 완료되었습니다!\n\n"
                        f"📁 저장 위치: {file_path}\n"
                        f"📊 총 {self.results_panel.get_results_count()}건의 검색 결과가 저장되었습니다.")
                
                # 성공적으로 저장된 파일 경로를 output_entry에 업데이트
                self.search_panel.output_entry.delete(0, tk.END)
                self.search_panel.output_entry.insert(0, str(Path(actual_file_path).name))
                
                # 내보내기 완료 후 버튼 상태 업데이트
                self.search_panel.export_btn.configure(text=f"📊 Excel 내보내기 ({self.results_panel.get_results_count()}건) - 완료!")
                self.main_app.root.after(2000, lambda: self.search_panel.export_btn.configure(text=f"📊 Excel 내보내기 ({self.results_panel.get_results_count()}건)"))
                
            else:
                messagebox.showerror("오류", "Excel 파일 저장 중 오류가 발생했습니다.")
                self.search_panel.export_btn.configure(state="normal", text=f"📊 Excel 내보내기 ({self.results_panel.get_results_count()}건)")
                
        except Exception as e:
            messagebox.showerror("오류", f"내보내기 완료 처리 중 오류가 발생했습니다:\n{str(e)}")
            print(f"내보내기 완료 처리 오류: {e}")
        finally:
            # 내보내기 상태 해제
            self.is_exporting = False
            self.search_panel.export_btn.configure(state="normal")
    
    def _export_error(self, error_message):
        """Excel 내보내기 오류 처리"""
        try:
            # 진행률 숨김
            self.results_panel.hide_progress()
            
            messagebox.showerror("오류", f"Excel 내보내기 중 오류가 발생했습니다:\n{error_message}")
            print(f"Excel 내보내기 오류 상세: {error_message}")
            
        except Exception as e:
            print(f"오류 처리 중 추가 오류: {e}")
        finally:
            # 내보내기 상태 해제
            self.is_exporting = False
            self.search_panel.export_btn.configure(state="normal", text=f"📊 Excel 내보내기 ({self.results_panel.get_results_count()}건)")
    
    def _get_actual_saved_file_path(self, original_path: str) -> str:
        """실제로 저장된 파일 경로를 찾습니다"""
        path = Path(original_path)
        if path.exists():
            return str(path)
        
        # 파일명이 자동으로 변경되었을 가능성 확인
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        
        counter = 1
        while True:
            new_filename = f"{stem}_{counter}{suffix}"
            new_path = parent / new_filename
            if new_path.exists():
                return str(new_path)
            counter += 1
            # 무한 루프 방지 (최대 1000번까지 시도)
            if counter > 1000:
                break
        
        # 찾지 못한 경우 원본 경로 반환
        return original_path
    
    def show_export_tooltip(self, event):
        """Excel 내보내기 버튼 툴팁 표시"""
        if self.search_panel.export_btn.cget("state") == "disabled":
            tooltip_text = "검색 결과가 없습니다. 먼저 검색을 실행해주세요."
        else:
            tooltip_text = f"검색 결과 {self.results_panel.get_results_count()}건을 Excel 파일로 내보냅니다.\n\n💡 파일명이 중복되면 자동으로 _1, _2를 붙여서 새 파일을 생성합니다."
        
        # 툴팁 위치 계산
        x = self.search_panel.export_btn.winfo_rootx() + self.search_panel.export_btn.winfo_width() // 2
        y = self.search_panel.export_btn.winfo_rooty() - 30
        
        # 기존 툴팁 제거
        if self.export_tooltip:
            self.export_tooltip.destroy()
        
        # 새 툴팁 생성
        self.export_tooltip = tk.Toplevel(self.main_app.root)
        self.export_tooltip.wm_overrideredirect(True)
        self.export_tooltip.wm_geometry(f"+{x}+{y}")
        
        # 툴팁 스타일
        tooltip_label = tk.Label(self.export_tooltip, text=tooltip_text, 
                                bg="#2b2b2b", fg="white", 
                                relief="solid", borderwidth=1,
                                font=("Arial", 10))
        tooltip_label.pack(padx=5, pady=3)
        
        # 자동 숨김
        self.main_app.root.after(3000, lambda: self.hide_export_tooltip())
    
    def hide_export_tooltip(self, event=None):
        """Excel 내보내기 버튼 툴팁 숨김"""
        if self.export_tooltip:
            self.export_tooltip.destroy()
            self.export_tooltip = None


class FileEventHandler:
    """파일 관련 이벤트 핸들러"""
    
    def __init__(self, main_app, results_panel):
        self.main_app = main_app
        self.results_panel = results_panel
        self.bind_events()
    
    def bind_events(self):
        """이벤트 바인딩"""
        self.results_panel.bind_double_click(self.open_selected_file)
        self.results_panel.bind_right_click(self.show_context_menu)
        
        # 컨텍스트 메뉴 이벤트
        self.results_panel.context_menu.entryconfig("파일 열기", command=self.open_selected_file)
        self.results_panel.context_menu.entryconfig("폴더 열기", command=self.open_selected_folder)
        self.results_panel.context_menu.entryconfig("경로 복사", command=self.copy_selected_path)
    
    def open_selected_file(self, event=None):
        """선택된 파일 열기"""
        result = self.results_panel.get_selected_result()
        if not result:
            return
        
        try:
            if sys.platform.startswith('darwin'):  # macOS
                os.system(f'open "{result.file_path}"')
            elif sys.platform.startswith('win'):  # Windows
                os.startfile(result.file_path)
            else:  # Linux
                os.system(f'xdg-open "{result.file_path}"')
        except Exception as e:
            messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{e}")
    
    def open_selected_folder(self):
        """선택된 파일의 폴더 열기"""
        result = self.results_panel.get_selected_result()
        if not result:
            return
        
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
    
    def copy_selected_path(self):
        """선택된 파일 경로 복사"""
        result = self.results_panel.get_selected_result()
        if not result:
            return
        
        self.main_app.root.clipboard_clear()
        self.main_app.root.clipboard_append(result.file_path)
        messagebox.showinfo("복사 완료", "파일 경로가 클립보드에 복사되었습니다.")
    
    def show_context_menu(self, event):
        """컨텍스트 메뉴 표시"""
        try:
            self.results_panel.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.results_panel.context_menu.grab_release()
