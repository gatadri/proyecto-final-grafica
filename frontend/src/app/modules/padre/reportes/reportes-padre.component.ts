import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { MLService } from '../../../services/ml.service';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

interface EstadisticasHijo {
  id: number;
  nombre: string;
  apellido: string;
  nivel: number;
  experiencia: number;
  monedas: number;
  racha_dias: number;
  tareas_completadas: number;
  total_aciertos: number;
  total_errores: number;
  promedio_tiempo_ms: number;
  tasa_exito: number;
  ultima_actividad: string;
}

interface EstadisticasGrupales {
  total_hijos: number;
  total_tareas_completadas: number;
  total_aciertos: number;
  total_errores: number;
  promedio_nivel: number;
  total_monedas: number;
  hijo_mas_activo: string;
  mejor_rendimiento: string;
  rendimiento_semanal: { dia: string; aciertos: number; errores: number }[];
}

interface TemaProblematico {
  tema: string;
  tema_legible: string;
  errores: number;
  aciertos: number;
  porcentaje_error: number;
  tiempo_promedio_ms: number;
  tarea_id: number;
  tarea_titulo: string;
}

interface ReportePorSubtema {
  subtema: string;
  total_errores: number;
  total_aciertos: number;
  temas_problematicos: TemaProblematico[];
}

interface ReporteML {
  nino: any;
  padre: any;
  profesor: any;
  reporte_por_subtema: ReportePorSubtema[];
  resumen: {
    total_errores: number;
    total_aciertos: number;
    subtemas_con_dificultad: number;
  };
}

@Component({
  selector: 'app-reportes-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reportes-padre.component.html',
  styleUrls: ['./reportes-padre.component.css']
})
export class ReportesPadreComponent implements OnInit {
  estadisticasHijos: EstadisticasHijo[] = [];
  estadisticasGrupales: EstadisticasGrupales | null = null;
  hijoSeleccionado: EstadisticasHijo | null = null;
  reporteML: ReporteML | null = null;
  loadingReporteML = false;
  loading = true;
  generandoPDF = false;
  padreId: number = 0;

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private mlService: MLService
  ) {}

  ngOnInit(): void {
    const user = this.auth.getUser();
    if (user) {
      this.padreId = user.id;
      this.cargarEstadisticas();
    }
  }

  cargarEstadisticas(): void {
    this.loading = true;
    this.api.get<any>(`padre/${this.padreId}/estadisticas-hijos`).subscribe({
      next: data => {
        this.estadisticasHijos = data.estadisticas_individuales;
        this.estadisticasGrupales = data.estadisticas_grupales;
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando estadísticas', err);
        this.loading = false;
      }
    });
  }

  seleccionarHijo(hijo: EstadisticasHijo): void {
    this.hijoSeleccionado = hijo;
    this.cargarReporteML(hijo.id);
  }

  verGrupal(): void {
    this.hijoSeleccionado = null;
    this.reporteML = null;
  }

  cargarReporteML(ninoId: number): void {
    this.loadingReporteML = true;
    this.reporteML = null;
    this.mlService.obtenerReporteDetallado(ninoId).subscribe({
      next: (data) => {
        this.reporteML = data;
        this.loadingReporteML = false;
      },
      error: (err) => {
        console.error('Error cargando reporte ML', err);
        this.loadingReporteML = false;
      }
    });
  }

  async descargarPDF(): Promise<void> {
    this.generandoPDF = true;
    
    const elemento = document.getElementById('reporte-contenido');
    if (!elemento) {
      this.generandoPDF = false;
      return;
    }

    try {
      const canvas = await html2canvas(elemento, {
        scale: 2,
        logging: false,
        useCORS: true
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgWidth = 210;
      const pageHeight = 297;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      let heightLeft = imgHeight;
      let position = 0;

      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      const fecha = new Date().toISOString().split('T')[0];
      const tipo = this.hijoSeleccionado ? 'individual' : 'grupal';
      pdf.save(`reporte-${tipo}-${fecha}.pdf`);
    } catch (error) {
      console.error('Error generando PDF:', error);
      alert('Error al generar el PDF');
    } finally {
      this.generandoPDF = false;
    }
  }

  get currentDate(): Date {
    return new Date();
  }

  formatearTiempo(ms: number): string {
    const minutos = Math.floor(ms / 60000);
    const segundos = Math.floor((ms % 60000) / 1000);
    return `${minutos}m ${segundos}s`;
  }

  getRecomendaciones(): string[] {
    if (!this.reporteML) return [];
    
    const recs: string[] = [];
    
    for (const subtema of this.reporteML.reporte_por_subtema) {
      if (subtema.total_errores >= 5) {
        const temasTop = subtema.temas_problematicos
          .slice(0, 2)
          .map(t => t.tema_legible)
          .join(' y ');
        
        recs.push(`Reforzar ${subtema.subtema}: especialmente ${temasTop}. Practiquen juntos en casa.`);
      }
    }
    
    if (recs.length === 0) {
      recs.push('Continuar practicando regularmente. ¡Su hijo va por buen camino!');
    }
    
    return recs;
  }
}
