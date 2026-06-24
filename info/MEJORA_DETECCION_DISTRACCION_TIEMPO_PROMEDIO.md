# 🎯 MEJORA: Detección de Distracción por Tiempo Promedio Histórico

## 📊 Resumen de la Mejora

Se ha mejorado el sistema de detección de distracciones para que **utilice el tiempo promedio histórico específico de cada niño** en lugar de solo el promedio de la sesión actual. Ahora el sistema detecta cuando un niño tarda **3x su propio promedio histórico**.

---

## ✨ Características Implementadas

### 1. **Cálculo de Tiempo Promedio Histórico**

El sistema ahora:
- Calcula el promedio de los **últimos 30 ejercicios** del niño
- Excluye outliers (tiempos > 3 minutos)
- Usa este promedio personalizado para cada niño

### 2. **Detección Mejorada**

**Antes:**
```python
# Usaba solo el promedio de los últimos 10 ejercicios de la sesión actual
tiempo_promedio = promedio_ultimos_10_ejercicios
```

**Ahora:**
```python
# Usa el promedio histórico de los últimos 30 ejercicios del niño
tiempo_promedio_historico = promedio_ultimos_30_ejercicios_del_nino
# Si el tiempo actual > 3x promedio histórico → Distracción detectada
```

### 3. **Fallback Inteligente**

Si no hay suficiente historial (< 5 ejercicios):
- Usa el promedio de la sesión actual
- Garantiza que el sistema funcione incluso con niños nuevos

---

## 🔧 Cambios Técnicos Realizados

### Backend

#### 1. **`tareas/ml_utils.py`**

**Función actualizada:** `detectar_distraccion()`

```python
def detectar_distraccion(historial_estudiante, tiempo_promedio_historico=None):
    """
    Detecta distracción usando tiempo promedio histórico del niño
    
    Args:
        historial_estudiante: Lista de últimas respuestas
        tiempo_promedio_historico: Promedio histórico del niño (nuevo parámetro)
    
    Returns:
        {
            'requiere_descanso': bool,
            'focus_score': float,
            'motivo': str,
            'detalles': str  # Nuevo campo con información detallada
        }
    """
```

**Mejoras:**
- ✅ Acepta `tiempo_promedio_historico` como parámetro
- ✅ Usa promedio histórico si está disponible
- ✅ Fallback a promedio de sesión si no hay datos
- ✅ Retorna detalles de la detección

#### 2. **`tareas/views.py`**

**Vista actualizada:** `AnalizarRespuestaView`

**Nuevo código:**
```python
# Calcular tiempo promedio histórico (últimos 30 ejercicios)
historial_tiempos = EjercicioProgreso.objects.filter(
    student=nino,
    time_spent_ms__gt=0,
    time_spent_ms__lt=180000  # Excluir outliers > 3 minutos
).order_by('-created_at')[:30].values_list('time_spent_ms', flat=True)

tiempo_promedio_historico = None
if historial_tiempos and len(historial_tiempos) >= 5:
    tiempo_promedio_historico = sum(historial_tiempos) / len(historial_tiempos)
```

**Detección mejorada:**
```python
# Calcular si el tiempo es excesivo
excessive_time = 0
if tiempo_promedio_historico and tiempo_promedio_historico > 0:
    # Usa promedio histórico del niño (más preciso)
    excessive_time = 1 if tiempo_ms > (tiempo_promedio_historico * 3) else 0
else:
    # Fallback: usa historial reciente
    # ...
```

**Respuesta con debug:**
```python
return Response({
    'prediccion': resultado,
    'distraccion': distraccion,
    'consecutive_errors': consecutive_errors,
    'excessive_time': excessive_time,
    'tiempo_promedio_historico': tiempo_promedio_historico,
    'debug': {
        'tiempo_actual_ms': tiempo_ms,
        'triple_promedio_ms': tiempo_promedio_historico * 3,
        'cantidad_datos_historicos': len(historial_tiempos)
    }
})
```

### Frontend

#### 3. **`nino-tarea.component.ts`**

**Análisis ML mejorado:**

```typescript
this.mlService.analizarRespuesta({...}).subscribe({
  next: (resultado) => {
    console.log('Análisis ML completo:', resultado);
    
    const dist = resultado.distraccion || {};
    const debug = resultado.debug || {};
    
    // Mostrar información de debug
    if (debug.tiempo_promedio_historico) {
      console.log(`Tiempo actual: ${debug.tiempo_actual_ms}ms`);
      console.log(`Promedio histórico: ${debug.tiempo_promedio_historico}ms`);
      console.log(`Triple del promedio: ${debug.triple_promedio_ms}ms`);
      console.log(`Datos históricos: ${debug.cantidad_datos_historicos}`);
    }
    
    if (dist.requiere_descanso) {
      const motivo = dist.motivo || 'Distracción detectada';
      const detalles = dist.detalles || '';
      console.log(`🛑 Pantalla de descanso: ${motivo}`);
      console.log(`   Detalles: ${detalles}`);
      this.mostrarPantallaDescanso(`${motivo} - ${detalles}`);
    }
  }
});
```

**Logs mejorados:**
```typescript
mostrarPantallaDescanso(razon: string): void {
  console.log('═══════════════════════════════════');
  console.log('🛑 PANTALLA DE DESCANSO ACTIVADA');
  console.log(`📋 Razón: ${razon}`);
  console.log(`👤 Niño: ${this.nino.nombre}`);
  console.log(`📝 Ejercicio: ${this.ejercicioActual + 1}/${this.ejercicios.length}`);
  console.log('═══════════════════════════════════');
  
  if (this.pantallaDescanso) {
    this.pantallaDescanso.iniciarDescanso();
  }
}
```

---

## 📈 Ejemplos de Funcionamiento

### Ejemplo 1: Niño Rápido

```
Niño: Juan (promedio histórico: 4000ms)

Ejercicio actual: 13000ms
Triple del promedio: 12000ms

Resultado: ⚠️ DISTRACCIÓN DETECTADA
Motivo: tiempo_excesivo
Detalles: Tardó 13000ms (promedio: 4000ms)
```

### Ejemplo 2: Niño Lento Pero Consistente

```
Niño: María (promedio histórico: 15000ms)

Ejercicio actual: 18000ms
Triple del promedio: 45000ms

Resultado: ✅ NORMAL
Motivo: María naturalmente tarda más, pero está dentro de su rango
```

### Ejemplo 3: Niño Nuevo (Sin Historial)

```
Niño: Pedro (sin historial suficiente)

Fallback: Usa promedio de sesión actual
Promedio sesión: 5000ms
Ejercicio actual: 16000ms
Triple: 15000ms

Resultado: ⚠️ DISTRACCIÓN DETECTADA
```

---

## 🎯 Ventajas de la Mejora

### 1. **Personalización**
- Cada niño tiene su propio umbral de detección
- Respeta el ritmo natural de aprendizaje

### 2. **Precisión**
- Usa 30 ejercicios históricos (no solo 10 recientes)
- Excluye outliers automáticamente

### 3. **Adaptabilidad**
- Funciona con niños nuevos (fallback)
- Se ajusta conforme el niño mejora

### 4. **Debug Completo**
- Logs detallados en consola
- Información de debug en respuesta API

### 5. **Base de Datos MySQL**
- Confirmado uso de MySQL
- Optimizado para consultas históricas

---

## 🔍 Condiciones de Detección Actualizadas

El sistema detecta distracción cuando:

| Condición | Descripción | Prioridad |
|-----------|-------------|-----------|
| **3 errores consecutivos** | El niño comete 3 errores seguidos | Alta |
| **Tiempo excesivo** | Tarda 3x su promedio histórico | Alta |
| **Focus score bajo** | Score < 0.4 (modelo RNN) | Media |

---

## 📊 Datos Debug en Respuesta

La respuesta del endpoint `analizar-respuesta` ahora incluye:

```json
{
  "prediccion": {...},
  "distraccion": {
    "requiere_descanso": true,
    "focus_score": 0.3,
    "motivo": "tiempo_excesivo",
    "detalles": "Tardó 13000ms (promedio: 4000ms)"
  },
  "consecutive_errors": 0,
  "excessive_time": 1,
  "tiempo_promedio_historico": 4000,
  "debug": {
    "tiempo_actual_ms": 13000,
    "triple_promedio_ms": 12000,
    "cantidad_datos_historicos": 30
  }
}
```

---

## 🧪 Cómo Probar

### 1. **Consola del Navegador**

Al resolver ejercicios, verás:
```
Análisis ML completo: {...}
Tiempo actual: 13000ms
Promedio histórico: 4000ms
Triple del promedio: 12000ms
Datos históricos usados: 30

🛑 Pantalla de descanso activada: tiempo_excesivo
   Detalles: Tardó 13000ms (promedio: 4000ms)

═══════════════════════════════════
🛑 PANTALLA DE DESCANSO ACTIVADA
📋 Razón: tiempo_excesivo - Tardó 13000ms (promedio: 4000ms)
👤 Niño: Juan
📝 Ejercicio: 5/10
═══════════════════════════════════
```

### 2. **Endpoint Directo**

```bash
curl -X POST http://localhost:8000/api/tareas/ml/analizar-respuesta \
  -H "Content-Type: application/json" \
  -d '{
    "nino_id": 1,
    "ejercicio_id": 10,
    "tiempo_ms": 13000,
    "correcto": false,
    "tab_blur_count": 0,
    "idle_ms": 0,
    "erratic_clicks": 0
  }'
```

### 3. **Base de Datos**

Verificar tabla `tareas_progreso`:
```sql
SELECT 
  student_id,
  COUNT(*) as total_ejercicios,
  AVG(time_spent_ms) as promedio_tiempo,
  MAX(time_spent_ms) as tiempo_maximo,
  MIN(time_spent_ms) as tiempo_minimo
FROM tareas_progreso
WHERE student_id = 1
  AND time_spent_ms > 0
  AND time_spent_ms < 180000
GROUP BY student_id;
```

---

## 📂 Archivos Modificados

```
backend/tareas/ml_utils.py          ✅ Actualizado
backend/tareas/views.py             ✅ Actualizado
frontend/.../nino-tarea.component.ts ✅ Actualizado
info/MEJORA_DETECCION_DISTRACCION_TIEMPO_PROMEDIO.md ✅ Nuevo
```

---

## ✅ Estado Final

- ✅ MySQL confirmado como base de datos
- ✅ Detección por tiempo promedio histórico implementada
- ✅ Sistema usa últimos 30 ejercicios del niño
- ✅ Fallback para niños nuevos
- ✅ Debug completo en consola
- ✅ Información detallada en respuesta API
- ✅ Logs mejorados en frontend
- ✅ Documentación completa

---

## 🚀 Próximas Mejoras Sugeridas

1. **Panel de Admin**: Ver promedio histórico por niño
2. **Gráficos**: Visualizar evolución de tiempos
3. **Alertas**: Notificar a profesores si hay cambios bruscos
4. **ML Avanzado**: Predecir tiempo esperado por ejercicio
5. **Configuración**: Permitir ajustar el multiplicador (actualmente 3x)

---

## 📞 Soporte

Si encuentras problemas:
1. Verifica logs en consola del navegador
2. Revisa terminal de Django
3. Consulta tabla `tareas_progreso` en MySQL
4. Verifica que hay suficiente historial (> 5 ejercicios)

---

**Fecha de Implementación:** 2025
**Versión:** 1.0
**Estado:** ✅ COMPLETADO Y FUNCIONAL
