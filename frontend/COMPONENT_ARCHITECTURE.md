# Component Architecture & Refactoring Guide

## Overview

The Fantasy Inn Tycoon application has been refactored to support a more modular, component-based architecture with Google Authentication integration.

## Implemented Features

### ✅ Authentication System

**Location**: `src/app/core/auth/`

- **`auth.service.ts`**: Centralized authentication service
  - Google Sign-In integration using Google Identity Services
  - Local storage for session persistence
  - Guest mode support (play without signing in)
  - JWT decoding for user information extraction
  - Observable pattern for reactive auth state

- **`login/`**: Login component
  - Beautiful login screen with Google Sign-In button
  - "Continue as Guest" option for non-authenticated play
  - Responsive design matching game aesthetic
  - Auto-loads Google Identity Services script

**Key Features**:
- Persistent login via localStorage
- User profile display with avatar
- Sign out functionality
- Guest mode for quick play
- Reactive authentication state management

### 🏗️ Generated Component Scaffolds

Component scaffolds have been created for future refactoring:

#### Shared Components (`src/app/shared/`)
- `header/` - Game header with title and actions
- `resources-panel/` - Resource display (gold, reputation, etc.)
- `tab-navigation/` - Tab switcher for Inn vs Tavern

#### Inn Feature Components (`src/app/features/inn/`)
- `rooms-section/` - Room management interface
- `waiting-guests/` - Guest queue display
- `upgrades-section/` - Upgrade purchase interface

#### Tavern Feature Components (`src/app/features/tavern/`)
- `ingredient-store/` - Ingredient purchasing
- `recipe-discovery/` - Recipe experimentation
- `tavern-management/` - Crafting and guest serving

## Configuration

### Google Authentication Setup

1. **Get Google Client ID**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google Identity Services API
   - Create OAuth 2.0 credentials
   - Add authorized JavaScript origins (e.g., `http://localhost:4200`)

2. **Update Client ID**:
   ```typescript
   // File: src/app/core/auth/login/login.component.ts
   private readonly GOOGLE_CLIENT_ID = 'YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com';
   ```

3. **Test Authentication**:
   - Run `npm start`
   - You'll see the login screen
   - Click "Sign in with Google" or "Continue as Guest"

## Architecture Patterns

### Current State

**Before Refactoring**:
```
app.component (monolithic)
├── All game logic
├── All templates
└── All styles
```

**After Authentication**:
```
app.component (orchestrator)
├── Authentication check
├── Login component (when not authenticated)
└── Game interface (when authenticated)
```

### Recommended Future Structure

```
app/
├── core/
│   └── auth/                    ✅ IMPLEMENTED
│       ├── auth.service.ts
│       ├── auth.guard.ts (TODO)
│       └── login/
├── shared/
│   ├── header/                  📦 SCAFFOLD CREATED
│   ├── resources-panel/         📦 SCAFFOLD CREATED
│   └── tab-navigation/          📦 SCAFFOLD CREATED
├── features/
│   ├── inn/                     📦 SCAFFOLDS CREATED
│   │   ├── rooms-section/
│   │   ├── waiting-guests/
│   │   └── upgrades-section/
│   └── tavern/                  📦 SCAFFOLDS CREATED
│       ├── ingredient-store/
│       ├── recipe-discovery/
│       └── tavern-management/
└── services/
    └── game.service.ts          ✅ EXISTS
```

## Migration Guide

### Phase 1: Authentication (✅ Complete)

The authentication layer is fully functional and integrated.

### Phase 2: Extract Shared Components (Next Steps)

**Example: Creating Resources Panel Component**

1. **Move template HTML** from `app.component.html`:
```html
<!-- From app.component.html -->
<div class="resources-panel">
  <!-- Move this entire block to resources-panel.component.html -->
</div>
```

2. **Move related CSS** from `app.component.css` to `resources-panel.component.css`

3. **Create @Input decorator** for game state:
```typescript
// resources-panel.component.ts
@Input() gameState!: InnState;
```

4. **Use in parent**:
```html
<!-- app.component.html -->
<app-resources-panel [gameState]="gameState"></app-resources-panel>
```

### Phase 3: Extract Feature Components

Follow the same pattern for larger feature sections:

**Rooms Section Example**:
```typescript
@Component({
  selector: 'app-rooms-section',
  standalone: true
})
export class RoomsSectionComponent {
  @Input() gameState!: InnState;
  @Input() selectedGuest: Guest | null = null;
  @Output() guestSelected = new EventEmitter<Guest>();
  @Output() roomAction = new EventEmitter<{action: string, room: Room}>();

  // Move room-related methods here
}
```

## Benefits of This Architecture

### ✅ Already Achieved

1. **Authentication Integration**
   - Secure Google Sign-In
   - Guest mode for quick access
   - Persistent sessions
   - User profile display

2. **Improved Maintainability**
   - Clear separation of concerns (auth vs game logic)
   - Login component is fully isolated
   - Auth service is reusable across the app

3. **Component Scaffolds Ready**
   - All component files generated
   - Standalone components (no module boilerplate)
   - Ready for implementation

### 🎯 Future Benefits (When Fully Migrated)

1. **Easier Testing**
   - Components can be tested in isolation
   - Mock inputs/outputs easily
   - Focused unit tests

2. **Better Collaboration**
   - Multiple developers can work on different components
   - Less merge conflicts
   - Clear ownership of code sections

3. **Reusability**
   - Components can be used in multiple places
   - Shared components across features
   - Easier to build new features

4. **Performance**
   - Lazy loading potential
   - Change detection optimization
   - Smaller bundle sizes per route

## Testing

### Test Authentication Flow

1. **Start the dev server**:
   ```bash
   npm start
   ```

2. **Visit** `http://localhost:4200`

3. **You should see**:
   - Login screen with Fantasy Inn branding
   - Google Sign-In button
   - "Continue as Guest" button

4. **Test Guest Mode**:
   - Click "Continue as Guest"
   - Game should load immediately
   - User name shows as "Guest Player"

5. **Test Google Sign-In** (requires Google Client ID setup):
   - Click Google button
   - Complete Google authentication
   - Game loads with your Google profile

6. **Test Sign Out**:
   - Click "Sign Out" in header
   - Returns to login screen
   - Game state is cleared

## Code Examples

### Using Auth Service in Components

```typescript
import { AuthService } from './core/auth/auth.service';

export class MyComponent {
  constructor(private authService: AuthService) {
    // Subscribe to user changes
    this.authService.user$.subscribe(user => {
      console.log('Current user:', user);
    });

    // Check if authenticated
    if (this.authService.isAuthenticated()) {
      console.log('User is logged in');
    }

    // Get user ID for API calls
    const userId = this.authService.getUserId();
  }
}
```

### Component Communication Pattern

```typescript
// Parent Component
<app-child-component
  [inputData]="myData"
  (outputEvent)="handleEvent($event)">
</app-child-component>

// Child Component
export class ChildComponent {
  @Input() inputData: any;
  @Output() outputEvent = new EventEmitter<any>();

  doSomething() {
    this.outputEvent.emit({ data: 'value' });
  }
}
```

## Next Steps

### Immediate (Quick Wins)

1. **Configure Google Client ID** in `login.component.ts`
2. **Test authentication flow** thoroughly
3. **Consider backend changes** for user-specific game saves

### Short Term (Component Migration)

1. **Extract Header Component**
   - Move header HTML/CSS
   - Add @Input for user info
   - Add @Output for actions (new game, sign out)

2. **Extract Resources Panel**
   - Move resources display
   - Simple @Input for game state
   - Read-only display component

3. **Extract Tab Navigation**
   - Move tab switcher
   - @Input for active tab
   - @Output for tab changes

### Long Term (Full Refactoring)

1. **Extract all feature components**
2. **Add routing** (`@angular/router`)
3. **Implement lazy loading**
4. **Add state management** (NgRx or similar)
5. **Backend integration** for user-specific saves

## Resources

- [Angular Components Guide](https://angular.io/guide/component-overview)
- [Google Identity Services](https://developers.google.com/identity/gsi/web)
- [Angular Standalone Components](https://angular.io/guide/standalone-components)
- [Component Communication](https://angular.io/guide/inputs-outputs)

## Support

For questions about this architecture:
1. Review this document
2. Check the generated component scaffolds
3. Examine `auth.service.ts` for authentication patterns
4. Look at `login.component` for a complete example

---

**Status**: ✅ Authentication complete, 📦 Components scaffolded, 🚧 Migration in progress
