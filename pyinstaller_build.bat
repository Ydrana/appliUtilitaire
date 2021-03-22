@echo off

setlocal
:PROMPT
SET /P AREYOUSURE=Incrementer le numero de version (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO PACKAGING

bumpversion --verbose patch

:PACKAGING

pyinstaller --onefile --windowed --icon=./loop.ico main.py --exclude-module numpy --exclude-module=_bz2 --exclude-module=_ctypes --exclude-module=_hashlib --exclude-module=_lzma --name appUtilitaire
pause