import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

interface EstadisticasGenerales {
  total_estudiantes: number;
  total_tareas_completadas: number;
  promedio_aciertos: number;
  promedio_errores: number;
  total_monedas_sistema: number;
  total_xp_sistema: number;
  estudiantes_activos: number;
  tareas_por_tipo: { tipo: string; cantidad: number }[];
  distribucion_niveles: { nivel: number; cantidad: number }[];
  rendimiento_semanal: { dia: string; aciertos: number; errores: number }[];
}

@Component({
  selector: 'app-reportes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reportes.component.html',
  styleUrls: ['./reportes.component.css']
})
export class ReportesComponent implements OnInit {
  stats: EstadisticasGenerales | null = null;
  loading = true;
  generandoPDF = false;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.cargarEstadisticas();
  }

  cargarEstadisticas(): void {
    this.loading = true;
    this.api.get<EstadisticasGenerales>('director/estadisticas-generales').subscribe({
      next: data => {
        this.stats = data;
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando estadísticas', err);
        this.loading = false;
      }
    });
  }

  get promedioRendimiento(): number {
    if (!this.stats) return 0;
    const total = this.stats.promedio_aciertos + this.stats.promedio_errores;
    return total > 0 ? (this.stats.promedio_aciertos / total) * 100 : 0;
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
      pdf.save(`reporte-general-${fecha}.pdf`);
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
}
