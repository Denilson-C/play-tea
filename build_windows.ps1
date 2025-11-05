# Script de build para Windows (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build do PLAY TEA para Windows (itch.io)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se PyInstaller está instalado
try {
    python -c "import PyInstaller" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller não encontrado"
    }
} catch {
    Write-Host "PyInstaller não encontrado. Instalando..." -ForegroundColor Yellow
    pip install pyinstaller
}

Write-Host "Limpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

Write-Host ""
Write-Host "Compilando jogo..." -ForegroundColor Green
pyinstaller main.spec

Write-Host ""
if (Test-Path "dist\PLAYTEA.exe") {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build concluído com sucesso!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executável: dist\PLAYTEA.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para publicar no itch.io:" -ForegroundColor Yellow
    Write-Host "1. Copie o arquivo PLAYTEA.exe para uma pasta" -ForegroundColor White
    Write-Host "2. Faça upload dessa pasta no itch.io" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "ERRO: Executável não foi criado!" -ForegroundColor Red
    Write-Host "Verifique os erros acima." -ForegroundColor Red
}

Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

