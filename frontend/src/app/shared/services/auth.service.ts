import { EventEmitter, Injectable, Output } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { url } from './config';
import { SignupModel } from '../models/SignupModel';
import { AuthModel } from '../models/AuthModel';
import { CookieService } from './cookie.service';
import { PairTokensModel } from '../models/PairTokensModel';
import { Router } from '@angular/router';

const KEY_ACCESS_TOKEN = 'access_token';
const KEY_REFRESH_TOKEN = 'refresh_token';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private http: HttpClient,
    private cookieService: CookieService,
    private router: Router
  ) {}
  @Output() TokenRefreshed = new EventEmitter();
  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `,
        error.error
      );
    }
    // Return an observable with a user-facing error message.
    return throwError(error.error.detail);
  }

  Registration(user: SignupModel): Observable<Object> {
    return this.http
      .post(`${url}/auth/signup`, user)
      .pipe(catchError(this.handleError));
  }

  Login(user: AuthModel): Observable<Object> {
    return this.http
      .post(`${url}/auth/login`, user)
      .pipe(catchError(this.handleError));
  }

  RefreshToken() {
    let token = this.cookieService.getCookie(KEY_REFRESH_TOKEN);

    this.http
      .get(`${url}/auth/refresh_token`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .pipe(catchError(this.handleError))
      .subscribe(
        (response) => {
          this.saveAccessToken((response as any).access_token);
          this.TokenRefreshed.emit()
        },
        (err) => {
          this.cookieService.deleteCookie(KEY_ACCESS_TOKEN);
          this.cookieService.deleteCookie(KEY_REFRESH_TOKEN);
          this.router.navigate(['/login'], {
            queryParams: {
              authAgain: true,
            },
          });
        }
      );
  }

  IsAuthenticated() {
    let token = this.cookieService.getCookie(KEY_ACCESS_TOKEN);
    return token!='' ? true : false;
  }

  private saveRefreshToken(token: string) {
    this.cookieService.setCookie({
      name: KEY_REFRESH_TOKEN,
      value: token,
      expireDays: 7,
      secure: true,
    });
  }
  private saveAccessToken(token: string) {
    this.cookieService.setCookie({
      name: KEY_ACCESS_TOKEN,
      value: token,
      expireDays: 1,
      secure: true,
    });
  }
  SaveTokens(pair: PairTokensModel) {
    this.saveAccessToken(pair.access_token);
    this.saveRefreshToken(pair.refresh_token);
  }

  GetAccessToken() {
    return this.cookieService.getCookie(KEY_ACCESS_TOKEN);
  }
}
