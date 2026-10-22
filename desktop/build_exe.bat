@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   PyQuest - gerando o executavel (.exe)
echo ============================================
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado.
    echo Instale o Python em https://www.python.org/downloads/
    echo e marque a opcao "Add Python to PATH" na instalacao.
    pause
    exit /b 1
)
echo Instalando PyInstaller...
python -m pip install --upgrade pyinstaller
echo.
echo Gerando PyQuest.exe (pode levar 1-2 minutos)...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name PyQuest --hidden-import this pyquest.py
echo.
if exist "dist\PyQuest.exe" (
    copy /Y "dist\PyQuest.exe" "PyQuest.exe" >nul
    echo PRONTO! O arquivo PyQuest.exe esta nesta pasta.
) else (
    echo Algo deu errado. Veja as mensagens acima.
)
pause
