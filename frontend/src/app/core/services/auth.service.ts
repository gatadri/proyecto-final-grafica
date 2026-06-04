import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthResponse, NinoLoginResponse, User, Nino } from '../models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = environment.apiUrl;

  private userSubject = new BehaviorSubject<User | null>(this.loadUser());
  private ninoSubject = new BehaviorSubject<Nino | null>(this.loadNino());

  user$ = this.userSubject.asObservable();
  nino$ = this.ninoSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) {}

  login(email: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, { email, password }).pipe(
      tap(res => {
        localStorage.setItem('token', res.token);
        localStorage.setItem('user', JSON.stringify(res.user));
        this.userSubject.next(res.user);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.userSubject.next(null);
    this.router.navigate(['/auth/login']);
  }

  ninoLogin(nombre: string, pin: string): Observable<NinoLoginResponse> {
    return this.http.post<NinoLoginResponse>(`${this.apiUrl}/nino/login`, { nombre, pin }).pipe(
      tap(res => {
        // Limpiar sesión de usuario anterior si existe
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        this.userSubject.next(null);
        
        localStorage.setItem('nino', JSON.stringify(res.nino));
        this.ninoSubject.next(res.nino);
      })
    );
  }

  ninoLogout(): void {
    localStorage.removeItem('nino');
    this.ninoSubject.next(null);
    this.router.navigate(['/auth/nino-login']);
  }

  getToken(): string | null { return localStorage.getItem('token'); }
  getUser(): User | null    { return this.userSubject.value; }
  getNino(): Nino | null    { return this.ninoSubject.value; }
  isLoggedIn(): boolean     { return !!this.getToken(); }
  isNinoLoggedIn(): boolean { return !!this.getNino(); }
  getRole(): string | null  { return this.getUser()?.role ?? null; }

  saveNino(nino: Nino): void {
    localStorage.setItem('nino', JSON.stringify(nino));
    this.ninoSubject.next(nino);
  }

  redirectByRole(): void {
    const role = this.getRole();
    if (role) this.router.navigate([`/${role}/dashboard`]);
  }

  private loadUser(): User | null {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) : null;
  }

  private loadNino(): Nino | null {
    const raw = localStorage.getItem('nino');
    return raw ? JSON.parse(raw) : null;
  }
}
