@echo off
setlocal enabledelayedexpansion

:: Force uv to use the custom venv directory name
set VENV_DIR=.win_venv
set UV_PROJECT_ENVIRONMENT=%VENV_DIR%
set PYTHON_EXE=%VENV_DIR%\Scripts\python.exe

if "%1" == "" goto help
if "%1" == "help" goto help
if "%1" == "setup" goto setup
if "%1" == "sync-libs" goto sync-libs
if "%1" == "build" goto build
if "%1" == "render" goto render
if "%1" == "test" goto test
if "%1" == "lint" goto lint
if "%1" == "clean" goto clean

echo Unknown command: %1
goto help

:help
echo Usage: make.bat [command]
echo Commands:
echo   setup      - Create and initialize %VENV_DIR%
echo   sync-libs  - Copy libs from venv to PythonSCAD (Requires Admin)
echo   build      - Generate STL model
echo   render     - Generate PNG image
echo   test       - Run pytest
echo   lint       - Run ruff linter and formatter check
echo   clean      - Remove build artifacts
goto :eof

:setup
echo Creating virtual environment in %VENV_DIR%...
if not exist %VENV_DIR% uv venv %VENV_DIR%
uv sync --all-groups --python %VENV_DIR%
uv pip install -e . --python %PYTHON_EXE%
goto :eof

:sync-libs
echo Syncing libraries to PythonSCAD...
set SRC=%VENV_DIR%\Lib\site-packages
set DST=C:\Program Files\PythonSCAD\libraries\python
if not exist "%SRC%" (
    echo Error: Source directory "%SRC%" not found. Run "make.bat setup" first.
    goto :eof
)
robocopy "%SRC%" "%DST%" /E /R:3 /W:5 /NJH /NJS
if %ERRORLEVEL% GEQ 8 (
    echo.
    echo [ERROR] Robocopy failed (code %ERRORLEVEL%). 
    echo Please ensure you are running this command as Administrator.
) else (
    echo.
    echo Libraries synced successfully.
)
goto :eof

:build
if not exist build mkdir build
uv run --python %PYTHON_EXE% pythonscad src/main.py --trust-python -o build/keyboard.stl
uv run --python %PYTHON_EXE% pythonscad src/main.py --trust-python -o build/keyboard.3mf
goto :eof

:render
if not exist build mkdir build
uv run --python %PYTHON_EXE% pythonscad src/main.py --trust-python --colorscheme "Tomorrow Night" --imgsize 2048,2048 --render -o build/keyboard.png
goto :eof

:test
uv run --python %PYTHON_EXE% pytest
goto :eof

:lint
uv run --python %PYTHON_EXE% ruff check .
uv run --python %PYTHON_EXE% ruff format --check .
goto :eof

:clean
if exist build rmdir /s /q build
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
goto :eof
