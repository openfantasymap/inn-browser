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
  showIncomeBreakdown = false;
  showMultiplierBreakdown = false;

  toggleIncomeBreakdown(): void {
    this.showIncomeBreakdown = !this.showIncomeBreakdown;
    if (this.showIncomeBreakdown) {
      this.showMultiplierBreakdown = false;
    }
  }

  toggleMultiplierBreakdown(): void {
    this.showMultiplierBreakdown = !this.showMultiplierBreakdown;
    if (this.showMultiplierBreakdown) {
      this.showIncomeBreakdown = false;
    }
  }

  getIncomeUpgrades() {
    if (!this.gameState || !this.gameState.upgrades) return [];
    return this.gameState.upgrades.filter(u =>
      u.effect_type === 'income_multiplier' && u.purchased
    );
  }

  getActiveGuests() {
    if (!this.gameState || !this.gameState.guests) return [];
    return this.gameState.guests.filter(g => g.room_id !== null);
  }

  getTotalGuestIncome(): number {
    return this.getActiveGuests().reduce((sum, guest) => sum + guest.gold_per_tick, 0);
  }

  getBaseMultiplier(): number {
    return 1.0;
  }

  getUpgradeMultipliers() {
    const upgrades = this.getIncomeUpgrades();
    return upgrades.map(u => ({
      name: u.name,
      multiplier: u.effect_value
    }));
  }

  getTotalOperationalCost(): number {
    if (!this.gameState || !this.gameState.upgrades) return 0;
    return this.gameState.upgrades
      .filter(u => u.purchased && u.operational_cost_per_tick)
      .reduce((sum, u) => sum + (u.operational_cost_per_tick || 0), 0);
  }
}
