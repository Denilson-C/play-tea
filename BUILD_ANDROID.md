# Guia de Compilação Android - PLAY TEA

Este documento explica como compilar o jogo PLAY TEA para Android (APK).

## Método 1: GitHub Actions (Recomendado) ⭐

O método mais fácil é usar o GitHub Actions que compila automaticamente o APK na nuvem.

### Como usar:

1. **Faça push do código para o GitHub**:
   ```bash
   git push origin claude/transforma-011CUoyJvEAWLZ8N43tmaQcr
   ```

2. **Aguarde a compilação**:
   - Acesse: https://github.com/Denilson-C/play-tea/actions
   - O workflow "Build Android APK" será executado automaticamente
   - Aguarde ~10-20 minutos para a compilação completar

3. **Baixe o APK**:
   - Após a compilação concluir, clique no workflow
   - Em "Artifacts", clique em "play-tea-apk" para baixar
   - Descompacte o arquivo ZIP e você terá o APK

### Quando o APK é compilado automaticamente:

- Sempre que você fizer push para `master`, `main` ou branches `claude/**`
- Quando criar um Pull Request
- Manualmente através da aba Actions (botão "Run workflow")

---

## Método 2: Compilação Local

Se preferir compilar localmente na sua máquina:

### Requisitos:

- Linux (Ubuntu 20.04+ ou similar)
- Python 3.8+
- 8GB RAM mínimo
- 20GB espaço em disco

### Passos:

1. **Instalar dependências do sistema**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y \
     build-essential git python3-pip \
     python3-dev python3-setuptools python3-sh \
     openjdk-17-jdk autoconf libtool pkg-config \
     zlib1g-dev libncurses5-dev libncursesw5-dev \
     libtinfo5 cmake libffi-dev libssl-dev zip unzip
   ```

2. **Configurar JAVA_HOME**:
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
   ```

3. **Instalar Buildozer**:
   ```bash
   pip3 install --upgrade buildozer cython
   ```

4. **Compilar o APK**:
   ```bash
   buildozer android debug
   ```

5. **Localizar o APK**:
   O APK estará em: `bin/playtea-1.1-arm64-v8a-debug.apk`

### Tempo de compilação:

- **Primeira vez**: 20-40 minutos (baixa SDK, NDK, compila dependências)
- **Compilações subsequentes**: 5-10 minutos (usa cache)

---

## Método 3: Buildozer em Docker

Para um ambiente isolado:

```bash
docker run --rm -v "$(pwd)":/app kivy/buildozer android debug
```

---

## Instalando o APK no Android

### Via USB:

1. Ative "Depuração USB" no Android (Configurações > Desenvolvedor)
2. Conecte o dispositivo ao PC
3. Execute:
   ```bash
   adb install -r bin/playtea-1.1-arm64-v8a-debug.apk
   ```

### Via Arquivo:

1. Transfira o APK para o dispositivo
2. Abra o arquivo APK no dispositivo
3. Permita "Instalar de fontes desconhecidas" se solicitado
4. Toque em "Instalar"

---

## Troubleshooting

### Erro: "sh" não pode ser instalado

**Solução**: Instale via apt primeiro:
```bash
sudo apt-get install python3-sh
```

### Erro: JAVA_HOME não configurado

**Solução**:
```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# Ou encontre o caminho correto:
sudo update-alternatives --config java
```

### Erro: Sem espaço em disco

**Solução**: Buildozer precisa ~15GB. Limpe espaço ou use:
```bash
buildozer android clean
```

### Compilação travada/lenta

**Solução**: Use mais cores da CPU:
```bash
# No buildozer.spec, adicione:
# android.num_cores = 4
```

---

## Especificações do APK

- **Nome**: PLAY TEA
- **Package**: org.fatecbarueri.playtea
- **Versão**: 1.1
- **Arquitetura**: arm64-v8a (64-bit)
- **API mínima**: Android 5.0 (API 21)
- **API alvo**: Android 12 (API 31)
- **Permissões**:
  - INTERNET
  - READ_EXTERNAL_STORAGE
  - WRITE_EXTERNAL_STORAGE

---

## Próximos Passos

### Para versão de produção (Release):

1. Gere uma chave de assinatura:
   ```bash
   keytool -genkey -v -keystore playtea.keystore \
     -alias playtea -keyalg RSA -keysize 2048 -validity 10000
   ```

2. Configure no `buildozer.spec`:
   ```ini
   android.keystore = /path/to/playtea.keystore
   android.keystore_key = playtea
   ```

3. Compile versão release:
   ```bash
   buildozer android release
   ```

### Para publicar na Google Play:

1. Crie uma conta de desenvolvedor
2. Configure a listagem do app
3. Faça upload do APK assinado
4. Preencha os requisitos de conteúdo
5. Envie para revisão

---

## Links Úteis

- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Python-for-Android](https://python-for-android.readthedocs.io/)
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Android Developer Guide](https://developer.android.com/guide)

---

## Suporte

Para problemas específicos:

1. Verifique os logs em `.buildozer/android/platform/build-*/`
2. Consulte o README_ANDROID.md para detalhes técnicos
3. Abra uma issue no repositório do GitHub
