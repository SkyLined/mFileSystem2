@ECHO OFF
WHERE PYTHON 2>&1 >nul
IF ERRORLEVEL 1 (
  ECHO - PYTHON was not found!
  EXIT /B 1
)

CALL PYTHON "%~dp0\%~n0\%~n0.py" %*
EXIT /B %ERRORLEVEL%
