# 🔍 GUÍA VISUAL: DÓNDE VER EL ML EN ACCIÓN

Esta guía te muestra exactamente dónde puedes ver y verificar que las redes neuronales están funcionando en tu aplicación.

---

## 📱 1. PANTALLA DE DESCANSO (RNN en acción)

### ¿Dónde verla?
**Ruta**: Durante la resolución de ejercicios por el niño

### Cómo activarla:
1. Iniciar sesión como niño (PIN de 4 dígitos)
2. Seleccionar cualquier tarea
3. **Opción A**: Cometer 3 errores consecutivos
4. **Opción B**: Tardar mucho tiempo (>2 minutos en un ejercicio)
5. La pantalla aparecerá automáticamente

### Qué verás:
```
╔════════════════════════════════════════╗
║                                        ║
║              😌                        ║
║                                        ║
║      ¡Hora de un descanso!            ║
║                                        ║
║   Relájate por unos segundos...       ║
║                                        ║
║          ╭─────────╮                  ║
║          │    10   │  ← Cuenta regresiva
║          ╰─────────╯                  ║
║                                        ║
║   ¡Respira profundo! 🌟               ║
║                                        ║
╚════════════════════════════════════════╝
```

### Evidencia de ML:
- En la consola del navegador (F12) verás:
  ```javascript
  Análisis ML: {
    prediccion: {...},
    distraccion: {
      requiere_descanso: true,
      focus_score: 0.3,
      motivo: "bajo_focus"
    }
  }
  ```

### Archivo de código:
- **Frontend**: `frontend/src/app/components/pantalla-descanso.component.ts`
- **Activación**: `frontend/src/app/modules/nino/tarea/nino-tarea.component.ts` (línea ~140-150)
- **Backend**: `backend/tareas/ml_utils.py` → función `detectar_distraccion()`

---

## 📊 2. REPORTE DE APRENDIZAJE (FFN + Análisis)

### ¿Dónde verlo?
**Ruta**: `/padre/reportes`

### Cómo acceder:
1. Iniciar sesión como padre
   - Email: `jose@correo.com`
   - Password: `password`
2. Hacer clic en menú lateral: **"Reportes"**
3. Verás tarjetas de tus hijos
4. Clic en **"Ver Detalle"** de cualquier hijo

### Qué verás:

#### Vista General:
```
╔══════════════════════════════════════════════════╗
║  REPORTES DE PROGRESO                            ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  ┌─────────────────────────────────┐            ║
║  │  👦 Hijo 1                      │            ║
║  │  Nivel 3 • 450 monedas          │            ║
║  │  5 tareas completadas           │            ║
║  │  [Ver Detalle]  [Ver Grupal]    │            ║
║  └─────────────────────────────────┘            ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

#### Vista de Detalle (con ML):
```
╔══════════════════════════════════════════════════╗
║  ANÁLISIS DETALLADO - Hijo 1                     ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  📈 TEMAS CON DIFICULTAD                        ║
║  ┌────────────────────────────────────────────┐ ║
║  │ Multiplicación                             │ ║
║  │ • Tabla del 7: 5 errores (60% error)      │ ║
║  │ • Tabla del 8: 3 errores (50% error)      │ ║
║  │ Tiempo promedio: 8.5s                      │ ║
║  └────────────────────────────────────────────┘ ║
║                                                  ║
║  ┌────────────────────────────────────────────┐ ║
║  │ Fracciones                                 │ ║
║  │ • Suma de fracciones: 4 errores (70%)     │ ║
║  │ • División de fracciones: 2 errores (40%) │ ║
║  │ Tiempo promedio: 12.3s                     │ ║
║  └────────────────────────────────────────────┘ ║
║                                                  ║
║  💡 RECOMENDACIONES                             ║
║  • Reforzar Multiplicación: especialmente      ║
║    tablas del 7 y 8. Practiquen juntos.       ║
║  • Reforzar Fracciones: especialmente suma     ║
║    de fracciones. Practiquen juntos.           ║
║                                                  ║
║  [📄 Descargar PDF]                             ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

### Evidencia de ML:
- **Temas con dificultad**: Identificados por análisis de patrones de error
- **Porcentajes**: Calculados por el sistema ML
- **Recomendaciones**: Generadas automáticamente basadas en ML
- Los datos vienen de la tabla `AnalisisErrorTema` que se actualiza con cada respuesta

### Archivos de código:
- **Frontend**: `frontend/src/app/modules/padre/reportes/reportes-padre.component.ts`
- **Backend**: `backend/tareas/views.py` → clase `ReporteDetalladoView`
- **Tabla BD**: `backend/tareas/models.py` → clase `AnalisisErrorTema`

---

## 🔍 3. VERIFICAR EN LA BASE DE DATOS

### Tablas que almacenan datos de ML:

#### Tabla: `tareas_prediccionerror`
```sql
SELECT * FROM tareas_prediccionerror ORDER BY fecha_prediccion DESC LIMIT 5;
```
**Contiene**:
- `nino_id`: ID del estudiante
- `tipo_error`: Predicción del modelo FFN (fracciones, multiplicacion, etc.)
- `probabilidad`: Confianza de la predicción (0.0 - 1.0)
- `fecha_prediccion`: Cuándo se hizo la predicción
- `notificado`: Si ya se notificó al padre/profesor

#### Tabla: `tareas_eventodistraccion`
```sql
SELECT * FROM tareas_eventodistraccion ORDER BY fecha_evento DESC LIMIT 5;
```
**Contiene**:
- `nino_id`: ID del estudiante
- `focus_score`: Predicción del modelo RNN (0.0 - 1.0)
- `tab_blur_count`: Veces que cambió de pestaña
- `idle_ms`: Tiempo inactivo
- `fecha_evento`: Cuándo se detectó
- `descanso_mostrado`: Si se mostró la pantalla

#### Tabla: `tareas_analisiserrortema`
```sql
SELECT * FROM tareas_analisiserrortema WHERE nino_id = 1;
```
**Contiene**:
- `nino_id`: ID del estudiante
- `tarea_id`: ID de la tarea
- `tema`: Tema específico (tabla_7, suma_fracciones, etc.)
- `subtema`: Categoría general (multiplicacion, fracciones)
- `cantidad_errores`: Total de errores en ese tema
- `cantidad_aciertos`: Total de aciertos
- `tiempo_promedio_ms`: Tiempo promedio

---

## 🖥️ 4. VERIFICAR EN LOS LOGS DEL BACKEND

### Al iniciar el servidor Django:
Abre la terminal donde corre Django y busca:

```bash
python manage.py runserver
```

Verás mensajes como:
```
System check identified no issues (0 silenced).
December 2024
Django version X.X.X, using settings 'backend_django.settings'
Starting development server at http://127.0.0.1:8000/
```

### Al cargar los modelos ML:
Si revisas los logs o la consola cuando se carga `ml_utils.py`:
```python
# Los modelos se cargan al importar
model_ffn = tf.keras.models.load_model("ml/models/ffn_model.h5")
model_rnn = tf.keras.models.load_model("ml/models/rnn_model.h5")
```

### Al analizar una respuesta:
En la consola del backend verás (si hay prints de debug):
```
Análisis ML:
- Tipo de error predicho: multiplicacion
- Probabilidad de error siguiente: 0.67
- Focus score: 0.35
- Requiere descanso: True
```

---

## 🌐 5. VERIFICAR EN LA CONSOLA DEL NAVEGADOR

### Durante los ejercicios:
1. Abre el navegador (Chrome/Edge)
2. Presiona `F12` para abrir DevTools
3. Ve a la pestaña **"Console"**
4. Resuelve ejercicios como niño

Verás mensajes como:
```javascript
Análisis ML: {
  prediccion: {
    error_type: "multiplicacion",
    prob_mistake_next: 0.6543
  },
  distraccion: {
    requiere_descanso: false,
    focus_score: 0.78,
    motivo: null
  },
  consecutive_errors: 1,
  excessive_time: 0
}
```

### En los reportes:
```javascript
Reporte ML cargado: {
  nino: {...},
  reporte_por_subtema: [
    {
      subtema: "multiplicacion",
      total_errores: 8,
      temas_problematicos: [...]
    }
  ],
  resumen: {
    total_errores: 15,
    subtemas_con_dificultad: 2
  }
}
```

---

## 🔧 6. VERIFICAR CON EL SCRIPT DE VERIFICACIÓN

### Ejecutar:
```bash
cd c:\laragon\www\proyecto_adri_angular
python verificar_sistema_ml.py
```

### Salida esperada:
```
============================================================
VERIFICACIÓN DEL SISTEMA DE MACHINE LEARNING
============================================================

============================================================
1. VERIFICANDO ESTRUCTURA DE CARPETAS
============================================================
[OK] Carpeta ml/ existe: c:\laragon\www\proyecto_adri_angular\ml
[OK] Carpeta ml/models/ existe: ...

============================================================
2. VERIFICANDO MODELOS ENTRENADOS
============================================================
[OK] Modelo FFN existe: ffn_model.h5
[OK] Modelo RNN existe: rnn_model.h5
[OK] Scaler existe: scaler.pkl
[OK] Encoder existe: encoder.pkl

... (más verificaciones) ...

============================================================
RESUMEN DE VERIFICACIÓN
============================================================

Verificaciones exitosas: 35/35 (100.0%)

[SUCCESS] SISTEMA DE ML COMPLETAMENTE FUNCIONAL
Todas las verificaciones principales pasaron correctamente.
```

---

## 📸 7. EVIDENCIA FOTOGRÁFICA (Simulada)

### Pantalla de Descanso:
```
┌─────────────────────────────────────────────┐
│                                             │
│              😌                             │
│                                             │
│         ¡Hora de un descanso!               │
│                                             │
│      Relájate por unos segundos...          │
│                                             │
│              ╱────────╲                     │
│             │    10   │  ← Círculo animado  │
│              ╲────────╱                     │
│                                             │
│      ¡Respira profundo! 🌟                  │
│                                             │
└─────────────────────────────────────────────┘
   Gradiente: #FFD4A3 → #B3E0FF
   Animaciones: fadeIn, slideUp, pulse
```

### Reporte de Padre:
```
┌─────────────────────────────────────────────┐
│  📊 ANÁLISIS DE APRENDIZAJE                 │
├─────────────────────────────────────────────┤
│                                             │
│  Estudiante: Juan Pérez                     │
│  Edad: 8 años • Grado: 3                    │
│                                             │
│  ═══════════════════════════════════        │
│                                             │
│  📈 Multiplicación (8 errores)              │
│  ┌──────────────────────────────────┐       │
│  │ • Tabla del 7: ████░░░░  60%    │       │
│  │ • Tabla del 8: ███░░░░░  50%    │       │
│  └──────────────────────────────────┘       │
│                                             │
│  📈 Fracciones (6 errores)                  │
│  ┌──────────────────────────────────┐       │
│  │ • Suma: █████░░░░  70%          │       │
│  │ • División: ██░░░░░░  40%       │       │
│  └──────────────────────────────────┘       │
│                                             │
│  💡 Recomendaciones:                        │
│  • Reforzar multiplicación (tablas 7 y 8)   │
│  • Practicar suma de fracciones             │
│                                             │
│  [📄 Descargar PDF]                         │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎓 RESUMEN DE ACCESOS RÁPIDOS

### Para probar la Pantalla de Descanso:
```
1. URL: http://localhost:4200/nino/dashboard
2. Login: PIN del niño (ejemplo: 1234)
3. Clic en cualquier tarea
4. Cometer 3 errores seguidos
5. Ver pantalla de descanso aparecer
```

### Para ver Reportes ML:
```
1. URL: http://localhost:4200/padre/dashboard
2. Login: jose@correo.com / password
3. Menú: "Reportes"
4. Clic: "Ver Detalle" en cualquier hijo
5. Ver análisis por temas y recomendaciones
```

### Para verificar Base de Datos:
```bash
cd c:\laragon\www\proyecto_adri_angular\backend
python manage.py dbshell

sqlite> SELECT COUNT(*) FROM tareas_prediccionerror;
sqlite> SELECT COUNT(*) FROM tareas_eventodistraccion;
sqlite> SELECT COUNT(*) FROM tareas_analisiserrortema;
```

### Para verificar archivos de modelos:
```bash
cd c:\laragon\www\proyecto_adri_angular\ml\models
dir

# Deberías ver:
# ffn_model.h5
# rnn_model.h5
# encoder.pkl
# scaler.pkl
```

---

## ✅ CHECKLIST DE VERIFICACIÓN RÁPIDA

- [ ] Modelos entrenados existen en `ml/models/`
- [ ] Backend Django está corriendo
- [ ] Frontend Angular está corriendo
- [ ] Login como niño funciona
- [ ] Pantalla de descanso aparece tras 3 errores
- [ ] Login como padre funciona
- [ ] Reportes muestran análisis por temas
- [ ] Se puede descargar PDF del reporte
- [ ] Consola muestra datos de ML (F12)
- [ ] Base de datos contiene registros en tablas ML

---

**¿TODO FUNCIONANDO?** ✅
Si todos los puntos arriba están verificados, tu sistema de ML está 100% operativo.

**DOCUMENTACIÓN RELACIONADA**:
- `CONFIRMACION_ML_FUNCIONAL.md` - Resumen ejecutivo
- `ANALISIS_FUNCIONAMIENTO_ML.md` - Análisis técnico detallado
- `verificar_sistema_ml.py` - Script de verificación automática
