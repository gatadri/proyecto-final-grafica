# Sistema de Reportes Detallados por Tema

## Descripción

Sistema ML que analiza los errores del niño por **tema específico** (tabla del 11, tabla del 8, división entre 7, suma de fracciones, etc.) y genera reportes detallados para padres y profesores.

## Arquitectura

### 1. Modelos de Base de Datos

#### Ejercicio (Modificado)
```python
tema = models.CharField(max_length=100, blank=True)
# Ejemplos: "tabla_11", "tabla_8", "division_entre_7", "suma_fracciones"

subtema = models.CharField(max_length=100, blank=True)  
# Ejemplos: "multiplicacion", "division", "fracciones", "algebra"
```

#### AnalisisErrorTema (Nuevo)
```python
nino = ForeignKey(Nino)
tarea = ForeignKey(Tarea)
tema = CharField(max_length=100)           # "tabla_11"
subtema = CharField(max_length=100)        # "multiplicacion"
cantidad_errores = IntegerField()          # 5
cantidad_aciertos = IntegerField()         # 2
tiempo_promedio_ms = IntegerField()        # 8500
fecha_analisis = DateTimeField(auto_now=True)
```

### 2. Detección Automática de Temas

Script: `backend/etiquetar_ejercicios.py`

**Patrones detectados:**

| Contenido | Tema | Subtema |
|-----------|------|---------|
| `11 × 8` | `tabla_11` | `multiplicacion` |
| `7 × 9` | `tabla_9` | `multiplicacion` |
| `56 ÷ 7` | `division_entre_7` | `division` |
| `3/4 + 1/4` | `suma_fracciones` | `fracciones` |
| `5/6 - 2/6` | `resta_fracciones` | `fracciones` |

**Función `detectar_tema_subtema(pregunta)`:**
```python
# Detecta tabla específica en multiplicaciones
match = re.search(r'(\d+)\s*×\s*(\d+)', pregunta)
if match:
    numeros = [int(n) for n in match.groups()]
    tabla = max(numeros)  # Usar el número mayor
    return f'tabla_{tabla}', 'multiplicacion'

# Detecta divisor específico en divisiones
match = re.search(r'÷\s*(\d+)', pregunta)
if match:
    divisor = int(match.group(1))
    return f'division_entre_{divisor}', 'division'

# ... más patrones
```

### 3. Análisis en Tiempo Real

**Vista: `AnalizarRespuestaView`**

Cada vez que el niño responde un ejercicio:

```python
# 1. Obtener ejercicio con tema
ejercicio = Ejercicio.objects.get(id=ejercicio_id)

# 2. Crear o actualizar análisis
analisis, created = AnalisisErrorTema.objects.get_or_create(
    nino=nino,
    tarea=ejercicio.tarea,
    tema=ejercicio.tema,
    defaults={
        'subtema': ejercicio.subtema,
        'cantidad_errores': 0 if correcto else 1,
        'cantidad_aciertos': 1 if correcto else 0,
        'tiempo_promedio_ms': tiempo_ms
    }
)

# 3. Si ya existe, actualizar
if not created:
    if correcto:
        analisis.cantidad_aciertos += 1
    else:
        analisis.cantidad_errores += 1
    
    # Calcular nuevo promedio
    total = analisis.cantidad_aciertos + analisis.cantidad_errores
    analisis.tiempo_promedio_ms = (
        (analisis.tiempo_promedio_ms * (total - 1) + tiempo_ms) / total
    )
    analisis.save()
```

### 4. Generación de Reportes

**Vista: `ReporteDetalladoView`**

**Endpoint:** `GET /api/tareas/ml/reporte-detallado?nino_id=X&tarea_id=Y`

**Respuesta:**
```json
{
  "nino": {
    "id": 17,
    "nombre": "Alejandra",
    "apellido": "López",
    "edad": 9,
    "grado": 4
  },
  "padre": {
    "email": "padre@ejemplo.com",
    "nombre": "Juan López"
  },
  "profesor": {
    "email": "profesor@ejemplo.com",
    "nombre": "María García"
  },
  "reporte_por_subtema": [
    {
      "subtema": "multiplicacion",
      "total_errores": 8,
      "total_aciertos": 12,
      "temas_problematicos": [
        {
          "tema": "tabla_11",
          "tema_legible": "Tabla 11",
          "errores": 5,
          "aciertos": 2,
          "porcentaje_error": 71.4,
          "tiempo_promedio_ms": 12500,
          "tarea_id": 11,
          "tarea_titulo": "Multiplicación - Tablas Avanzadas"
        },
        {
          "tema": "tabla_8",
          "tema_legible": "Tabla 8",
          "errores": 3,
          "aciertos": 5,
          "porcentaje_error": 37.5,
          "tiempo_promedio_ms": 8200,
          "tarea_id": 11,
          "tarea_titulo": "Multiplicación - Tablas Avanzadas"
        }
      ]
    },
    {
      "subtema": "division",
      "total_errores": 4,
      "total_aciertos": 8,
      "temas_problematicos": [
        {
          "tema": "division_entre_7",
          "tema_legible": "Division Entre 7",
          "errores": 4,
          "aciertos": 3,
          "porcentaje_error": 57.1,
          "tiempo_promedio_ms": 15000,
          "tarea_id": 12,
          "tarea_titulo": "División - Nivel Intermedio"
        }
      ]
    }
  ],
  "resumen": {
    "total_errores": 12,
    "total_aciertos": 20,
    "subtemas_con_dificultad": 2
  }
}
```

### 5. Componente de Visualización

**Archivo:** `frontend/src/app/components/reporte-detallado.component.ts`

**Características:**
- ✅ Tarjetas con código de colores por gravedad
- ✅ Tabla detallada con temas específicos
- ✅ Barras de progreso de % de error
- ✅ Tiempo promedio formateado
- ✅ Recomendaciones automáticas
- ✅ Botón para enviar por email
- ✅ Botón para imprimir

**Rutas:**
```typescript
// En app.routes.ts agregar:
{
  path: 'reporte-detallado/:ninoId',
  component: ReporteDetalladoComponent
}
```

## Instalación y Configuración

### Paso 1: Ejecutar Setup Automático

```bash
cd backend
python setup_reportes_ml.py
```

Este script:
1. Ejecuta `makemigrations` y `migrate`
2. Etiqueta todos los ejercicios existentes
3. Muestra instrucciones de uso

### Paso 2: Verificar Etiquetado

```bash
cd backend
python etiquetar_ejercicios.py
```

Salida esperada:
```
📝 Encontrados 68 ejercicios para etiquetar
------------------------------------------------------------
✅ #1: 11 × 8 = ?
   → Tema: tabla_11, Subtema: multiplicacion

✅ #2: 56 ÷ 7 = ?
   → Tema: division_entre_7, Subtema: division

...

📊 Resumen por tema:
   multiplicacion - tabla_11: 12 ejercicios
   multiplicacion - tabla_8: 10 ejercicios
   division - division_entre_7: 8 ejercicios
   fracciones - suma_fracciones: 15 ejercicios
```

### Paso 3: Agregar Ruta en Angular

**app.routes.ts:**
```typescript
import { ReporteDetalladoComponent } from './components/reporte-detallado.component';

export const routes: Routes = [
  // ... rutas existentes
  {
    path: 'reporte-detallado/:ninoId',
    component: ReporteDetalladoComponent
  }
];
```

## Uso

### Para Profesores

1. **Ver reporte de un estudiante:**
   ```
   http://localhost:4200/reporte-detallado/17
   ```

2. **Desde panel de profesor:**
   - Lista de estudiantes → Click en "Ver Reporte"
   - Dashboard → Sección "Estudiantes con Dificultades"

### Para Padres

1. **Acceder desde portal de padres:**
   ```
   http://localhost:4200/padre/reportes
   ```

2. **Recibir por email:**
   - Automático: cada semana
   - Manual: botón "Enviar Reporte" desde la vista

### Para el Sistema

**Análisis automático:**
- Cada respuesta del niño se analiza y almacena
- No requiere intervención manual
- Actualización en tiempo real

## API Endpoints

### 1. Analizar Respuesta (Automático)
```
POST /api/tareas/ml/analizar-respuesta
Body: {
  "nino_id": 17,
  "ejercicio_id": 123,
  "tiempo_ms": 8500,
  "correcto": false,
  "tab_blur_count": 2,
  "idle_ms": 1500,
  "erratic_clicks": 3
}
```

### 2. Obtener Reporte Detallado
```
GET /api/tareas/ml/reporte-detallado?nino_id=17
GET /api/tareas/ml/reporte-detallado?nino_id=17&tarea_id=11
```

### 3. Enviar Reporte por Email
```
POST /api/tareas/ml/notificar
Body: {
  "nino_id": 17
}
```

### 4. Estadísticas Generales
```
GET /api/tareas/ml/estadisticas?nino_id=17
```

## Ejemplos de Reportes

### Ejemplo 1: Problema con Tabla del 11

```
Subtema: Multiplicación
Total: 8 errores / 12 aciertos

Temas Problemáticos:
┌────────────┬─────────┬──────────┬──────────┬─────────────┐
│ Tema       │ Errores │ Aciertos │ % Error  │ Tiempo Prom │
├────────────┼─────────┼──────────┼──────────┼─────────────┤
│ Tabla 11   │    5    │    2     │  71.4%   │   12.5s     │
│ Tabla 8    │    3    │    5     │  37.5%   │    8.2s     │
└────────────┴─────────┴──────────┴──────────┴─────────────┘

Recomendación:
Reforzar multiplicación: especialmente Tabla 11 y Tabla 8.
```

### Ejemplo 2: Dificultad con Fracciones

```
Subtema: Fracciones
Total: 12 errores / 8 aciertos

Temas Problemáticos:
┌──────────────────────┬─────────┬──────────┬──────────┐
│ Tema                 │ Errores │ Aciertos │ % Error  │
├──────────────────────┼─────────┼──────────┼──────────┤
│ Suma Fracciones      │    8    │    3     │  72.7%   │
│ Resta Fracciones     │    4    │    5     │  44.4%   │
└──────────────────────┴─────────┴──────────┴──────────┘

Recomendación:
Reforzar fracciones: especialmente Suma Fracciones.
```

## Testing

### 1. Crear datos de prueba

```python
# Desde Django shell
python manage.py shell

from tareas.models import Ejercicio, Tarea, Nino
from tareas.views import AnalizarRespuestaView

nino = Nino.objects.get(id=17)
ejercicio = Ejercicio.objects.filter(tema='tabla_11').first()

# Simular errores en tabla del 11
for i in range(5):
    # POST a analizar-respuesta con correcto=False
    pass
```

### 2. Verificar reporte

```bash
curl "http://localhost:8000/api/tareas/ml/reporte-detallado?nino_id=17"
```

### 3. Verificar en UI

```
http://localhost:4200/reporte-detallado/17
```

## Personalización

### Agregar Nuevos Patrones de Detección

**En `etiquetar_ejercicios.py`:**

```python
def detectar_tema_subtema(pregunta):
    # Detectar ecuaciones lineales
    if 'x' in pregunta and '=' in pregunta:
        if re.search(r'(\d+)x\s*\+\s*(\d+)', pregunta):
            return 'ecuaciones_lineales_simples', 'algebra'
        return 'ecuaciones_generales', 'algebra'
    
    # Detectar geometría
    if 'área' in pregunta.lower():
        if 'triángulo' in pregunta.lower():
            return 'area_triangulos', 'geometria'
        elif 'círculo' in pregunta.lower():
            return 'area_circulos', 'geometria'
    
    # ... más patrones
```

### Personalizar Colores de Alertas

**En `reporte-detallado.component.ts`:**

```typescript
// Cambiar umbrales de color
[class.bg-danger]="subtema.total_errores >= 5"      // Rojo: 5+ errores
[class.bg-warning]="subtema.total_errores >= 3"     // Amarillo: 3-4 errores
[class.bg-info]="subtema.total_errores < 3"         // Azul: <3 errores
```

## Notas Importantes

1. **Tema vs Subtema:**
   - `tema`: Específico ("tabla_11", "division_entre_7")
   - `subtema`: Categoría general ("multiplicacion", "division")

2. **Umbral de Reportes:**
   - Solo temas con >= 2 errores aparecen en reportes
   - Evita ruido de errores puntuales

3. **Tiempo Promedio:**
   - Calculado como media ponderada
   - Actualizado en cada respuesta

4. **Compatibilidad:**
   - Ejercicios sin `tema` funcionan normalmente
   - No rompe funcionalidad existente
   - Se puede etiquetar gradualmente

## Troubleshooting

### Problema: Ejercicios sin tema

```bash
# Re-ejecutar etiquetado
python backend/etiquetar_ejercicios.py
```

### Problema: Reporte vacío

- Verificar que el niño haya completado tareas
- Verificar que ejercicios tengan campo `tema`
- Revisar logs de backend para errores

### Problema: Email no se envía

- Configurar SMTP en `settings.py`
- Verificar que padre/profesor tengan email válido
