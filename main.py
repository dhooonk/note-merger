import sys
import os
import tkinter as tk
from tkinter import filedialog, ttk

sys.path.insert(0, os.path.dirname(__file__))
from core.merger import merge_files


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Note Merger")
        self.geometry("600x480")
        self.minsize(480, 360)
        self.configure(bg="#f5f5f5")
        self._build()

    def _build(self):
        pad = {"padx": 12, "pady": 6}

        # 파일 목록 영역
        list_frame = tk.LabelFrame(self, text="선택된 파일", bg="#f5f5f5", font=("", 10))
        list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 4))

        self._count_var = tk.StringVar(value="0개")
        tk.Label(list_frame, textvariable=self._count_var, bg="#f5f5f5",
                 fg="#666", font=("", 9)).pack(anchor="ne", padx=6)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            activestyle="none",
            font=("", 10),
            bd=0,
            highlightthickness=1,
            highlightcolor="#aaa",
            selectbackground="#4a90d9",
            selectforeground="white",
        )
        self._listbox.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))
        scrollbar.config(command=self._listbox.yview)

        # 파일 조작 버튼
        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, padx=12, pady=2)

        self._btn(btn_frame, "파일 추가", self._add_files).pack(side=tk.LEFT, padx=(0, 4))
        self._btn(btn_frame, "선택 삭제", self._remove_selected).pack(side=tk.LEFT, padx=4)
        self._btn(btn_frame, "전체 삭제", self._clear_all).pack(side=tk.LEFT, padx=4)

        # 위아래 순서 이동
        self._btn(btn_frame, "▲", self._move_up, width=3).pack(side=tk.RIGHT, padx=(4, 0))
        self._btn(btn_frame, "▼", self._move_down, width=3).pack(side=tk.RIGHT, padx=4)

        # 저장 경로
        save_frame = tk.LabelFrame(self, text="저장 경로", bg="#f5f5f5", font=("", 10))
        save_frame.pack(fill=tk.X, padx=12, pady=6)

        self._save_path = tk.StringVar()
        path_inner = tk.Frame(save_frame, bg="#f5f5f5")
        path_inner.pack(fill=tk.X, padx=6, pady=6)

        tk.Entry(path_inner, textvariable=self._save_path, font=("", 10)).pack(
            side=tk.LEFT, fill=tk.X, expand=True, ipady=3
        )
        self._btn(path_inner, "찾아보기", self._browse_save).pack(side=tk.LEFT, padx=(6, 0))

        # 합치기 버튼
        merge_btn = tk.Button(
            self,
            text="합 치 기",
            command=self._merge,
            font=("", 12, "bold"),
            bg="#4a90d9",
            fg="white",
            activebackground="#357abd",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
        )
        merge_btn.pack(pady=8)

        # 상태 바
        self._status_var = tk.StringVar(value="파일을 추가하고 합치기를 누르세요.")
        status_bar = tk.Label(
            self,
            textvariable=self._status_var,
            bg="#e0e0e0",
            fg="#444",
            font=("", 9),
            anchor="w",
            padx=10,
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=3)

    def _btn(self, parent, text, command, width=None):
        kw = dict(
            text=text,
            command=command,
            font=("", 9),
            bg="#e8e8e8",
            activebackground="#d0d0d0",
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            pady=4,
        )
        if width:
            kw["width"] = width
        return tk.Button(parent, **kw)

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title="합칠 파일 선택 (여러 개 가능)",
            filetypes=[("모든 파일", "*.*")],
        )
        existing = list(self._listbox.get(0, tk.END))
        added = 0
        for p in paths:
            if p not in existing:
                self._listbox.insert(tk.END, p)
                added += 1
        self._refresh_count()
        if added:
            self._set_status(f"{added}개 파일 추가됨 (총 {self._listbox.size()}개)")

    def _remove_selected(self):
        for i in reversed(self._listbox.curselection()):
            self._listbox.delete(i)
        self._refresh_count()
        self._set_status(f"총 {self._listbox.size()}개 파일")

    def _clear_all(self):
        self._listbox.delete(0, tk.END)
        self._refresh_count()
        self._set_status("목록을 초기화했습니다.")

    def _move_up(self):
        sel = self._listbox.curselection()
        for i in sel:
            if i == 0:
                return
            text = self._listbox.get(i)
            self._listbox.delete(i)
            self._listbox.insert(i - 1, text)
            self._listbox.selection_set(i - 1)

    def _move_down(self):
        sel = self._listbox.curselection()
        for i in reversed(sel):
            if i == self._listbox.size() - 1:
                return
            text = self._listbox.get(i)
            self._listbox.delete(i)
            self._listbox.insert(i + 1, text)
            self._listbox.selection_set(i + 1)

    def _browse_save(self):
        path = filedialog.asksaveasfilename(
            title="저장할 파일 선택",
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")],
            initialfile="merged_notes.txt",
        )
        if path:
            self._save_path.set(path)

    def _merge(self):
        file_paths = list(self._listbox.get(0, tk.END))
        if not file_paths:
            self._set_status("오류: 파일을 먼저 추가하세요.", error=True)
            return

        save_path = self._save_path.get().strip()
        if not save_path:
            self._set_status("오류: 저장 경로를 지정하세요.", error=True)
            return

        self._set_status("합치는 중...")
        self.update_idletasks()

        merged_text, warnings = merge_files(file_paths)

        if not merged_text.strip():
            self._set_status("오류: 읽을 수 있는 파일이 없습니다.", error=True)
            return

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(merged_text)

        success_count = len(file_paths) - len(warnings)
        msg = f"완료: {success_count}개 합침 → {os.path.basename(save_path)}"
        if warnings:
            msg += f"  (건너뜀 {len(warnings)}개)"
        self._set_status(msg)

    def _refresh_count(self):
        self._count_var.set(f"{self._listbox.size()}개")

    def _set_status(self, msg, error=False):
        self._status_var.set(msg)


if __name__ == "__main__":
    App().mainloop()
