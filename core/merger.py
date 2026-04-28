import os
from utils.file_reader import read_file

_SEPARATOR = "=" * 80


def merge_files(file_paths: list) -> tuple:
    """
    Returns (merged_text: str, warnings: list[str])
    """
    parts = []
    warnings = []

    for path in file_paths:
        filename = os.path.basename(path)
        try:
            content = read_file(path)
        except (OSError, UnicodeDecodeError) as e:
            warnings.append(f"[건너뜀] {filename}: {e}")
            continue

        header = f"{_SEPARATOR}\n=== {filename} ===\n{_SEPARATOR}"
        parts.append(f"{header}\n{content}")

    merged = "\n\n".join(parts)
    return merged, warnings
