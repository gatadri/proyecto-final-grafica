import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MenuItem, SidebarComponent } from '../../shared/components/sidebar/sidebar.component';

@Component({
  selector: 'app-profesor-layout',
  standalone: true,
  imports: [RouterModule, SidebarComponent],
  template: `
    <div class="d-flex">
      <app-sidebar [menuItems]="menu"></app-sidebar>
      <div class="main-content flex-grow-1">
        <div class="content-wrapper p-4">
          <router-outlet></router-outlet>
        </div>
      </div>
    </div>
  `
})
export class ProfesorLayoutComponent {
  menu: MenuItem[] = [
    { label: 'Dashboard',        icon: 'tachometer-alt', route: '/profesor/dashboard'  },
    { label: 'Mis Tareas',       icon: 'tasks',          route: '/profesor/tareas'     },
    { label: 'Mis Estudiantes',  icon: 'users',          route: '/profesor/estudiantes'},
    { label: 'Inventario Tienda',icon: 'store',          route: '/profesor/inventario' }
  ];
}
