import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { SharedModule } from '../../shared/shared.module';

import { ProfesorLayoutComponent } from './profesor-layout.component';
import { ProfesorDashboardComponent } from './dashboard/profesor-dashboard.component';
import { TareasComponent } from './tareas/tareas.component';
import { EstudiantesComponent } from './estudiantes/estudiantes.component';
import { InventarioProfesorComponent } from './inventario/inventario-profesor.component';
import { ReportesProfesorComponent } from './reportes/reportes-profesor.component';
import { TutorialProfesorComponent } from './tutorial/tutorial-profesor.component';

const routes: Routes = [
  {
    path: '',
    component: ProfesorLayoutComponent,
    children: [
      { path: 'dashboard',  component: ProfesorDashboardComponent },
      { path: 'tareas',     component: TareasComponent },
      { path: 'estudiantes',component: EstudiantesComponent },
      { path: 'inventario', component: InventarioProfesorComponent },
      { path: 'reportes',   component: ReportesProfesorComponent },
      { path: 'tutorial',   component: TutorialProfesorComponent },
      { path: '',           redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  }
];

@NgModule({
  imports: [
    CommonModule, ReactiveFormsModule, FormsModule, SharedModule, RouterModule.forChild(routes),
    ProfesorLayoutComponent,
    ProfesorDashboardComponent,
    TareasComponent,
    EstudiantesComponent,
    InventarioProfesorComponent,
    ReportesProfesorComponent,
    TutorialProfesorComponent
  ]
})
export class ProfesorModule {}
