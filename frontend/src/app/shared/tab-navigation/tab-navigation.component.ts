import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-tab-navigation',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tab-navigation.component.html',
  styleUrl: './tab-navigation.component.css'
})
export class TabNavigationComponent {
  @Input() activeTab: 'inn' | 'tavern' = 'inn';
  @Input() guests: number = 0;
  @Output() tabChange = new EventEmitter<'inn' | 'tavern'>();

  switchTab(tab: 'inn' | 'tavern'): void {
    this.tabChange.emit(tab);
  }
}
