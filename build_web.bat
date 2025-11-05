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
REM Verifica se o build foi criado (pode estar em build/web ou web)
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
echo.
echo NOTA: pygbag pode ter limitacoes com Pygame.
echo Verifique a documentacao do pygbag.
goto :end

:success
echo ========================================
echo Build Web concluido com sucesso!
echo ========================================
echo Arquivos: %BUILD_DIR%\
echo.
echo Para testar localmente:
echo cd %BUILD_DIR%
echo python -m http.server 8000
echo Depois acesse: http://localhost:8000
echo.
echo Para publicar no itch.io:
echo 1. Vá para a pasta %BUILD_DIR%
echo 2. Selecione todos os arquivos
echo 3. Compacte em ZIP (PLAYTEA-web.zip)
echo 4. No itch.io, faça upload como plataforma "HTML"
echo 5. IMPORTANTE: Marque "Play in browser"
echo.
echo.
echo Deseja compactar automaticamente? (S/N)
set /p COMPACTAR=
if /i "%COMPACTAR%"=="S" (
    echo Compactando...
    cd %BUILD_DIR%
    REM Tenta usar PowerShell primeiro, se falhar usa python
    powershell -Command "Compress-Archive -Path * -DestinationPath ..\PLAYTEA-web.zip -Force" 2>nul
    if errorlevel 1 (
        echo PowerShell falhou, tentando com Python...
        python -c "import shutil, os, sys; shutil.make_archive('..\PLAYTEA-web', 'zip', '.')"
    )
    cd ..
    if exist PLAYTEA-web.zip (
        echo ZIP criado: PLAYTEA-web.zip
        echo.
        echo Pronto para fazer upload no itch.io!
    ) else (
        echo AVISO: Nao foi possivel criar o ZIP automaticamente.
        echo Por favor, compacte manualmente a pasta %BUILD_DIR%
    )
)

:end
pause

