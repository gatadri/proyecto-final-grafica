import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { SharedModule } from '../../shared/shared.module';

import { DirectorLayoutComponent } from './director-layout.component';
import { DirectorDashboardComponent } from './dashboard/director-dashboard.component';
import { UsuariosComponent } from './usuarios/usuarios.component';
import { InventarioDirectorComponent } from './inventario/inventario-director.component';
import { EstadisticasComponent } from './estadisticas/estadisticas.component';
import { LogsComponent } from './logs/logs.component';
import { ReportesComponent } from './reportes/reportes.component';

const routes: Routes = [
  {
    path: '',
    component: DirectorLayoutComponent,
    children: [
      { path: 'dashboard',   component: DirectorDashboardComponent },
      { path: 'usuarios',    component: UsuariosComponent },
      { path: 'inventario',  component: InventarioDirectorComponent },
      { path: 'estadisticas',component: EstadisticasComponent },
      { path: 'reportes',    component: ReportesComponent },
      { path: 'logs',        component: LogsComponent },
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
    InventarioDirectorComponent,
    EstadisticasComponent,
    ReportesComponent,
    LogsComponent
  ]
})
export class DirectorModule {}
