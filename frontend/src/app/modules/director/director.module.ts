import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { SharedModule } from '../../shared/shared.module';

import { DirectorLayoutComponent } from './director-layout.component';
import { DirectorDashboardComponent } from './dashboard/director-dashboard.component';
import { UsuariosComponent } from './usuarios/usuarios.component';
import { EstadisticasComponent } from './estadisticas/estadisticas.component';
import { LogsComponent } from './logs/logs.component';
import { ReportesComponent } from './reportes/reportes.component';
import { TutorialDirectorComponent } from './tutorial/tutorial-director.component';

const routes: Routes = [
  {
    path: '',
    component: DirectorLayoutComponent,
    children: [
      { path: 'dashboard',   component: DirectorDashboardComponent },
      { path: 'usuarios',    component: UsuariosComponent },
      { path: 'estadisticas',component: EstadisticasComponent },
      { path: 'reportes',    component: ReportesComponent },
      { path: 'logs',        component: LogsComponent },
      { path: 'tutorial',    component: TutorialDirectorComponent },
      { path: '',            redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  }
];

@NgModule({
  imports: [
    CommonModule, ReactiveFormsModule, FormsModule, SharedModule, RouterModule.forChild(routes),
    DirectorLayoutComponent,
    DirectorDashboardComponent,
    UsuariosComponent,
    EstadisticasComponent,
    ReportesComponent,
    LogsComponent,
    TutorialDirectorComponent
  ]
})
export class DirectorModule {}
