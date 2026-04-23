import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';
import { NinoGuard } from './core/guards/nino.guard';
import { LandingComponent } from './landing/landing.component';

const routes: Routes = [
  { path: '', component: LandingComponent },

  // Auth
  {
    path: 'auth',
    loadChildren: () => import('./modules/auth/auth.module').then(m => m.AuthModule)
  },

  // Director
  {
    path: 'director',
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['director'] },
    loadChildren: () => import('./modules/director/director.module').then(m => m.DirectorModule)
  },

  // Profesor
  {
    path: 'profesor',
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['profesor', 'director'] },
    loadChildren: () => import('./modules/profesor/profesor.module').then(m => m.ProfesorModule)
  },

  // Padre
  {
    path: 'padre',
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['padre'] },
    loadChildren: () => import('./modules/padre/padre.module').then(m => m.PadreModule)
  },

  // Niño (acceso por PIN, sin token)
  {
    path: 'nino',
    canActivate: [NinoGuard],
    loadChildren: () => import('./modules/nino/nino.module').then(m => m.NinoModule)
  },

  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
