import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.merger import merge_files
from utils.file_reader import read_file


class TestReadFile:
    def test_utf8(self, tmp_path):
        f = tmp_path / "note.txt"
        f.write_text("안녕하세요", encoding="utf-8")
        assert read_file(str(f)) == "안녕하세요"

    def test_cp949(self, tmp_path):
        f = tmp_path / "note_cp949.txt"
        f.write_bytes("안녕하세요".encode("cp949"))
        assert read_file(str(f)) == "안녕하세요"

    def test_ascii(self, tmp_path):
        f = tmp_path / "note.log"
        f.write_text("hello world", encoding="utf-8")
        assert read_file(str(f)) == "hello world"

    def test_missing_file(self, tmp_path):
        with pytest.raises(OSError):
            read_file(str(tmp_path / "nonexistent.txt"))


class TestMergeFiles:
    def test_basic_merge(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.md"
        f1.write_text("내용A", encoding="utf-8")
        f2.write_text("내용B", encoding="utf-8")

        merged, warnings = merge_files([str(f1), str(f2)])
        assert "a.txt" in merged
        assert "내용A" in merged
        assert "b.md" in merged
        assert "내용B" in merged
        assert warnings == []

    def test_header_format(self, tmp_path):
        f = tmp_path / "memo.txt"
        f.write_text("테스트", encoding="utf-8")
        merged, _ = merge_files([str(f)])
        assert "=== memo.txt ===" in merged
        assert "=" * 80 in merged

    def test_order_preserved(self, tmp_path):
        files = []
        for i in range(5):
            f = tmp_path / f"file_{i}.txt"
            f.write_text(f"내용{i}", encoding="utf-8")
            files.append(str(f))

        merged, _ = merge_files(files)
        positions = [merged.index(f"내용{i}") for i in range(5)]
        assert positions == sorted(positions)

    def test_skip_unreadable_file(self, tmp_path):
        good = tmp_path / "good.txt"
        good.write_text("좋은 파일", encoding="utf-8")
        bad = tmp_path / "missing.txt"

        merged, warnings = merge_files([str(good), str(bad)])
        assert "좋은 파일" in merged
        assert len(warnings) == 1
        assert "missing.txt" in warnings[0]

    def test_thirty_files(self, tmp_path):
        paths = []
        for i in range(30):
            f = tmp_path / f"memo_{i:02d}.txt"
            f.write_text(f"메모 {i}", encoding="utf-8")
            paths.append(str(f))

        merged, warnings = merge_files(paths)
        assert warnings == []
        for i in range(30):
            assert f"메모 {i}" in merged

    def test_various_extensions(self, tmp_path):
        exts = [".txt", ".md", ".log", ".csv", ".json", ".py"]
        paths = []
        for ext in exts:
            f = tmp_path / f"file{ext}"
            f.write_text(f"content of {ext}", encoding="utf-8")
            paths.append(str(f))

        merged, warnings = merge_files(paths)
        assert warnings == []
        for ext in exts:
            assert f"content of {ext}" in merged
