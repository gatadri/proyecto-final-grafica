import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Logro, Nino } from '../../../core/models';

@Component({
  selector: 'app-nino-logros',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './nino-logros.component.html'
})
export class NinoLogrosComponent implements OnInit {
  nino!: Nino;
  logros: Logro[] = [];
  loading = true;

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.nino = this.auth.getNino()!;
    this.api.get<any>(`nino/${this.nino.pin}/logros`).subscribe({
      next: d => { this.logros = d.logros ?? d; this.loading = false; },
      error: () => this.loading = false
    });
  }
}
