import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { PadreLayoutComponent } from './padre-layout.component';
import { PadreDashboardComponent } from './dashboard/padre-dashboard.component';
import { CalendarioComponent } from './calendario/calendario.component';
import { LogrosPadreComponent } from './logros/logros-padre.component';
import { ReportesPadreComponent } from './reportes/reportes-padre.component';

const routes: Routes = [
  {
    path: '',
    component: PadreLayoutComponent,
    children: [
      { path: 'dashboard',  component: PadreDashboardComponent },
      { path: 'calendario', component: CalendarioComponent },
      { path: 'logros',     component: LogrosPadreComponent },
      { path: 'reportes',   component: ReportesPadreComponent },
      { path: '',           redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  }
];

@NgModule({
  imports: [
    CommonModule, SharedModule, RouterModule.forChild(routes),
    PadreLayoutComponent, PadreDashboardComponent, CalendarioComponent, LogrosPadreComponent, ReportesPadreComponent
  ]
})
export class PadreModule {}
