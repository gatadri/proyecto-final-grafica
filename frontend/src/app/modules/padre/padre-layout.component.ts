import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MenuItem, SidebarComponent } from '../../shared/components/sidebar/sidebar.component';

@Component({
  selector: 'app-padre-layout',
  standalone: true,
  imports: [RouterModule, SidebarComponent],
  template: `
    <div class="d-flex">
      <app-sidebar [menuItems]="menu"></app-sidebar>
      <div class="main-content flex-grow-1 p-4"><router-outlet></router-outlet></div>
    </div>
  `
})
export class PadreLayoutComponent {
  menu: MenuItem[] = [
    { label: 'Dashboard',  icon: 'tachometer-alt', route: '/padre/dashboard'  },
    { label: 'Calendario', icon: 'calendar',        route: '/padre/calendario' },
    { label: 'Reportes',   icon: 'chart-line',      route: '/padre/reportes'   },
    { label: 'Logros',     icon: 'trophy',          route: '/padre/logros'     }
  ];
}
