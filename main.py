import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox

sys.path.insert(0, os.path.dirname(__file__))
from core.merger import merge_files


def main():
    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames(
        title="합칠 파일을 선택하세요 (여러 개 선택 가능)",
        filetypes=[("모든 파일", "*.*")],
    )

    if not file_paths:
        messagebox.showinfo("알림", "선택된 파일이 없습니다. 프로그램을 종료합니다.")
        return

    merged_text, warnings = merge_files(list(file_paths))

    if not merged_text.strip():
        messagebox.showerror("오류", "읽을 수 있는 파일이 없습니다.\n\n" + "\n".join(warnings))
        return

    save_path = filedialog.asksaveasfilename(
        title="저장할 파일 경로를 선택하세요",
        defaultextension=".txt",
        filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")],
        initialfile="merged_notes.txt",
    )

    if not save_path:
        messagebox.showinfo("알림", "저장이 취소되었습니다.")
        return

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(merged_text)

    success_count = len(file_paths) - len(warnings)
    detail = f"합쳐진 파일 수: {success_count}개\n저장 경로: {save_path}"
    if warnings:
        detail += f"\n\n건너뛴 파일 ({len(warnings)}개):\n" + "\n".join(warnings)

    messagebox.showinfo("완료", detail)


if __name__ == "__main__":
    main()
