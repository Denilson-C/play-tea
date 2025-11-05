# 📱 Guia: Como Gerar APK Android Real

## ⚠️ IMPORTANTE: Diferença entre os "APKs"

### ❌ `build/web/play-tea.apk` (Pygbag)
- **NÃO é um APK Android instalável**
- É apenas um arquivo empacotado para web
- Contém código Python + assets em formato WebAssembly
- **Uso**: Apenas para versão web no navegador
- **Erro comum**: "Erro ao analisar pacote" no Android

### ✅ APK Android Real (Buildozer)
- É um arquivo `.apk` instalável no Android
- Contém código Python compilado com Kivy/Pygame
- **Uso**: Instalar no celular/tablet Android
- **Gerado com**: Buildozer

---

## 🚀 Como Gerar o APK Android Real

### Pré-requisitos

#### **Opção 1: Linux/Ubuntu (Recomendado)**

```bash
# Atualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3 python3-pip git zip unzip \
  openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake \
  libffi-dev libssl-dev

# Instalar Buildozer e Cython
pip3 install --user --upgrade buildozer cython
```

#### **Opção 2: Windows com WSL2**

1. Instale o WSL2:
   ```powershell
   wsl --install
   ```

2. Abra o Ubuntu no WSL2 e siga os passos da "Opção 1"

#### **Opção 3: Docker (Multiplataforma)**

```bash
# Baixar imagem oficial do Buildozer
docker pull kivy/buildozer

# Navegar até a pasta do projeto
cd /caminho/para/play-tea

# Executar compilação dentro do container
docker run -v "$(pwd)":/app -it kivy/buildozer buildozer android debug
```

---

## 📦 Compilar o APK

### Passo 1: Navegue até a pasta do projeto

```bash
cd /home/user/play-tea
```

### Passo 2: Limpar builds anteriores (opcional)

```bash
buildozer android clean
```

### Passo 3: Compilar APK em modo Debug

```bash
buildozer android debug
```

⏱️ **Tempo estimado**:
- **Primeira compilação**: 30-120 minutos (baixa SDK, NDK, Python-for-Android)
- **Compilações seguintes**: 5-15 minutos

💾 **Espaço em disco**: ~5 GB

### Passo 4: Localizar o APK gerado

Após a compilação bem-sucedida:

```bash
ls -lh bin/
```

Você verá algo como:
```
playtea-1.1-arm64-v8a-debug.apk
playtea-1.1-armeabi-v7a-debug.apk
```

---

## 📲 Instalar no Android

### Método 1: Via USB (ADB)

```bash
# Instalar ADB
sudo apt install adb

# Conectar celular via USB
# Ativar "Depuração USB" nas opções de desenvolvedor

# Verificar dispositivo
adb devices

# Instalar APK
adb install bin/playtea-1.1-arm64-v8a-debug.apk
```

### Método 2: Transferência Manual

1. Copie o arquivo `.apk` para o celular (via cabo USB, Bluetooth, ou email)
2. Abra o arquivo no celular
3. Ative "Permitir instalação de fontes desconhecidas" quando solicitado
4. Clique em "Instalar"

---

## 🐛 Resolução de Problemas Comuns

### Erro: "Command failed: git"
```bash
sudo apt install git
```

### Erro: "SDK/NDK não encontrado"
```bash
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

### Erro: "Java não encontrado"
```bash
sudo apt install openjdk-11-jdk
```

### Erro: "Permissão negada"
```bash
chmod +x main.py
```

### APK trava ao abrir
```bash
# Verificar logs do Android
adb logcat | grep python
```

### Compilação muito lenta
- Use Linux nativo ao invés de VM
- Use SSD ao invés de HD
- Aumente RAM disponível (mínimo 4GB)

---

## 🎯 Alternativas Rápidas (Sem Compilar)

Se você **não quer esperar 30-120 minutos** para compilar:

### 1. **Versão Web no Celular** ⚡ (Mais Rápido)

1. Hospede no itch.io (conforme `README_WEB.md`)
2. Acesse o link no navegador do celular
3. Jogue direto (sem instalação)

**Prós:**
- ✅ Funciona imediatamente
- ✅ Não precisa instalar nada
- ✅ Compatível com qualquer celular

**Contras:**
- ⚠️ Requer internet
- ⚠️ Performance pode ser menor

### 2. **PWA (Progressive Web App)** 📱

No navegador do celular:
1. Acesse o jogo no itch.io
2. Menu → "Adicionar à tela inicial"
3. Jogue como se fosse app nativo

---

## 📊 Comparação: Web vs APK

| Característica | Versão Web | APK Android |
|----------------|------------|-------------|
| **Instalação** | Não requer | Requer instalação |
| **Internet** | Necessária | Opcional |
| **Performance** | Média | Excelente |
| **Tempo setup** | Imediato | 30-120 min |
| **Espaço disco** | Nenhum | ~30 MB |
| **Atualização** | Automática | Manual |
| **Compatibilidade** | Todos navegadores | Android 5.0+ |

---

## 🔄 Compilar APK Release (Para Publicar)

### Para Google Play Store:

```bash
# Gerar APK release
buildozer android release

# Criar keystore (primeira vez)
keytool -genkey -v -keystore play-tea.keystore \
  -alias play-tea -keyalg RSA -keysize 2048 -validity 10000

# Assinar APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore play-tea.keystore bin/*.apk play-tea

# Alinhar APK
zipalign -v 4 bin/*-release-unsigned.apk bin/play-tea-release.apk
```

---

## 💡 Recomendação

Para **testes rápidos**: Use a **versão web** (itch.io)

Para **distribuição profissional**: Compile o **APK Android**

Para **melhor dos dois mundos**:
1. Publique versão web no itch.io (imediato)
2. Compile APK em paralelo (background)
3. Adicione APK como download no itch.io quando estiver pronto

---

## 📞 Suporte

Se encontrar erros durante a compilação:

1. Verifique `README_ANDROID.md` para troubleshooting detalhado
2. Consulte logs em `.buildozer/android/platform/build-*/`
3. Procure o erro específico no Google

**Projeto**: PLAY TEA - TG2
**Instituição**: Fatec Barueri
**Versão**: 1.1

---

**Última atualização**: Novembro 2025
