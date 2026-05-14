# Whisper Transcriber

## Versión correcta de Python en WSL moderno
La versión de Python que viene por defecto en Ubuntu WSL “resolute” es **3.14** (muy nueva). Sin embargo, PyTorch no soporta Python 3.14 aún, lo que hace imposible instalarlo usando `apt` o `pip` sin una versión compatible de Python. 

SOLUCIÓN (la correcta en WSL moderno): No usar `apt` para Python.

## Instalar Python 3.11 con **pyenv** (estándar para ML).

### 1. Instalar dependencias

```bash
sudo apt update
sudo apt install -y build-essential curl git \
libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
libsqlite3-dev libffi-dev liblzma-dev tk-dev
```

---

### 2. Instalar pyenv

```bash
curl https://pyenv.run | bash
```

---

### 3. Activar pyenv

Agrega esto a tu shell:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

---

### 4. Instalar Python 3.11

```bash
pyenv install 3.11.9
```

---

### 5. Usarlo en tu proyecto

```bash
cd ~/proyectos/trabajo/whisper-transcriber
pyenv local 3.11.9
```

Verifica:

```bash
python --version
```

Debe decir:

```
Python 3.11.9
```

## Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Actualizar pip
```bash
pip install --upgrade pip
```

Instalar PyTorch CUDA
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Faster Whisper
```bash
pip install faster-whisper
```

Verificar GPU disponible
```bash
# main.py
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

# output:
True
NVIDIA GeForce RTX 3090
```

## Donde se guarda el modelo
El modelo se guarda en la carpeta `~/.cache/huggingface/hub/` después de la primera ejecución.

## Test
Utilizamos el videos de prueba de [YouTube - De PayPal a SpaceX: la apuesta que lo cambió todo](https://www.youtube.com/watch?v=6ahkjtgL28k&t=297s) para probar el transcriptor.

## Ejecución
```bash
python -m whisper_transcriber.main
```