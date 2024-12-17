title exeMaker
pyinstaller --onefile main.py
del /f /q main.spec main.exe
copy dist\main.exe main.exe
rd /s /q __pycache__ && rd /s /q build && rd /s /q dist
pause