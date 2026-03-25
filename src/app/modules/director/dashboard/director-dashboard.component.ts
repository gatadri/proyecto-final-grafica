import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatCardComponent } from '../../../shared/components/stat-card/stat-card.component';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-director-dashboard',
  standalone: true,
  imports: [CommonModule, StatCardComponent],
  templateUrl: './director-dashboard.component.html'
})
export class DirectorDashboardComponent implements OnInit {
  stats: any = {};
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.get<any>('dashboard/director').subscribe({
      next: data => { this.stats = data; this.loading = false; },
      error: ()  => { this.loading = false; }
    });
  }
}
