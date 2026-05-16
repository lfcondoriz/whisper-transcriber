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
Default:
```bash
python -m whisper_transcriber.main
```

Con opciones:
```bash
python -m whisper_transcriber.main --model base --language es --task translate --device cuda --input data/input --output data/output
```
Donde:
- `--model`: el modelo de Whisper a usar (tiny, base, small, medium, large)
- `--device`: el dispositivo a usar (cpu o cuda)
- `--input`: la carpeta de entrada con los archivos de audio/video a transcribir
- `--output`: la carpeta de salida donde se guardarán las transcripciones
- `--language`: el código del idioma (por ejemplo, 'es', 'en'). Usa None para auto-detección
- `--task`: el modo de tarea: transcribe (mismo idioma) o translate (a inglés) (Whisper NO tiene traducción multi-idioma real SOLO en inglés.)

# 🧠 Modelos Whisper (actualizado 2026)
| Modelo         | Parámetros | Idioma                   | VRAM aprox | Velocidad relativa | Estado                                  |
| -------------- | ---------- | ------------------------ | ---------- | ------------------ | --------------------------------------- |
| tiny           | 39M        | Multilingual / tiny.en   | ~1 GB      | ~10×               | activo                                  |
| base           | 74M        | Multilingual / base.en   | ~1 GB      | ~7×                | activo                                  |
| small          | 244M       | Multilingual / small.en  | ~2 GB      | ~4×                | activo                                  |
| medium         | 769M       | Multilingual / medium.en | ~5 GB      | ~2×                | activo                                  |
| large-v2       | 1.55B      | Multilingual             | ~10 GB     | 1×                 | legado                                  |
| large-v3       | 1.55B      | Multilingual             | ~10 GB     | 1×                 | **actual estándar de máxima precisión** |
| large-v3-turbo | 0.81B      | Multilingual             | ~6 GB      | ~6–8×              | **recomendado general (equilibrio)**    |

# ⚔️ Whisper vs faster-whisper (2026)
| Característica           | OpenAI Whisper                             | faster-whisper                                                 |
| ------------------------ | ------------------------------------------ | -------------------------------------------------------------- |
| Motor                    | PyTorch (implementación original)          | CTranslate2 optimizado                                         |
| Precisión                | Igual (depende del modelo: large-v3, etc.) | Igual (mismos pesos del modelo)                                |
| Velocidad                | 1× (baseline)                              | 4× a 8× más rápido ([LocalAlternative][1])                     |
| Uso de VRAM              | Alto (FP16 típico)                         | 30–60% menos VRAM (INT8/FP16 optimizado) ([LLMHardware.io][2]) |
| CPU                      | Más lento                                  | Mucho más eficiente (INT8 + SIMD)                              |
| GPU                      | Necesario para grande/fluido               | Mejor aprovechado (CUDA optimizado)                            |
| Modelos soportados       | tiny → large-v3                            | tiny → large-v3 / large-v3-turbo                               |
| Streaming / tiempo real  | Limitado                                   | Mejor soporte (batch + streaming)                              |
| Producción               | Menos usado                                | **Estándar en producción**                                     |
| Compatibilidad           | Oficial OpenAI                             | Wrapper compatible (mismos modelos)                            |
| Diarización (speaker ID) | No nativo                                  | No nativo (pero se integra mejor con pipelines tipo WhisperX)  |

[1]: https://www.localalternative.io/compare/whisper-vs-faster-whisper?utm_source=chatgpt.com "Whisper vs Faster-Whisper: Best Local Transcription? (2026) | LocalAlternative"
[2]: https://llmhardware.io/guides/whisper-local-hardware-guide?utm_source=chatgpt.com "Whisper Local Hardware Requirements: GPU, CPU, Apple Silicon (2026) | LLMHardware.io"
