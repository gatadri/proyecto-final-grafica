# 🧠 SISTEMA DE DATASET MASIVO Y ENTRENAMIENTO ML

## 📋 OPCIONES DE DATASET DISPONIBLES

Ahora tienes 3 opciones para generar datasets de diferentes tamaños:

### 1️⃣ Dataset Original (50 registros)
- **Archivo**: `tdah_tutor_dataset.csv` (actual)
- **Tamaño**: ~50 registros
- **Uso**: Pruebas rápidas

### 2️⃣ Dataset Masivo (15,000 registros) ⭐ RECOMENDADO
- **Script**: `generar_dataset_masivo.py`
- **Configuración**: 500 estudiantes × 30 ejercicios
- **Tamaño**: ~15,000 registros
- **Tiempo de generación**: ~30 segundos
- **Tiempo de entrenamiento**: ~5-10 minutos

### 3️⃣ Mega Dataset (50,000+ registros) 🚀 MÁXIMO
- **Script**: `generar_dataset_mega.py`
- **Configuración**: 1,000 estudiantes × 50 ejercicios
- **Tamaño**: ~50,000 registros
- **Tiempo de generación**: ~2-3 minutos
- **Tiempo de entrenamiento**: ~15-30 minutos

## 🚀 INICIO RÁPIDO

### Opción A: Dataset Masivo (RECOMENDADO)

```bash
cd ml
python generar_dataset_masivo.py
python train.py
```

### Opción B: Mega Dataset (Máxima precisión)

```bash
cd ml
python generar_dataset_mega.py
python train.py
```

### Opción C: Pipeline Automático

```bash
cd ml
python entrenar_todo.py
```

Este script ejecuta todo automáticamente:
- ✅ Genera el dataset
- ✅ Entrena ambos modelos (FFN y RNN)
- ✅ Valida que todo funcione
- ✅ Muestra métricas de rendimiento

## 📊 CARACTERÍSTICAS DEL DATASET GENERADO

### Datos Realistas Incluyen:

✅ **12 características por ejercicio:**
- Dificultad (1-4)
- Tiempo de respuesta
- Intentos
- Uso de pistas
- Respuesta rápida
- Correcto/Incorrecto
- Conteo de desenfoque de pestañas
- Tiempo inactivo
- Clics erráticos
- **Errores consecutivos** (NUEVO)
- **Tiempo excesivo** (NUEVO)

✅ **Perfiles de estudiantes variados:**
- Excelentes (15%)
- Buenos (30%)
- Promedio (35%)
- Con dificultad (15%)
- TDAH (5%)

✅ **Patrones realistas:**
- Fatiga durante sesiones
- Variación por día de la semana
- Progresión de dificultad
- Racha de errores
- Sesiones de estudio

✅ **5 tipos de errores:**
- Procedimiento (25%)
- Inatención (30%)
- Conceptual (25%)
- Consigna (15%)
- Aleatorio (5%)

## 🧠 MEJORAS EN EL ENTRENAMIENTO

### Modelo FFN (Feed-Forward Network)
**Antes:**
- 2 capas (64 → 32 neuronas)
- 10 epochs
- Sin validación

**Ahora:**
- 3 capas (128 → 64 → 32 neuronas)
- BatchNormalization
- Dropout mejorado (0.3, 0.2)
- Early stopping
- 50 epochs con validación
- Métricas de precisión

### Modelo RNN (Recurrent Neural Network)
**Antes:**
- 1 capa LSTM (32 unidades)
- Secuencias de 3
- 10 epochs

**Ahora:**
- 2 capas Bidirectional LSTM (64, 32 unidades)
- Secuencias de 5 (mejor contexto)
- Dropout entre capas
- Early stopping
- 50 epochs con validación
- Métricas MSE y MAE

## 📈 RESULTADOS ESPERADOS

### Con Dataset Original (50 registros):
- Precisión FFN: ~60-70%
- MAE RNN: ~0.15-0.20

### Con Dataset Masivo (15,000 registros):
- Precisión FFN: ~85-92%
- MAE RNN: ~0.08-0.12

### Con Mega Dataset (50,000 registros):
- Precisión FFN: ~92-96%
- MAE RNN: ~0.05-0.08

## 🔧 PERSONALIZACIÓN

### Cambiar Tamaño del Dataset Masivo

Edita `generar_dataset_masivo.py`:

```python
NUM_STUDENTS = 500  # Cambia este número
EXERCISES_PER_STUDENT = 30  # Y este
```

### Cambiar Tamaño del Mega Dataset

Edita `generar_dataset_mega.py`:

```python
NUM_STUDENTS = 1000  # Cambia este número
EXERCISES_PER_STUDENT = 50  # Y este
```

### Ajustar Hiperparámetros del Modelo

Edita `train.py`:

```python
# Arquitectura FFN
layers.Dense(128, ...)  # Número de neuronas
layers.Dropout(0.3)     # Tasa de dropout

# Entrenamiento
epochs=50               # Épocas
batch_size=32           # Tamaño de batch
```

## 📁 ARCHIVOS GENERADOS

Después del entrenamiento, tendrás:

```
ml/
├── models/
│   ├── ffn_model.h5      # Modelo Feed-Forward
│   ├── rnn_model.h5      # Modelo Recurrent
│   ├── scaler.pkl        # Escalador de datos
│   └── encoder.pkl       # Codificador de errores
├── tdah_tutor_dataset.csv  # Dataset (generado)
└── [scripts de generación y entrenamiento]
```

## ⚡ COMANDOS RÁPIDOS

```bash
# Generar dataset masivo
python generar_dataset_masivo.py

# Generar mega dataset
python generar_dataset_mega.py

# Solo entrenar (usa dataset existente)
python train.py

# Pipeline completo automático
python entrenar_todo.py

# Actualizar dataset existente (añade nuevas columnas)
python actualizar_dataset.py
```

## 📊 MONITOREO DEL ENTRENAMIENTO

Durante el entrenamiento verás:

```
Epoch 1/50
████████████████ 375/375 - 2s - loss: 1.2456 - accuracy: 0.7234
Epoch 2/50
████████████████ 375/375 - 2s - loss: 0.9823 - accuracy: 0.7891
...
```

Métricas finales:
```
✅ Modelo FFN entrenado
   - Precisión tipo de error: 92.5%
   - Precisión próximo error: 88.3%

✅ Modelo RNN entrenado
   - MSE: 0.0234
   - MAE: 0.0867
```

## 🎯 RECOMENDACIONES

### Para Desarrollo/Pruebas:
→ Usa **Dataset Masivo** (15,000 registros)
- Balance perfecto entre velocidad y precisión
- Entrenamiento en 5-10 minutos

### Para Producción:
→ Usa **Mega Dataset** (50,000 registros)
- Máxima precisión y robustez
- Mejor generalización
- Modelos más confiables

### Para Pruebas Rápidas:
→ Mantén el dataset original
- Solo para verificar que el código funciona
- No recomendado para uso real

## 🐛 TROUBLESHOOTING

### Error: "Memory Error"
- Reduce `NUM_STUDENTS` o `EXERCISES_PER_STUDENT`
- Cierra otras aplicaciones
- Usa dataset masivo en lugar de mega

### El entrenamiento es muy lento
- Reduce `epochs` en train.py
- Aumenta `batch_size`
- Usa GPU si está disponible

### Precisión muy baja
- Genera un dataset más grande
- Verifica que las columnas `consecutive_errors` y `excessive_time` existen
- Ejecuta `python actualizar_dataset.py` si usas un dataset antiguo

## 📞 SOPORTE

Si tienes problemas:
1. Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
2. Asegúrate de estar en la carpeta `ml/`
3. Revisa que Python sea 3.7+
4. Verifica que TensorFlow esté instalado correctamente

## 🎉 SIGUIENTE PASO

Después de entrenar:

```bash
cd ../backend
python manage.py runserver
```

¡El sistema de detección de distracción está listo! 🚀
