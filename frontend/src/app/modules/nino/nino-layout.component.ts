import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AvatarSelectorComponent } from '../../shared/components/avatar-selector/avatar-selector.component';

@Component({
  selector: 'app-nino-layout',
  standalone: true,
  imports: [RouterModule, AvatarSelectorComponent],
  template: `
    <router-outlet></router-outlet>
    <app-avatar-selector></app-avatar-selector>
  `
})
export class NinoLayoutComponent {}
