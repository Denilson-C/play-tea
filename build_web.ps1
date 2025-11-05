# Script de build para Web (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build do PLAY TEA para Web (HTML5)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se pygbag está instalado
try {
    python -c "import pygbag" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "pygbag não encontrado"
    }
} catch {
    Write-Host "pygbag não encontrado. Instalando..." -ForegroundColor Yellow
    pip install pygbag
}

Write-Host "Limpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "build\web") { Remove-Item -Recurse -Force "build\web" }
if (Test-Path "web") { Remove-Item -Recurse -Force "web" }

Write-Host ""
Write-Host "Compilando jogo para Web..." -ForegroundColor Green
pygbag main.py

Write-Host ""
# Verifica se o build foi criado (pode estar em build/web ou web)
$buildDir = $null
if (Test-Path "build\web") {
    $buildDir = "build\web"
} elseif (Test-Path "web") {
    $buildDir = "web"
}

if ($buildDir) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build Web concluído com sucesso!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Arquivos: $buildDir\" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para testar localmente:" -ForegroundColor Yellow
    Write-Host "cd $buildDir" -ForegroundColor White
    Write-Host "python -m http.server 8000" -ForegroundColor White
    Write-Host "Depois acesse: http://localhost:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "Para publicar no itch.io:" -ForegroundColor Yellow
    Write-Host "1. Vá para a pasta $buildDir" -ForegroundColor White
    Write-Host "2. Selecione todos os arquivos" -ForegroundColor White
    Write-Host "3. Compacte em ZIP (PLAYTEA-web.zip)" -ForegroundColor White
    Write-Host "4. No itch.io, faça upload como plataforma 'HTML'" -ForegroundColor White
    Write-Host "5. IMPORTANTE: Marque 'Play in browser'" -ForegroundColor Red
    Write-Host ""
    
    $compactar = Read-Host "Deseja compactar automaticamente? (S/N)"
    if ($compactar -eq "S" -or $compactar -eq "s") {
        Write-Host "Compactando..." -ForegroundColor Yellow
        $zipPath = Join-Path (Get-Location) "PLAYTEA-web.zip"
        Compress-Archive -Path "$buildDir\*" -DestinationPath $zipPath -Force
        if (Test-Path $zipPath) {
            Write-Host "ZIP criado: $zipPath" -ForegroundColor Green
        }
    }
} else {
    Write-Host "ERRO: Build web não foi criado!" -ForegroundColor Red
    Write-Host "Verifique os erros acima." -ForegroundColor Red
    Write-Host ""
    Write-Host "NOTA: pygbag pode ter limitações com Pygame." -ForegroundColor Yellow
    Write-Host "Verifique a documentação do pygbag." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

