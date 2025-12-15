import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InnState } from '../../models/game.models';

@Component({
  selector: 'app-resources-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './resources-panel.component.html',
  styleUrl: './resources-panel.component.css'
})
export class ResourcesPanelComponent {
  @Input() gameState!: InnState;
}
