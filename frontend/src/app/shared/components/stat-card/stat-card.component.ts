import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  template: `
    <div class="card text-center h-100">
      <div class="card-body">
        <i class="fas fa-{{ icon }} fa-2x text-{{ color }} mb-2"></i>
        <h4 class="fw-bold">{{ value }}</h4>
        <p class="text-muted mb-0">{{ label }}</p>
      </div>
    </div>
  `
})
export class StatCardComponent {
  @Input() icon  = 'chart-bar';
  @Input() value: number | string = 0;
  @Input() label = '';
  @Input() color = 'primary';
}
