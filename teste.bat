@echo off
setlocal

:: Caminho do repositório
set REPO=D:\brunofcrosa\2025-CPPIG101-Bruno
set FILE=%REPO%\readme.md

:: Adiciona um espaço no fim do arquivo
echo.>> "%FILE%"

:: Faz o commit
cd /d "%REPO%"
git add .
git commit -m "fix"
git push origin main

echo.
echo Espaço adicionado e commit feito com sucesso!
pause
