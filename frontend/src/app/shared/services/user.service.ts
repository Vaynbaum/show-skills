import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { LinkModel } from '../models/LinkModel';
import { UserAdditionalDataModel } from '../models/UserAdditionalDataModel';
import { UserModel } from '../models/UserModel';
import { AuthService } from './auth.service';
import { url } from './config';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor(private authService: AuthService, private http: HttpClient) {}
  private handleError(error: HttpErrorResponse) {
    if (error.status === 0)
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    // The backend returned an unsuccessful response code.
    // The response body may contain clues as to what went wrong.
    else
      console.error(
        `Backend returned code ${error.status}, body was: `,
        error.error
      );
    // Return an observable with a user-facing error message.
    return throwError(error);
  }

  GetFullInformationAuthUser(): Observable<UserModel | null> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .get(`${url}/user/my`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .pipe(catchError(this.handleError))
        .subscribe(
          (response) => {
            observer.next(response as UserModel);
          },
          (err) => {
            if (err.status === 401 || err.status === 403) {
              this.authService.RefreshToken();
              this.authService.TokenRefreshed.subscribe(() => {
                token = this.authService.GetAccessToken();
                this.http
                  .get(`${url}/user/my`, {
                    headers: { Authorization: `Bearer ${token}` },
                  })
                  .subscribe(
                    (response) => {
                      observer.next(response as UserModel);
                    },
                    (err) => {
                      observer.next(null);
                    }
                  );
                this.authService.TokenRefreshed.unsubscribe();
              });
            }
            observer.next(null);
          }
        );
    });
  }
  GetUserByUsername(username: string) {
    console.log(username);
    return this.http.get(`${url}/user/profile/${username}`);
  }

  Add(user: UserAdditionalDataModel): Observable<string> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .put(`${url}/user/additional_data`, user, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .pipe(catchError(this.handleError))
        .subscribe(
          (response) => {
            observer.next(response as string);
          },
          (err) => {
            if (err.status === 401 || err.status === 403) {
              this.authService.RefreshToken();
              this.authService.TokenRefreshed.subscribe(() => {
                token = this.authService.GetAccessToken();
                this.http
                  .put(`${url}/user/additional_data`, user, {
                    headers: { Authorization: `Bearer ${token}` },
                  })
                  .subscribe(
                    (response) => {
                      observer.next(response as string);
                    },
                    (err) => {
                      observer.error(err as string);
                    }
                  );
                this.authService.TokenRefreshed.unsubscribe();
              });
            }
            observer.error(err.error.detail as string);
          }
        );
    });
  }
  UnloadSub(username: string): Observable<string> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .post(`${url}/subscription/arrange`, {},{
          headers: { Authorization: `Bearer ${token}` },
          params: { username_favorite: username },
        })
        .pipe(catchError(this.handleError))
        .subscribe(
          (response) => {
            observer.next(response as string);
          },
          (err) => {
            if (err.status === 401 || err.status === 403) {
              this.authService.RefreshToken();
              this.authService.TokenRefreshed.subscribe(() => {
                token = this.authService.GetAccessToken();
                this.http
                .post(`${url}/subscription/arrange`, {},{
                  headers: { Authorization: `Bearer ${token}` },
                  params: { username_favorite: username },
                })
                  .subscribe(
                    (response) => {
                      observer.next(response as string);
                    },
                    (err) => {
                      observer.error(err.error.detail);
                    }
                  );
              });
            }
            observer.error(err.error.detail);
          }
        );
    });
  }
  AddLink(link: LinkModel): Observable<LinkModel> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .post(`${url}/link/add`, link, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .pipe(catchError(this.handleError))
        .subscribe(
          (response) => {
            observer.next(response as LinkModel);
          },
          (err) => {
            if (err.status === 401 || err.status === 403) {
              this.authService.RefreshToken();
              this.authService.TokenRefreshed.subscribe(() => {
                token = this.authService.GetAccessToken();
                this.http
                  .post(`${url}/link/add`, link, {
                    headers: { Authorization: `Bearer ${token}` },
                  })
                  .subscribe(
                    (response) => {
                      observer.next(response as LinkModel);
                    },
                    (err) => {
                      observer.error(err.error.detail);
                    }
                  );
              });
            }
            observer.error(err.error.detail);
          }
        );
    });
  }
  DeleateSub(username: string): Observable<string> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .delete(`${url}/subscription/annul`, {
          headers: { Authorization: `Bearer ${token}` },
          params: { username_favorite: username },
        })
        .pipe(catchError(this.handleError))
        .subscribe(
          (response) => {
            observer.next(response as string);
          },
          (err) => {
            if (err.status === 401 || err.status === 403) {
              this.authService.RefreshToken();
              this.authService.TokenRefreshed.subscribe(() => {
                token = this.authService.GetAccessToken();
                this.http
                  .delete(`${url}/subscription/annul`, {
                    headers: { Authorization: `Bearer ${token}` },
                    params: { username_favorite: username },
                  })
                  .subscribe(
                    (response) => {
                      observer.next(response as string);
                    },
                    (err) => {
                      observer.error(err.error.detail);
                    }
                  );
              });
            }
            observer.error(err.error.detail);
          }
        );
    });
  }
}
