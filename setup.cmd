@echo off
rem One-time setup for LucidForm on Windows. Run it from the project folder:
rem     setup.cmd
setlocal
cd /d "%~dp0"

where python >nul 2>nul || (
  echo Python was not found. Install Python 3.11+ from https://www.python.org/downloads/
  echo and tick "Add python.exe to PATH" during installation, then run setup.cmd again.
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating the Python environment in .venv ...
  python -m venv .venv || exit /b 1
)
echo Installing requirements (this takes a few minutes the first time) ...
".venv\Scripts\python.exe" -m pip install -q --upgrade pip
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt || exit /b 1

if not exist ".env" (
  copy /y ".env.example" ".env" >nul
  echo.
  echo Created .env from .env.example.
  echo Paste your Gemini API key after GEMINI_API_KEY= and save the file.
  echo Get a free key at https://aistudio.google.com/apikey
  start "" notepad ".env"
) else (
  echo .env already exists - leaving it as it is.
)

echo.
echo Checking the install with the offline test suite ...
".venv\Scripts\python.exe" -m pytest -q | findstr /r /c:"passed" /c:"failed"

echo.
echo Next steps:
echo   1. Save your key in .env (Notepad should be open).
echo   2. Build the help agent's index once:  .venv\Scripts\python -m lucidform.cli help build
echo   3. Fill a form:                        bin\lucidform
echo      (or add %CD%\bin to your PATH and just type: lucidform)
endlocal
