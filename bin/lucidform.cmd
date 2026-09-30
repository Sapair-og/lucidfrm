@echo off
setlocal
rem LucidForm launcher.  "lucidform" = fill the form live; "lucidform <cmd> ..." = any CLI command.
set "ROOT=%~dp0.."
set "PY=%ROOT%\.venv\Scripts\python.exe"
set PYTHONIOENCODING=utf-8
chcp 65001 >nul
pushd "%ROOT%"
if not "%~1"=="" (
  "%PY%" -m lucidform.cli %*
  goto :end
)
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"
set "OUT=data\forms\filled_%TS%.pdf"
"%PY%" -m lucidform.cli run --form official --ask-pdf --export "%OUT%"
if exist "%OUT%" (
  echo.
  echo Filled form: %ROOT%\%OUT%
  start "" "%OUT%"
)
:end
popd
endlocal
