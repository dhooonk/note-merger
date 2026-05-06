@echo off
REM ========================================
REM Note Merger - EXE 빌드 스크립트 (PyInstaller)
REM ========================================

echo ========================================
echo Note Merger EXE 빌드 시작
echo ========================================
echo.

REM 1. 이전 빌드 파일 정리
echo [1/5] 이전 빌드 파일 정리 중...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo 완료!
echo.

REM 2. Python 버전 확인
echo [2/5] Python 버전 확인 중...
python --version
if errorlevel 1 (
    echo 오류: Python이 설치되어 있지 않습니다!
    echo Python 3.8 이상을 설치하세요.
    pause
    exit /b 1
)
echo.

REM 3. PyInstaller 확인
echo [3/5] PyInstaller 확인 중...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller가 설치되어 있지 않습니다. 설치 중...
    pip install pyinstaller
    if errorlevel 1 (
        echo 오류: PyInstaller 설치 실패!
        pause
        exit /b 1
    )
)
echo PyInstaller 확인 완료!
echo.

REM 4. EXE 빌드 실행
echo [4/5] EXE 파일 빌드 중...
pyinstaller --clean --noconfirm note-merger.spec
if errorlevel 1 (
    echo.
    echo 오류: 빌드 실패!
    pause
    exit /b 1
)
echo.

REM 5. 빌드 결과 확인
echo [5/5] 빌드 결과 확인 중...
if exist dist\NoteMerger.exe (
    echo.
    echo ========================================
    echo 빌드 성공!
    echo ========================================
    echo 생성된 파일: dist\NoteMerger.exe
    echo.
) else (
    echo.
    echo 오류: EXE 파일이 생성되지 않았습니다!
    pause
    exit /b 1
)

pause
