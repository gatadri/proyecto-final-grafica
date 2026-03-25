import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { NinoLoginComponent } from './nino-login/nino-login.component';

const routes: Routes = [
  { path: 'login',      component: LoginComponent },
  { path: 'register',   component: RegisterComponent },
  { path: 'nino-login', component: NinoLoginComponent },
  { path: '',           redirectTo: 'login', pathMatch: 'full' }
];

@NgModule({
  imports: [CommonModule, ReactiveFormsModule, RouterModule.forChild(routes), LoginComponent, RegisterComponent, NinoLoginComponent]
})
export class AuthModule {}
