import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { User } from '../../core/auth/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  @Input() title: string = 'Fantasy Inn Tycoon';
  @Input() currentUser: User | null = null;
  @Output() newGame = new EventEmitter<void>();
  @Output() signOut = new EventEmitter<void>();

  onNewGame(): void {
    this.newGame.emit();
  }

  onSignOut(): void {
    this.signOut.emit();
  }
}
