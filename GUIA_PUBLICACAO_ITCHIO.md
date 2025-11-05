# Guia de Publicação - PLAY TEA no itch.io

Este guia explica como preparar e publicar o jogo PLAY TEA na plataforma itch.io.

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **PyInstaller** para criar executáveis
3. **Conta no itch.io** (crie em https://itch.io)

## 🛠️ Preparação do Build

### Opção 1: Build para Windows (.exe)

#### Windows (PowerShell):
```powershell
.\build_windows.ps1
```

#### Windows (CMD):
```cmd
build_windows.bat
```

#### Manual:
```bash
pip install pyinstaller
pyinstaller main.spec
```

O executável será criado em `dist/PLAYTEA.exe`

### Opção 2: Build para Web (HTML5)

#### Instalação do pygbag:
```bash
pip install pygbag
```

#### Build Web:
```bash
pygbag main.py
```

Isso criará uma pasta `build/web/` com os arquivos HTML5.

**Nota:** O pygbag pode ter limitações com Pygame. Se houver problemas, considere usar apenas builds executáveis.

## 📦 Estrutura de Arquivos para itch.io

### Para Windows:
```
PLAYTEA/
├── PLAYTEA.exe
└── (todos os assets já estão incluídos no .exe)
```

### Para Web:
```
PLAYTEA-web/
├── index.html
├── main.py
├── assets/
├── data/
└── src/
```

## 🚀 Publicando no itch.io

### 1. Criar uma Nova Página de Jogo

1. Acesse https://itch.io/dashboard
2. Clique em **"Create new project"**
3. Preencha:
   - **Project title:** PLAY TEA
   - **Project URL:** (será gerado automaticamente)
   - **Classification:** Game
   - **Genre:** Educational
   - **Tags:** educacional, terapia, crianças, dislexia

### 2. Configurar a Página

#### Descrição:
```
PLAY TEA é um jogo educacional desenvolvido para auxiliar no processo terapêutico de crianças, com foco em acessibilidade e inclusão.

Características:
- Fonte OpenDyslexic para melhorar a leitura
- Personalização de cores e sons
- Múltiplas fases de aprendizado
- Interface acessível e intuitiva
```

#### Capturas de Tela:
- Adicione 3-5 imagens do jogo
- Primeira imagem deve ser a mais atrativa (tela inicial ou gameplay)
- Use formato PNG ou JPG

#### Informações Adicionais:
- **Versão:** 1.1
- **Plataformas:** Windows, Web (HTML5)
- **Linguagem:** Português (Brasil)
- **Preço:** Gratuito ou valor sugerido

### 3. Upload dos Arquivos

#### Para Windows:
1. Vá em **"Upload files"**
2. Selecione **"Windows"** como plataforma
3. Faça upload do arquivo `PLAYTEA.exe` de `dist/`
4. Ou compacte em ZIP e faça upload (recomendado)

#### Para Web:
1. Vá em **"Upload files"**
2. Selecione **"HTML"** como plataforma
3. Faça upload de todos os arquivos da pasta `build/web/`
4. Ou compacte em ZIP e faça upload

### 4. Configurações de Distribuição

#### Opções Recomendadas:
- ✅ **"This game will be distributed for free"** (se for gratuito)
- ✅ **"Allow downloads"**
- ✅ **"Allow comments"**
- ✅ **"Allow ratings"**

#### Classificação:
- Selecione a classificação etária apropriada (provavelmente "Everyone")

### 5. Preview e Publicação

1. Clique em **"Save"** para salvar as alterações
2. Use **"Preview"** para ver como ficará a página
3. Quando estiver satisfeito, clique em **"Save & view page"**
4. Para publicar, clique em **"Edit"** → **"Status"** → **"Public"**

## 📝 Checklist de Publicação

- [ ] Build do executável criado sem erros
- [ ] Testado o executável localmente
- [ ] Capturas de tela prontas
- [ ] Descrição completa escrita
- [ ] Tags e categorias definidas
- [ ] Arquivos enviados para todas as plataformas desejadas
- [ ] Página revisada e sem erros
- [ ] Status definido como "Public"

## 🐛 Solução de Problemas

### Erro: "PyInstaller não encontrado"
```bash
pip install pyinstaller
```

### Erro: "Assets não encontrados"
- Verifique se os arquivos em `main.spec` estão corretos
- Certifique-se de que `assets/`, `data/` e `src/` existem

### Executável não abre
- Teste localmente antes de publicar
- Verifique se todas as dependências estão incluídas
- Considere criar um build com console habilitado para debug:
  - No `main.spec`, mude `console=False` para `console=True`

### Problemas com Web Build
- O pygbag pode ter limitações com Pygame
- Considere usar apenas builds executáveis
- Ou use outras ferramentas como Pygame Web (pygame-web)

## 📚 Recursos Adicionais

- [Documentação do itch.io](https://itch.io/docs)
- [Guia de PyInstaller](https://pyinstaller.org/)
- [Documentação do pygbag](https://pypi.org/project/pygbag/)

## 💡 Dicas

1. **Teste antes de publicar:** Sempre teste o executável em um computador limpo antes de fazer upload
2. **Versione:** Mantenha um controle de versão (ex: v1.1, v1.2)
3. **Atualize:** Use a seção "Changelog" no itch.io para documentar atualizações
4. **Comunidade:** Responda comentários e feedback dos usuários
5. **Marketing:** Compartilhe nas redes sociais e comunidades

## 📞 Suporte

Se encontrar problemas durante a publicação, verifique:
- Logs do PyInstaller em `build/`
- Documentação do itch.io
- Fóruns da comunidade

---

**Boa sorte com a publicação! 🎮**

