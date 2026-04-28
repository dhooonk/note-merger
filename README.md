# note_merger

> 여러 메모 파일을 하나로 합쳐주는 Python GUI 프로그램 — 확장자 무관, 30개 이상 동시 선택 가능

[![버전](https://img.shields.io/badge/version-1.0.0-blue)](docs/Change/CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 목차

- [개요](#개요)
- [개발 배경](#개발-배경)
- [목적](#목적)
- [구현 사항](#구현-사항)
- [프로젝트 구조](#프로젝트-구조)
- [요구 사항](#요구-사항)
- [실행 방법](#실행-방법)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [버전 히스토리](#버전-히스토리)
- [라이선스](#라이선스)

---

## 개요

확장자에 상관없이 텍스트로 열 수 있는 파일이라면 모두 불러와 하나의 파일에 차곡차곡 합쳐주는 프로그램입니다.

## 개발 배경

여러 곳에 흩어진 메모 파일을 하나로 정리할 필요가 생겼으나, 수작업으로 복사-붙여넣기를 반복하는 것은 비효율적입니다. 이를 자동화하기 위해 제작했습니다.

## 목적

- 메모 파일 통합 작업의 자동화
- GUI로 비개발자도 쉽게 사용 가능
- 한글 파일명 및 다양한 인코딩 환경 지원

## 구현 사항

- tkinter GUI 파일 선택 창 (30개 이상 동시 선택)
- UTF-8 / CP949 / EUC-KR / Latin-1 멀티 인코딩 자동 감지
- 각 파일 사이에 파일명 헤더 삽입
- 읽기 실패 파일 건너뛰기 및 경고 표시
- 저장 경로 선택 창 및 완료 팝업

## 프로젝트 구조

```
note_merger/
├── main.py              # 진입점 — GUI 흐름 제어
├── core/
│   └── merger.py        # 파일 합치기 핵심 로직
├── utils/
│   └── file_reader.py   # 멀티 인코딩 파일 읽기
├── tests/
│   └── test_merger.py   # pytest 테스트
├── docs/
│   ├── decisions/       # 기술 결정 기록
│   ├── failures/        # 실패 기록
│   ├── domain/          # 용어 사전
│   └── Change/          # CHANGELOG
├── requirements.txt
├── README.md
└── .gitignore
```

## 요구 사항

- Python 3.8 이상
- tkinter (Python 표준 라이브러리 포함, 별도 설치 불필요)
- pytest (테스트 실행 시)

```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
cd note_merger
python main.py
```

1. 파일 선택 창에서 합칠 파일들을 선택합니다 (Ctrl/Cmd 클릭으로 여러 개 선택).
2. 저장 경로 창에서 결과 파일 이름과 위치를 지정합니다.
3. 완료 팝업에서 합쳐진 파일 수와 저장 경로를 확인합니다.

### 테스트 실행

```bash
pytest tests/
```

## 주요 기능

- **멀티 파일 선택**: GUI 창에서 30개 이상 파일 동시 선택
- **확장자 무관**: .txt, .md, .log, .csv, .json 등 텍스트로 열 수 있으면 모두 지원
- **자동 인코딩 감지**: UTF-8, CP949(한글 Windows), EUC-KR, Latin-1 순서로 시도
- **파일명 헤더**: 각 파일 내용 앞에 구분선과 파일명 표시
- **오류 내성**: 읽기 실패 파일은 건너뛰고 나머지를 합침

## 기술 스택

- Language: Python 3.8+
- GUI: tkinter (표준 라이브러리)
- Test: pytest

## 버전 히스토리

| 버전 | 날짜 | 내용 |
|---|---|---|
| 1.0.0 | 2026-04-28 | 초기 구현 |

## 라이선스

이 프로젝트는 [MIT License](LICENSE) 하에 배포됩니다.
