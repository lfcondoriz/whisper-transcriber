# Configuración
## `compute_type`
- `compute_type` NO cambia el modelo (base, small, etc.), cambia cómo se ejecuta matemáticamente el modelo. define:
    - 🔢 precisión numérica (float32, float16, int8)
    - ⚡ velocidad de inferencia
    - 🧠 uso de VRAM
    - 🎯 estabilidad/precisión de resultados

📊 Tabla clara para tu RTX 3090 (24GB)
| compute_type   | Precisión     | Velocidad              | VRAM      | Cuándo usarlo                                       |
| -------------- | ------------- | ---------------------- | --------- | --------------------------------------------------- |
| `float32`      | ⭐⭐⭐⭐⭐ máxima  | ❌ lento                | 🔴 alto   | audio crítico (legal, médico, subtítulos oficiales) |
| `float16`      | ⭐⭐⭐⭐ muy alta | ⚡ muy rápido           | 🟡 medio  | uso normal + producción (RECOMENDADO en tu 3090)    |
| `int8_float16` | ⭐⭐⭐ buena     | 🚀 muy rápido          | 🟢 bajo   | batch grande / muchos audios                        |
| `int8`         | ⭐⭐ media      | 🚀 más rápido CPU-like | 🟢 mínimo | cuando importa más velocidad que calidad            |
