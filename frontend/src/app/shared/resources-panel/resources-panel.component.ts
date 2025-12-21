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
  showAchievements = false;

  toggleIncomeBreakdown(): void {
    this.showIncomeBreakdown = !this.showIncomeBreakdown;
    if (this.showIncomeBreakdown) {
      this.showMultiplierBreakdown = false;
      this.showAchievements = false;
    }
  }

  toggleMultiplierBreakdown(): void {
    this.showMultiplierBreakdown = !this.showMultiplierBreakdown;
    if (this.showMultiplierBreakdown) {
      this.showIncomeBreakdown = false;
      this.showAchievements = false;
    }
  }

  toggleAchievements(): void {
    this.showAchievements = !this.showAchievements;
    if (this.showAchievements) {
      this.showIncomeBreakdown = false;
      this.showMultiplierBreakdown = false;
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
    return this.getActiveGuests().reduce((sum, guest) => {
      return sum + this.getGuestActualIncome(guest);
    }, 0);
  }

  // Room-specific income calculations
  getRoomForGuest(guest: any) {
    if (!this.gameState || !this.gameState.rooms || !guest.room_id) return null;
    return this.gameState.rooms.find(r => r.id === guest.room_id);
  }

  getRoomTemplate(roomType: string) {
    if (!this.gameState || !this.gameState.room_types) return null;
    return this.gameState.room_types.find(rt => rt.id === roomType);
  }

  getRoomBonus(room: any, guest: any): number {
    if (!room || !guest) return 1.0;

    const roomTemplate = this.getRoomTemplate(room.room_type);
    if (!roomTemplate) return 1.0;

    let bonusMultiplier = 1.0;

    // Check species bonuses
    if (roomTemplate.species_bonuses && roomTemplate.species_bonuses[guest.species]) {
      bonusMultiplier = Math.max(bonusMultiplier, roomTemplate.species_bonuses[guest.species]);
    }

    // Check guest type bonuses
    if (roomTemplate.type_bonuses && roomTemplate.type_bonuses[guest.guest_type]) {
      bonusMultiplier = Math.max(bonusMultiplier, roomTemplate.type_bonuses[guest.guest_type]);
    }

    return bonusMultiplier;
  }

  getGuestActualIncome(guest: any): number {
    const room = this.getRoomForGuest(guest);
    if (!room) return guest.gold_per_tick;

    const roomBonus = this.getRoomBonus(room, guest);
    return guest.gold_per_tick * room.income_rate * roomBonus;
  }

  getGuestIncomeBreakdown(guest: any) {
    const room = this.getRoomForGuest(guest);
    if (!room) {
      return {
        base: guest.gold_per_tick,
        roomRate: 1,
        roomBonus: 1,
        total: guest.gold_per_tick
      };
    }

    const roomBonus = this.getRoomBonus(room, guest);
    return {
      base: guest.gold_per_tick,
      roomRate: room.income_rate,
      roomBonus: roomBonus,
      total: guest.gold_per_tick * room.income_rate * roomBonus
    };
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

  getNetIncomePerTick(): number {
    return (this.getTotalGuestIncome() * this.gameState.total_income_multiplier) - this.getTotalOperationalCost();
  }

  getPassiveIncomePerHour(): number {
    // Assuming ~60 ticks per minute, 3600 ticks per hour (game speed dependent)
    const ticksPerHour = 3600 / (this.gameState.game_speed || 1);
    return this.getNetIncomePerTick() * ticksPerHour;
  }

  getEstimatedOfflineEarnings(): number {
    return this.getPassiveIncomePerHour() * this.gameState.max_offline_hours;
  }

  // Achievements helpers
  getCompletedAchievements() {
    if (!this.gameState || !this.gameState.all_achievements) return [];
    return this.gameState.all_achievements.filter(a => a.is_completed);
  }

  getInProgressAchievements() {
    if (!this.gameState || !this.gameState.all_achievements) return [];
    return this.gameState.all_achievements.filter(a => !a.is_completed && a.progress > 0);
  }

  getLockedAchievements() {
    if (!this.gameState || !this.gameState.all_achievements) return [];
    return this.gameState.all_achievements.filter(a => a.progress === 0);
  }

  getTotalAchievements(): number {
    if (!this.gameState || !this.gameState.all_achievements) return 0;
    return this.gameState.all_achievements.length;
  }

  getProgressPercentage(achievement: any): number {
    if (achievement.requirement_value === 0) return 0;
    return Math.min(100, (achievement.progress / achievement.requirement_value) * 100);
  }
}
