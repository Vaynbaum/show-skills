import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { EventModel } from '../models/EventModel';
import { ResponseItemsModel } from '../models/ResponseItemsModel';
import { AuthService } from './auth.service';
import { url } from './config';

@Injectable({
  providedIn: 'root',
})
export class EventService {
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

  GetEventsFavorites(): Observable<ResponseItemsModel<EventModel> | null> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .get(`${url}/event/subscription`, {
          headers: { Authorization: `Bearer ${token}` },
          params: {
            next_days: 5,
            limit: 1000000,
          },
        })
        .pipe(catchError(this.handleError))
        .subscribe(
          (response) => {
            observer.next(response as ResponseItemsModel<EventModel>);
          },
          (err) => {
            if (err.status === 401 || err.status === 403) {
              this.authService.RefreshToken();
              this.authService.TokenRefreshed.subscribe(() => {
                token = this.authService.GetAccessToken();
                this.http
                  .get(`${url}/event/subscription`, {
                    headers: { Authorization: `Bearer ${token}` },
                    params: {
                      next_days: 5,
                      limit: 1000000,
                    },
                  })
                  .subscribe(
                    (response) => {
                      observer.next(response as ResponseItemsModel<EventModel>);
                    },
                    (err) => {
                      observer.next(null);
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
