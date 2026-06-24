# 🎯 Guía de Prueba - Detección de Distracción por Tiempo

## ¿Qué se implementó?

La detección de distracción ahora funciona de la siguiente manera:

1. **Promedio Histórico Personalizado**: El sistema calcula el tiempo promedio de respuesta de cada niño basado en sus últimos 30 ejercicios
2. **Detección Triple**: Si el niño tarda **3 veces o más** de su promedio, se activa la pantalla de descanso
3. **Fallback Inteligente**: Si no hay suficiente historial (menos de 5 ejercicios), usa el promedio de la sesión actual

## 🚀 Prueba Rápida (3 pasos)

### 1. Ejecutar script de verificación

```bash
cd backend
python test_deteccion_tiempo.py
```

**Resultado esperado:**
```
🧪 PRUEBA DE DETECCIÓN DE DISTRACCIÓN POR TIEMPO
👤 Niño: Juan Pérez (ID: 1)
📊 Ejercicios analizados: 30
⏱️  Tiempo promedio: 4500ms (4.5s)
⚠️  Umbral 3x: 13500ms (13.5s)

🔬 SIMULACIONES:
1️⃣  Tiempo normal (4500ms):
   Requiere descanso: False

3️⃣  Tiempo 3.5x promedio (15750ms):
   ✅ Requiere descanso: True
   📋 Motivo: tiempo_excesivo
   📝 Detalles: Tardó 15750ms (promedio: 4500ms)
```

### 2. Probar en la Interfaz

#### A. Iniciar servicios
```bash
# Terminal 1: Backend
cd backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend
ng serve
```

#### B. Probar con un niño
1. Abre `http://localhost:4200`
2. Haz login como niño (usa el PIN)
3. **IMPORTANTE**: Abre la consola del navegador (F12)
4. Entra a una tarea y completa ejercicios

#### C. Ver los logs en consola
Deberías ver algo como:

```
═══════════════════════════════════
📊 ANÁLISIS ML COMPLETADO
⏱️  Tiempo actual: 5000ms
📈 Promedio histórico: 4200ms
⚠️  Triple del promedio: 12600ms
📚 Datos históricos: 28 ejercicios
✅ Normal (margen de 7600ms)
✅ Todo normal - sin distracción detectada
═══════════════════════════════════
```

#### D. Forzar detección (tardar mucho a propósito)
1. Espera **deliberadamente** más de lo normal antes de responder
2. La consola mostrará:

```
═══════════════════════════════════
📊 ANÁLISIS ML COMPLETADO
⏱️  Tiempo actual: 18000ms
📈 Promedio histórico: 4200ms
⚠️  Triple del promedio: 12600ms
📚 Datos históricos: 28 ejercicios
🛑 TIEMPO EXCESIVO (excedió por 5400ms)
═══════════════════════════════════
🛑 PANTALLA DE DESCANSO ACTIVADA
📋 Razón: tiempo_excesivo
   Detalles: Tardó 18000ms (promedio: 4200ms)
═══════════════════════════════════
```

### 3. Verificar con API directamente

```bash
curl -X POST http://localhost:8000/api/tareas/ml/analizar-respuesta \
  -H "Content-Type: application/json" \
  -d '{
    "nino_id": 1,
    "ejercicio_id": 10,
    "tiempo_ms": 25000,
    "correcto": false,
    "tab_blur_count": 0,
    "idle_ms": 0,
    "erratic_clicks": 0
  }'
```

**Respuesta esperada:**
```json
{
  "distraccion": {
    "requiere_descanso": true,
    "motivo": "tiempo_excesivo",
    "detalles": "Tardó 25000ms (promedio: 4500ms)",
    "focus_score": 0.3
  },
  "tiempo_promedio_historico": 4500,
  "debug": {
    "tiempo_actual_ms": 25000,
    "triple_promedio_ms": 13500,
    "cantidad_datos_historicos": 30
  }
}
```

## 📊 Cómo funciona internamente

### Backend (ml_utils.py)
```python
# Calcula el promedio histórico
tiempo_promedio_historico = promedio_ultimos_30_ejercicios

# Si el tiempo actual > 3x promedio → activa descanso
if tiempo_ms > (tiempo_promedio_historico * 3):
    return {
        'requiere_descanso': True,
        'motivo': 'tiempo_excesivo',
        'detalles': f'Tardó {tiempo_ms}ms (promedio: {promedio}ms)'
    }
```

### Backend (views.py)
```python
# En AnalizarRespuestaView
historial_tiempos = EjercicioProgreso.objects.filter(
    student=nino,
    time_spent_ms__gt=0,
    time_spent_ms__lt=180000  # Excluir outliers
).order_by('-created_at')[:30]

tiempo_promedio_historico = sum(historial) / len(historial)

# Pasa el promedio a detectar_distraccion
distraccion = detectar_distraccion(historial, tiempo_promedio_historico)
```

### Frontend (nino-tarea.component.ts)
```typescript
// Llama a la API y muestra logs mejorados
this.mlService.analizarRespuesta({...}).subscribe(resultado => {
  console.log('📊 ANÁLISIS ML COMPLETADO');
  console.log(`⏱️  Tiempo actual: ${tiempo}ms`);
  console.log(`📈 Promedio histórico: ${promedio}ms`);
  
  if (resultado.distraccion.requiere_descanso) {
    this.mostrarPantallaDescanso(motivo);
  }
});
```

## ⚠️ Casos especiales

| Situación | Comportamiento |
|-----------|---------------|
| Niño nuevo (< 5 ejercicios) | Usa promedio de sesión actual como fallback |
| Outliers (> 3 minutos) | Se excluyen del cálculo del promedio |
| 3 errores consecutivos | Activa descanso independiente del tiempo |
| Focus score < 0.4 | Activa descanso por modelo ML |
| Tiempo > 3x promedio | ✅ Activa descanso por tiempo excesivo |

## 🎓 Ejemplo Real

**Niño: María**
- Promedio histórico: 5 segundos por ejercicio
- Umbral 3x: 15 segundos

**Escenarios:**
- Tarda 6 segundos → ✅ Normal
- Tarda 10 segundos → ✅ Normal  
- Tarda 12 segundos → ✅ Normal
- Tarda 16 segundos → 🛑 **PANTALLA DE DESCANSO**

## 🔍 Troubleshooting

| Problema | Solución |
|----------|----------|
| No se activa la pantalla | Verifica que el niño tenga al menos 5 ejercicios completados |
| Logs no aparecen | Abre la consola del navegador (F12) |
| Error 404 al analizar | Verifica que el nino_id existe en la BD |
| Siempre dice "historial insuficiente" | Completa más ejercicios para generar historial |

## ✅ Checklist de Verificación

- [ ] Script test_deteccion_tiempo.py ejecutado sin errores
- [ ] Logs visibles en consola del navegador (F12)
- [ ] Información de promedio histórico se muestra
- [ ] Pantalla de descanso se activa al tardar 3x
- [ ] API responde correctamente con curl/Postman

## 📁 Archivos modificados

1. `backend/tareas/views.py` - Agregado import de Ejercicio y modelos ML
2. `frontend/src/app/modules/nino/tarea/nino-tarea.component.ts` - Logs mejorados
3. `backend/test_deteccion_tiempo.py` - Nuevo script de prueba

**Funcionalidad ya existente:**
- `backend/tareas/ml_utils.py` - Lógica de detección (ya implementada)
- La base de datos y modelos ya estaban configurados correctamente

---

**🎉 ¡Listo! La detección por tiempo ya está funcionando.**
