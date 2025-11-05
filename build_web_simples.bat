@echo off
echo ========================================
echo Build do PLAY TEA para Web (HTML5)
echo ========================================
echo.

REM Verifica se pygbag está instalado
python -c "import pygbag" 2>nul
if errorlevel 1 (
    echo pygbag nao encontrado. Instalando...
    pip install pygbag
)

echo Limpando builds anteriores...
if exist build\web rmdir /s /q build\web
if exist web rmdir /s /q web

echo.
echo Compilando jogo para Web...
pygbag main.py

echo.
REM Verifica se o build foi criado
if exist build\web (
    set BUILD_DIR=build\web
    goto :success
)
if exist web (
    set BUILD_DIR=web
    goto :success
)

echo ERRO: Build web nao foi criado!
echo Verifique os erros acima.
goto :end

:success
echo ========================================
echo Build Web concluido com sucesso!
echo ========================================
echo.
echo Arquivos: %BUILD_DIR%\
echo.
echo Para testar localmente:
echo   cd %BUILD_DIR%
echo   python -m http.server 8000
echo   Depois acesse: http://localhost:8000
echo.
echo Para publicar no itch.io:
echo   1. Vá para a pasta %BUILD_DIR%
echo   2. Selecione todos os arquivos
echo   3. Clique com botão direito -> Enviar para -> Pasta compactada (ZIP)
echo   4. Renomeie o ZIP para PLAYTEA-web.zip
echo   5. No itch.io, faça upload como plataforma "HTML"
echo   6. IMPORTANTE: Marque "Play in browser"
echo.

:end
pause

