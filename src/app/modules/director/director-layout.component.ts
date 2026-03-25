import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MenuItem, SidebarComponent } from '../../shared/components/sidebar/sidebar.component';

@Component({
  selector: 'app-director-layout',
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
export class DirectorLayoutComponent {
  menu: MenuItem[] = [
    { label: 'Dashboard',          icon: 'tachometer-alt',  route: '/director/dashboard'    },
    { label: 'Gestión de Usuarios',icon: 'users',           route: '/director/usuarios'     },
    { label: 'Inventario Tienda',  icon: 'store',           route: '/director/inventario'   },
    { label: 'Estadísticas',       icon: 'chart-line',      route: '/director/estadisticas' },
    { label: 'Reportes',           icon: 'chart-bar',       route: '/director/reportes'     },
    { label: 'Log de Actividades', icon: 'history',         route: '/director/logs'         }
  ];
}
