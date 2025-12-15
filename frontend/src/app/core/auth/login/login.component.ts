import { Component, OnInit, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit, AfterViewInit {
  @ViewChild('googleButton') googleButton!: ElementRef;

  // TODO: Replace with your actual Google Client ID
  // Get this from: https://console.cloud.google.com/apis/credentials
  private readonly GOOGLE_CLIENT_ID = '600142170034-84c58rijt63ujplcdea50meb5pv5j427.apps.googleusercontent.com';

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    // Load Google Identity Services script
    this.loadGoogleScript();
  }

  ngAfterViewInit(): void {
    // Initialize Google Sign-In after view is ready
    setTimeout(() => {
      this.authService.initializeGoogleSignIn(this.GOOGLE_CLIENT_ID);
      if (this.googleButton) {
        this.authService.renderGoogleButton(this.googleButton.nativeElement);
      }
    }, 100);
  }

  private loadGoogleScript(): void {
    if (document.getElementById('google-signin-script')) {
      return; // Already loaded
    }

    const script = document.createElement('script');
    script.id = 'google-signin-script';
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }

  continueAsGuest(): void {
    this.authService.continueAsGuest();
  }
}
