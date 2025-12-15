# Google Authentication Setup Guide

## Quick Start

The Fantasy Inn Tycoon now supports Google Sign-In! Follow these steps to configure it.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Fantasy Inn Tycoon" (or your preferred name)
4. Click "Create"

## Step 2: Enable Google Identity Services

1. In your project, go to **APIs & Services** → **Library**
2. Search for "Google Identity Services API" or "Google+ API"
3. Click and enable it

## Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen first:
   - User Type: **External**
   - App name: **Fantasy Inn Tycoon**
   - User support email: *your email*
   - Developer contact: *your email*
   - Save and continue through the scopes (no changes needed)
   - Add test users if needed
   - Save and continue

4. Back to Create OAuth client ID:
   - Application type: **Web application**
   - Name: **Fantasy Inn Web Client**
   - Authorized JavaScript origins:
     - `http://localhost:4200` (for development)
     - `http://localhost:3000` (if using different port)
     - `https://your-domain.com` (for production)
   - Authorized redirect URIs:
     - `http://localhost:4200` (for development)
     - `https://your-domain.com` (for production)

5. Click **CREATE**

6. **IMPORTANT**: Copy your Client ID (it looks like: `123456789-abc123.apps.googleusercontent.com`)

## Step 4: Configure the Application

1. Open `frontend/src/app/core/auth/login/login.component.ts`

2. Find this line:
```typescript
private readonly GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com';
```

3. Replace it with your actual Client ID:
```typescript
private readonly GOOGLE_CLIENT_ID = '123456789-abc123.apps.googleusercontent.com';
```

4. Save the file

## Step 5: Test It!

1. **Start the development server**:
```bash
cd frontend
npm start
```

2. **Open your browser** to `http://localhost:4200`

3. **You should see**:
   - Fantasy Inn Tycoon login screen
   - Google Sign-In button
   - "Continue as Guest" button

4. **Try Guest Mode**:
   - Click "Continue as Guest"
   - Game should load immediately
   - Your progress saves locally

5. **Try Google Sign-In**:
   - Click the Google button
   - Sign in with your Google account
   - Game should load with your Google profile picture and name

## Troubleshooting

### "Popup closed by user" error
- Make sure your Client ID is correctly configured
- Check that your domain is in "Authorized JavaScript origins"
- Disable popup blockers for localhost

### "Invalid Client ID" error
- Double-check you copied the entire Client ID
- Make sure there are no extra spaces
- Verify the Client ID in Google Cloud Console

### "Origin not allowed" error
- Add your origin to "Authorized JavaScript origins"
- Make sure it matches exactly (http vs https, port number)
- Wait a few minutes for changes to propagate

### Button doesn't appear
- Check browser console for errors
- Verify the Google script is loading (Network tab)
- Try clearing cache and hard reload

## Development vs Production

### Development
```typescript
// Use localhost origins
Authorized JavaScript origins:
- http://localhost:4200
```

### Production
```typescript
// Use your actual domain
Authorized JavaScript origins:
- https://fantasy-inn.yourdomain.com

// Update Client ID or use environment variables
environment.googleClientId = 'PROD_CLIENT_ID';
```

## Security Best Practices

1. **Never commit your Client ID** to public repositories
   - Use environment variables
   - Add to `.gitignore` if using config files

2. **Restrict domains** in production
   - Only allow your actual domain
   - Remove localhost origins in production credentials

3. **Use different credentials** for dev vs prod
   - Create separate OAuth clients
   - Different Client IDs for different environments

## Environment Variables (Recommended)

Create `frontend/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  googleClientId: '123456789-abc123.apps.googleusercontent.com'
};
```

Create `frontend/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  googleClientId: 'PRODUCTION_CLIENT_ID.apps.googleusercontent.com'
};
```

Update `login.component.ts`:

```typescript
import { environment } from '../../../environments/environment';

// ...
private readonly GOOGLE_CLIENT_ID = environment.googleClientId;
```

## Guest Mode

Users can always play without signing in:
- Click "Continue as Guest"
- Progress saves to localStorage
- No cloud sync
- Perfect for quick play or privacy-conscious users

## Features

✅ **Implemented**:
- Google Sign-In with profile picture
- Guest mode (no authentication required)
- Persistent sessions (localStorage)
- Sign out functionality
- User display in header

🚧 **Future Enhancements**:
- Backend user sync
- Cloud save games
- Multiple device sync
- User preferences storage

## Need Help?

- [Google Identity Services Documentation](https://developers.google.com/identity/gsi/web/guides/overview)
- [OAuth 2.0 for Web Apps](https://developers.google.com/identity/protocols/oauth2/web-server)
- Check the browser console for error messages
- Verify all steps were completed correctly

---

**Note**: The Google Client ID in the code is a placeholder. You MUST replace it with your own Client ID for Google Sign-In to work.
