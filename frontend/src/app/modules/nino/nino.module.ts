import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

import { NinoLayoutComponent } from './nino-layout.component';
import { NinoDashboardComponent } from './dashboard/nino-dashboard.component';
import { NinoTareaComponent } from './tarea/nino-tarea.component';
import { NinoTiendaComponent } from './tienda/nino-tienda.component';
import { NinoLogrosComponent } from './logros/nino-logros.component';
import { NinoPracticaComponent } from './practica/nino-practica.component';
import { AprenderComponent } from './aprender/aprender.component';

const routes: Routes = [
  {
    path: '',
    component: NinoLayoutComponent,
    children: [
      { path: 'dashboard', component: NinoDashboardComponent },
      { path: 'tarea/:id', component: NinoTareaComponent },
      { path: 'tienda',    component: NinoTiendaComponent },
      { path: 'logros',    component: NinoLogrosComponent },
      { path: 'practica',  component: NinoPracticaComponent },
      { path: 'aprender',  component: AprenderComponent },
      { path: '',          redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  }
];

@NgModule({
  imports: [
    CommonModule, ReactiveFormsModule, FormsModule, RouterModule.forChild(routes),
    NinoLayoutComponent,
    NinoDashboardComponent,
    NinoTareaComponent,
    NinoTiendaComponent,
    NinoLogrosComponent,
    NinoPracticaComponent,
    AprenderComponent
  ]
})
export class NinoModule {}
