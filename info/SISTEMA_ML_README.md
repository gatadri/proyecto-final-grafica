# Sistema de Predicción de Errores y Detección de Distracciones

## Descripción

Sistema de Machine Learning que:
1. **Predice tipos de errores** en ejercicios matemáticos (fracciones, multiplicación, álgebra, etc.)
2. **Detecta distracciones** mediante análisis de comportamiento del estudiante
3. **Muestra pantalla de descanso** de 10 segundos cuando se detecta distracción
4. **Notifica a padres y profesores** sobre áreas problemáticas

## Arquitectura

### Backend (Django + TensorFlow)
- **Modelos ML entrenados**: FFN (errores) y RNN (distracción)
- **API REST**: Endpoints para análisis en tiempo real
- **Base de datos**: Almacena predicciones y eventos

### Frontend (Angular)
- **Componente de descanso**: Pantalla animada de 10 segundos
- **Servicio ML**: Integración con API
- **Detección automática**: Analiza cada respuesta

## Instalación

### 1. Dependencias Python
```bash
cd ml
pip install -r requirements.txt
```

### 2. Entrenar modelos (ya está hecho)
```bash
cd ..
python ml/train.py
```

### 3. Aplicar migraciones (ya está hecho)
```bash
cd backend
python manage.py migrate
```

### 4. Iniciar servidor Django
```bash
python manage.py runserver
```

## Uso

### API Endpoints

#### 1. Analizar respuesta
```http
POST /api/tareas/ml/analizar-respuesta
Content-Type: application/json

{
  "nino_id": 1,
  "ejercicio_id": 1,
  "tiempo_ms": 15000,
  "correcto": false,
  "tab_blur_count": 3,
  "idle_ms": 5000,
  "erratic_clicks": 8
}
```

**Respuesta:**
```json
{
  "prediccion": {
    "error_type": "fracciones",
    "prob_mistake_next": 0.75
  },
  "distraccion": {
    "requiere_descanso": true,
    "focus_score": 0.35
  }
}
```

#### 2. Reporte de errores
```http
GET /api/tareas/ml/reporte-errores?nino_id=1
```

#### 3. Notificar padre y profesor
```http
POST /api/tareas/ml/notificar
Content-Type: application/json

{
  "nino_id": 1
}
```

#### 4. Estadísticas
```http
GET /api/tareas/ml/estadisticas?nino_id=1
```

## Integración Frontend

### Usar en componente de ejercicios:

```typescript
import { Component, ViewChild } from '@angular/core';
import { MLService } from './services/ml.service';
import { PantallaDescansoComponent } from './components/pantalla-descanso.component';

export class EjerciciosComponent {
  @ViewChild(PantallaDescansoComponent) pantallaDescanso!: PantallaDescansoComponent;

  constructor(private mlService: MLService) {}

  onRespuestaSubmit(ejercicio: any, respuesta: any, tiempo: number) {
    const datos = {
      nino_id: this.ninoActual.id,
      ejercicio_id: ejercicio.id,
      tiempo_ms: tiempo,
      correcto: respuesta === ejercicio.respuesta_correcta,
      tab_blur_count: this.contadorCambiosPestana,
      idle_ms: this.tiempoInactivo,
      erratic_clicks: this.clicksErraticos
    };

    this.mlService.analizarRespuesta(datos).subscribe(result => {
      // Si requiere descanso, mostrar pantalla
      if (result.distraccion.requiere_descanso) {
        this.pantallaDescanso.iniciarDescanso();
      }

      // Si hay predicción de error, guardarlo
      if (result.prediccion) {
        console.log('Tipo de error detectado:', result.prediccion.error_type);
      }
    });
  }
}
```

### Template:
```html
<app-pantalla-descanso></app-pantalla-descanso>

<div class="ejercicios">
  <!-- Tu código de ejercicios -->
</div>
```

## Pruebas

Ejecutar script de pruebas:
```bash
cd backend
python test_ml_system.py
```

## Tipos de Errores Detectados

1. **fracciones** - Errores en operaciones con fracciones
2. **multiplicacion** - Errores en multiplicaciones
3. **division** - Errores en divisiones
4. **algebra** - Errores en álgebra
5. **geometria** - Errores en geometría
6. **procedimiento** - Errores de procedimiento
7. **conceptual** - Errores conceptuales
8. **inatencion** - Errores por falta de atención
9. **consigna** - Errores al leer la consigna
10. **aleatorio** - Errores aleatorios

## Indicadores de Distracción

- **tab_blur_count**: Cambios de pestaña/ventana
- **idle_ms**: Tiempo sin actividad
- **erratic_clicks**: Clicks fuera de elementos interactivos
- **time_spent_ms**: Tiempo muy alto o muy bajo
- **focus_score**: < 0.4 = requiere descanso

## Base de Datos

### Tabla: tareas_prediccionerror
- nino_id
- tipo_error
- probabilidad
- fecha_prediccion
- notificado

### Tabla: tareas_eventodistruccion
- nino_id
- focus_score
- tab_blur_count
- idle_ms
- erratic_clicks
- fecha_evento
- descanso_mostrado

## Notas Importantes

1. Los modelos ya están entrenados y listos en `ml/models/`
2. El sistema funciona en tiempo real
3. La pantalla de descanso es automática (10 segundos)
4. Las notificaciones se preparan pero no se envían por email (implementar según necesidad)
5. El CSV de entrenamiento contiene 50 ejemplos sintéticos

## Próximos Pasos

1. Implementar envío real de emails
2. Agregar más datos de entrenamiento reales
3. Crear dashboard para profesores/padres
4. Ajustar umbrales de detección según necesidad
5. Agregar más tipos de errores específicos
