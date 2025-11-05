@echo off
echo ========================================
echo Build do PLAY TEA para Windows (itch.io)
echo ========================================
echo.

REM Verifica se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
)

echo Limpando builds anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo.
echo Compilando jogo...
pyinstaller main.spec

echo.
if exist dist\PLAYTEA.exe (
    echo ========================================
    echo Build concluido com sucesso!
    echo ========================================
    echo Executavel: dist\PLAYTEA.exe
    echo.
    echo Para publicar no itch.io:
    echo 1. Copie o arquivo PLAYTEA.exe para uma pasta
    echo 2. Faca upload dessa pasta no itch.io
    echo.
) else (
    echo ERRO: Executavel nao foi criado!
    echo Verifique os erros acima.
)

pause

