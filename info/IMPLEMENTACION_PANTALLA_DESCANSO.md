# Implementación Sistema de Pantalla de Descanso

## Cambios Realizados

### 1. Frontend: nino-tarea.component.ts

**Imports Agregados:**
- `ViewChild` desde @angular/core
- `MLService` desde ../../../services/ml.service
- `PantallaDescansoComponent` desde ../../../components/pantalla-descanso.component

**Nuevas Variables:**
```typescript
@ViewChild(PantallaDescansoComponent) pantallaDescanso!: PantallaDescansoComponent;
erroresConsecutivos = 0;
historialRespuestas: any[] = [];
tiempoLimiteTimer: any;
tabBlurCount = 0;
idleMs = 0;
erraticClicks = 0;
lastActivityTime = Date.now();
```

**Funcionalidades Implementadas:**

1. **Detección de cambios de tab/blur:**
   - Event listener en constructor para `window.blur` que incrementa `tabBlurCount`
   - Event listener para `mousemove` que actualiza `lastActivityTime`

2. **Timer de 2 minutos por pregunta:**
   - Método `iniciarTimerTiempoLimite()` que crea setTimeout de 120000ms
   - Se ejecuta automáticamente al cargar tarea y al pasar a siguiente ejercicio
   - Muestra pantalla de descanso si se excede el tiempo

3. **Contador de errores consecutivos:**
   - Se incrementa cuando `correcto=false` y `intentos >= 2`
   - Se resetea a 0 cuando la respuesta es correcta
   - Muestra pantalla de descanso cuando llega a 3

4. **Integración con MLService:**
   - Llama a `mlService.analizarRespuesta()` después de cada respuesta
   - Envía: nino_id, ejercicio_id, tiempo_ms, correcto, tab_blur_count, idle_ms, erratic_clicks
   - Evalúa respuesta: `dist.requiere_descanso` o `dist.focus_score < 0.4`
   - Muestra pantalla de descanso si el modelo ML lo indica

5. **Método mostrarPantallaDescanso():**
   - Recibe razón como parámetro
   - Llama a `pantallaDescanso.iniciarDescanso()` para activar la pantalla

6. **Limpieza al cambiar ejercicio:**
   - Resetea `tabBlurCount = 0`, `erraticClicks = 0`
   - Reinicia timer de tiempo límite

### 2. Frontend: nino-tarea.component.html

**Componente agregado:**
```html
<app-pantalla-descanso></app-pantalla-descanso>
```
- Agregado justo después del div principal
- Se muestra en overlay cuando está activo

### 3. Backend: ml_utils.py (Ya existía, sin cambios)

**Lógica de detección:**
- `detectar_distraccion()` evalúa:
  - **Errores consecutivos >= 3**: `requiere_descanso = True, focus_score = 0.3`
  - **Tiempo excesivo (> 3x promedio)**: `requiere_descanso = True, focus_score = 0.3`
  - **Modelo RNN < 0.4**: `requiere_descanso = True, focus_promedio < 0.4`

### 4. Backend: views.py - AnalizarRespuestaView (Ya existía, sin cambios)

**Respuesta del endpoint:**
```json
{
  "prediccion": {...},
  "distraccion": {
    "requiere_descanso": true/false,
    "focus_score": 0.0-1.0,
    "motivo": "errores_consecutivos" | "tiempo_excesivo" | "bajo_focus"
  },
  "consecutive_errors": 0-N,
  "excessive_time": 0/1
}
```

## Condiciones que Activan Pantalla de Descanso

### 1. **3 Errores Consecutivos**
- Se cuenta solo cuando el niño falla el ejercicio en ambos intentos
- Contador se resetea cuando acierta
- Trigger: `erroresConsecutivos >= 3`

### 2. **Tiempo > 2 Minutos por Pregunta**
- Timer de 120000ms (2 minutos) se inicia al cargar ejercicio
- Se reinicia al pasar al siguiente ejercicio
- Trigger: `setTimeout(() => mostrarPantallaDescanso('Tiempo límite excedido'), 120000)`

### 3. **Modelo ML - Focus Score < 0.4**
- Analiza historial de últimas 5 respuestas
- Modelo RNN calcula focus_score basado en: tab_blur_count, idle_ms, erratic_clicks, time_spent_ms
- Trigger: `dist.focus_score < 0.4`

### 4. **Modelo ML - Errores Consecutivos (Backend)**
- Backend detecta >= 3 errores en últimas 5 respuestas
- Retorna `requiere_descanso = true, motivo = 'errores_consecutivos'`
- Trigger: `dist.requiere_descanso && dist.motivo === 'errores_consecutivos'`

### 5. **Modelo ML - Tiempo Excesivo (Backend)**
- Backend calcula si tiempo > 3x promedio de historial
- Retorna `requiere_descanso = true, motivo = 'tiempo_excesivo'`
- Trigger: `dist.requiere_descanso && dist.motivo === 'tiempo_excesivo'`

## Flujo de Ejecución

```
Usuario responde ejercicio
    ↓
responder() en nino-tarea.component.ts
    ↓
1. Calcular erroresConsecutivos
2. Calcular idleMs (Date.now() - lastActivityTime)
3. Enviar progreso a backend (api.post 'nino/ejercicio-progreso')
4. Llamar MLService.analizarRespuesta()
    ↓
Backend: AnalizarRespuestaView
    ↓
5. Obtener historial reciente (últimas 10 respuestas)
6. Calcular consecutive_errors y excessive_time
7. predict_ffn() para tipo de error
8. detectar_distraccion() para focus_score
    ↓
Respuesta al Frontend
    ↓
9. Evaluar resultado.distraccion.requiere_descanso
10. Si true o focus_score < 0.4 → mostrarPantallaDescanso()
    ↓
11. pantallaDescanso.iniciarDescanso()
    ↓
12. Pantalla se muestra por 10 segundos con animación
13. Después de 10 segundos se oculta automáticamente
```

## Requisitos de Modelos ML

**Archivos necesarios (ya existen):**
- `ml/models/ffn_model.h5` - Modelo de predicción de errores
- `ml/models/rnn_model.h5` - Modelo de detección de distracciones
- `ml/models/scaler.pkl` - Scaler para normalización
- `ml/models/encoder.pkl` - Encoder para tipos de error

**Features requeridas:**
```python
num_features = [
    'difficulty', 'time_spent_ms', 'attempts', 'used_hint', 'n_hints',
    'fast_response', 'correct', 'tab_blur_count', 'idle_ms', 
    'erratic_clicks', 'consecutive_errors', 'excessive_time'
]
```

## Testing

### Probar 3 errores consecutivos:
1. Entrar a una tarea como niño
2. Fallar 3 ejercicios seguidos (ambos intentos)
3. Debe aparecer pantalla de descanso después del 3er error

### Probar tiempo límite de 2 minutos:
1. Entrar a una tarea
2. Esperar 2 minutos sin responder
3. Debe aparecer pantalla de descanso automáticamente

### Probar ML - Focus score bajo:
1. Hacer varias acciones de distracción:
   - Cambiar de tab (incrementa tab_blur_count)
   - No mover el mouse por tiempo prolongado (incrementa idle_ms)
   - Hacer clicks erráticos
2. El modelo RNN calculará focus_score < 0.4
3. Debe aparecer pantalla de descanso

## Logs y Debugging

En consola del navegador:
```
Análisis ML: {
  prediccion: {...},
  distraccion: {
    requiere_descanso: true,
    focus_score: 0.35,
    motivo: "bajo_focus"
  },
  consecutive_errors: 2,
  excessive_time: 0
}
Mostrando pantalla de descanso. Razón: bajo_focus (score: 0.35)
```

## Notas Importantes

1. **AllowAny en endpoints**: Los endpoints ML tienen `permission_classes = [AllowAny]` para permitir acceso sin autenticación
2. **Modelos ML cargados**: Si los modelos no se cargan correctamente, `ML_LOADED = False` y las funciones retornan valores por defecto
3. **Timer cleanup**: El timer se limpia en `ngOnDestroy()` para evitar memory leaks
4. **Standalone component**: PantallaDescansoComponent es standalone y debe importarse en el imports array del componente padre
5. **ViewChild access**: El @ViewChild solo está disponible después de ngAfterViewInit, pero se usa en runtime después de que el componente está cargado
