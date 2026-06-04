import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MLService {
  private apiUrl = 'http://localhost:8000/api/tareas/ml';

  constructor(private http: HttpClient) { }

  analizarRespuesta(datos: {
    nino_id: number;
    ejercicio_id: number;
    tiempo_ms: number;
    correcto: boolean;
    tab_blur_count?: number;
    idle_ms?: number;
    erratic_clicks?: number;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}/analizar-respuesta`, datos);
  }

  obtenerReporteErrores(ninoId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/reporte-errores?nino_id=${ninoId}`);
  }

  notificarPadreProfesor(ninoId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/notificar`, { nino_id: ninoId });
  }

  obtenerEstadisticas(ninoId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/estadisticas?nino_id=${ninoId}`);
  }

  obtenerReporteDetallado(ninoId: number, tareaId?: number): Observable<any> {
    let url = `${this.apiUrl}/reporte-detallado?nino_id=${ninoId}`;
    if (tareaId) {
      url += `&tarea_id=${tareaId}`;
    }
    return this.http.get(url);
  }
}
