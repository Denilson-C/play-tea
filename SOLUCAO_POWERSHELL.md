# Solução para Problema de Execução do PowerShell

Se você está recebendo o erro:
```
Não é possível carregar o arquivo porque a execução de scripts foi desabilitada neste sistema
```

## Soluções Rápidas

### Opção 1: Usar o arquivo .bat (RECOMENDADO)
Simplesmente use o arquivo `.bat` que não tem essa restrição:

```cmd
build_web.bat
```

Ou o arquivo simplificado:
```cmd
build_web_simples.bat
```

### Opção 2: Executar os Comandos Manualmente

Se preferir executar manualmente:

```bash
# 1. Instalar pygbag
pip install pygbag

# 2. Limpar builds anteriores (opcional)
rmdir /s /q build\web
rmdir /s /q web

# 3. Compilar para web
pygbag main.py

# 4. Testar localmente
cd build\web
python -m http.server 8000
```

Depois acesse: http://localhost:8000

### Opção 3: Habilitar Execução de Scripts no PowerShell

Se você realmente precisa usar o `.ps1`, pode habilitar temporariamente:

1. **Abrir PowerShell como Administrador:**
   - Clique com botão direito no PowerShell
   - Selecione "Executar como administrador"

2. **Executar este comando:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **Confirmar:** Digite `S` quando perguntado

4. **Agora você pode executar:**
```powershell
.\build_web.ps1
```

**Nota:** Isso permite que você execute scripts locais. Ainda é seguro, pois scripts da internet ainda precisam ser assinados.

### Opção 4: Habilitar Apenas para Este Script

Se não quiser mudar a política globalmente:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_web.ps1
```

## Recomendação

**Use o arquivo `.bat`** - é mais simples e não requer mudanças de política de segurança.

---

**Boa sorte com o build! 🎮**

