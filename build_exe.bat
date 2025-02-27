@echo off
pip install pyinstaller pyfiglet ttkthemes
pyinstaller --onefile --windowed --name "ASCII Art Studio" ^
--add-data "%LOCALAPPDATA%\Programs\Python\Python312\Lib\site-packages\pyfiglet\fonts;pyfiglet\fonts" ^
--add-data "ascii_favorites.txt;." ^
--add-data "icon.png;." ^
--hidden-import=pyfiglet ^
--hidden-import=ttkthemes ^
--icon="icon.ico" ^
ascii_art_generator.py
pause