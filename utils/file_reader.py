import os

_ENCODINGS = ["utf-8", "cp949", "euc-kr", "latin-1"]


def read_file(path: str) -> str:
    for encoding in _ENCODINGS:
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except OSError as e:
            raise OSError(f"파일을 열 수 없습니다: {path}") from e
    raise UnicodeDecodeError(
        "multiple", b"", 0, 1, f"지원되지 않는 인코딩: {os.path.basename(path)}"
    )
