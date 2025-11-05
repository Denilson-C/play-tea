# Guia de Publicação - PLAY TEA no itch.io (Web/HTML5)

Este guia explica como preparar e publicar o jogo PLAY TEA na plataforma itch.io como jogo web (HTML5).

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **pygbag** para compilar Pygame para Web
3. **Conta no itch.io** (crie em https://itch.io)

## 🛠️ Instalação do pygbag

```bash
pip install pygbag
```

**Importante:** O pygbag pode ter algumas limitações com Pygame. Se encontrar problemas, verifique a seção de "Solução de Problemas" abaixo.

## 📦 Preparação do Build Web

### Opção 1: Usando o script automático

**Windows (CMD):**
```cmd
build_web.bat
```

**Windows (PowerShell):**
```powershell
.\build_web.bat
```

### Opção 2: Manual

```bash
# Limpar builds anteriores (opcional)
rmdir /s /q build\web

# Compilar para web
pygbag main.py
```

O build será criado em `build/web/` ou `web/`

## 📁 Estrutura de Arquivos Gerada

Após o build, você terá uma estrutura similar a:

```
build/web/
├── index.html
├── main.py
├── assets/
│   ├── audio/
│   ├── fonts/
│   └── images/
├── data/
├── src/
└── (outros arquivos necessários)
```

## ✅ Teste Local

Antes de publicar, teste localmente:

```bash
cd build/web
python -m http.server 8000
```

Depois acesse no navegador: `http://localhost:8000`

**Teste:**
- ✅ Jogo carrega corretamente
- ✅ Imagens aparecem
- ✅ Sons funcionam
- ✅ Fontes carregam
- ✅ Controles funcionam (mouse)
- ✅ Todas as fases funcionam

## 🚀 Publicando no itch.io

### 1. Criar uma Nova Página de Jogo

1. Acesse https://itch.io/dashboard
2. Clique em **"Create new project"**
3. Preencha:
   - **Project title:** PLAY TEA
   - **Project URL:** (será gerado automaticamente)
   - **Classification:** Game
   - **Genre:** Educational
   - **Tags:** educacional, terapia, crianças, dislexia, web

### 2. Configurar a Página

#### Descrição:
```
PLAY TEA é um jogo educacional desenvolvido para auxiliar no processo terapêutico de crianças, com foco em acessibilidade e inclusão.

Características:
- Fonte OpenDyslexic para melhorar a leitura
- Personalização de cores e sons
- Múltiplas fases de aprendizado
- Interface acessível e intuitiva
- Jogável diretamente no navegador!
```

#### Capturas de Tela:
- Adicione 3-5 imagens do jogo
- Primeira imagem deve ser a mais atrativa
- Use formato PNG ou JPG

#### Informações Adicionais:
- **Versão:** 1.1
- **Plataformas:** Web (HTML5)
- **Linguagem:** Português (Brasil)
- **Preço:** Gratuito ou valor sugerido

### 3. Upload dos Arquivos

#### Método 1: Upload de Pasta (Recomendado)

1. **Compacte a pasta `build/web/` em ZIP:**
   - Selecione todos os arquivos dentro de `build/web/`
   - Clique com botão direito → "Enviar para" → "Pasta compactada (em zip)"
   - Renomeie para `PLAYTEA-web.zip`

2. **No itch.io:**
   - Vá em **"Upload files"**
   - Selecione **"HTML"** como plataforma
   - Faça upload do arquivo `PLAYTEA-web.zip`
   - **IMPORTANTE:** Marque a opção **"This file will be played in the browser"**

#### Método 2: Upload Individual

1. Vá em **"Upload files"**
2. Selecione **"HTML"** como plataforma
3. Faça upload de todos os arquivos da pasta `build/web/`
4. **IMPORTANTE:** O arquivo `index.html` deve ser o principal

### 4. Configurações Importantes

#### Opções de Upload:
- ✅ **"This file will be played in the browser"** (CRÍTICO!)
- ✅ **"Allow downloads"** (opcional)
- ✅ **"Allow comments"**
- ✅ **"Allow ratings"**

#### URL Principal:
- O itch.io deve usar o `index.html` como ponto de entrada
- Se necessário, ajuste nas configurações do projeto

### 5. Configurações de Distribuição

#### Opções Recomendadas:
- ✅ **"This game will be distributed for free"** (se for gratuito)
- ✅ **"Allow comments"**
- ✅ **"Allow ratings"**

#### Classificação:
- Selecione a classificação etária apropriada (provavelmente "Everyone")

### 6. Preview e Publicação

1. Clique em **"Save"** para salvar as alterações
2. Use **"Preview"** para testar o jogo diretamente no itch.io
3. Quando estiver satisfeito, clique em **"Save & view page"**
4. Para publicar, clique em **"Edit"** → **"Status"** → **"Public"**

## 📝 Checklist de Publicação Web

- [ ] pygbag instalado e funcionando
- [ ] Build web criado sem erros
- [ ] Testado localmente (http://localhost:8000)
- [ ] Todos os assets carregam corretamente
- [ ] Sons funcionam no navegador
- [ ] Fontes carregam corretamente
- [ ] Controles (mouse) funcionam
- [ ] Todas as fases testadas
- [ ] Capturas de tela prontas
- [ ] Descrição completa escrita
- [ ] Tags e categorias definidas
- [ ] Arquivos ZIP compactados
- [ ] Upload feito como "HTML"
- [ ] "Play in browser" marcado
- [ ] Preview testado no itch.io
- [ ] Status definido como "Public"

## 🐛 Solução de Problemas

### Erro: "pygbag não encontrado"
```bash
pip install pygbag
```

### Erro: "Module not found" durante o build
- Verifique se todas as dependências estão no `requirements.txt`
- pygbag pode precisar de configurações adicionais

### Assets não carregam no navegador
- Verifique se os caminhos estão corretos
- Assets devem estar na mesma estrutura de pastas
- Verifique o console do navegador (F12) para erros

### Sons não funcionam
- Alguns navegadores bloqueiam áudio automático
- O usuário pode precisar clicar na tela primeiro
- Verifique se os formatos são suportados (OGG é geralmente bom)

### Fontes não carregam
- Verifique se todos os arquivos de fonte estão incluídos
- Alguns navegadores podem ter limitações com fontes personalizadas

### Jogo não carrega no itch.io
- Certifique-se de que "Play in browser" está marcado
- Verifique se o `index.html` está na raiz do ZIP
- Teste o arquivo ZIP localmente antes de fazer upload

### Performance lenta
- Otimize imagens (use compressão)
- Reduza tamanho de arquivos de áudio
- Considere usar spritesheets

## 🔧 Otimizações para Web

### 1. Compressão de Assets
- Comprima imagens PNG/JPG
- Use formatos OGG para áudio (já está usando!)
- Minimize tamanho de arquivos JSON

### 2. Configurações do pygbag
Você pode criar um arquivo `pygbag.toml` na raiz do projeto:

```toml
[metadata]
name = "PLAYTEA"
version = "1.1"
author = "Seu Nome"

[build]
main = "main.py"
```

### 3. Teste em Múltiplos Navegadores
- Chrome/Edge (Chromium)
- Firefox
- Safari (se possível)

## 📚 Recursos Adicionais

- [Documentação do itch.io](https://itch.io/docs)
- [Documentação do pygbag](https://pypi.org/project/pygbag/)
- [Pygame Web](https://pygame-web.github.io/)

## 💡 Dicas

1. **Teste extensivamente:** Teste em diferentes navegadores e dispositivos
2. **Otimize assets:** Menor tamanho = carregamento mais rápido
3. **Feedback:** Adicione uma mensagem de carregamento se necessário
4. **Mobile:** Considere se o jogo funciona em dispositivos móveis
5. **Analytics:** O itch.io fornece estatísticas de jogos

## ⚠️ Limitações Conhecidas

- Pygame para web pode ter algumas limitações
- Algumas funcionalidades podem não funcionar exatamente como no desktop
- Performance pode variar entre navegadores
- Áudio pode precisar de interação do usuário primeiro

## 📞 Suporte

Se encontrar problemas:
1. Verifique o console do navegador (F12)
2. Teste localmente primeiro
3. Verifique a documentação do pygbag
4. Consulte fóruns da comunidade

---

**Boa sorte com a publicação! 🎮**

