@echo off

setlocal
:PROMPT
SET /P AREYOUSURE=Incrementer le numero de version (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO PACKAGING

bumpversion --verbose patch

:PACKAGING

pyinstaller --onefile --windowed --icon=./loop.ico main.py --exclude-module numpy
pause