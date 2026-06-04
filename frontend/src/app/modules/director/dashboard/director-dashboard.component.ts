import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MockDataService } from '../../../core/services/mock-data.service';

@Component({
  selector: 'app-director-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './director-dashboard.component.html'
})
export class DirectorDashboardComponent implements OnInit {
  stats: any = {};
  loading = true;
  constructor(private mock: MockDataService) {}
  ngOnInit(): void {
    this.stats = {
      ...this.mock.getDashboardDirector(),
      tareas_completadas: this.mock.getTareas().reduce((s:number, t:any) => s, 0),
      xp_total:     this.mock.getNinos().reduce((s:number, n:any) => s + n.experiencia, 0),
      monedas_total: this.mock.getNinos().reduce((s:number, n:any) => s + n.monedas, 0),
      logros_total:  this.mock.getLogros().length,
    };
    this.loading = false;
  }
}
