import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import { StatCardComponent } from './components/stat-card/stat-card.component';

@NgModule({
  imports: [CommonModule, RouterModule, SidebarComponent, StatCardComponent],
  exports: [SidebarComponent, StatCardComponent]
})
export class SharedModule {}
