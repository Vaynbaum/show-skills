import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';
import { AuthService } from './auth.service';
import { url } from './config';
import axios from 'axios';
import { UnloadContentModel } from '../models/ContentUnloadModel';
import { UnloadPostModel } from '../models/UnloadPostModel';
import { PostModel } from '../models/PostModel';
@Injectable({
  providedIn: 'root',
})
export class PostService {
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

  UnloadImage(image: any): Observable<string | null> {
    let token = this.authService.GetAccessToken();
    let formData: FormData = new FormData();
    formData.append('file', image);
    return new Observable((observer) => {
      axios
        .post(`${url}/post/upload/image`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${token}`,
            accept: 'application/json',
          },
        })
        .then((value) => {
          observer.next(value.data as string);
        })
        .catch((error) => {
          if (error.status === 401 || error.status === 403) {
            this.authService.RefreshToken();
            this.authService.TokenRefreshed.subscribe(() => {
              token = this.authService.GetAccessToken();
              axios
                .post(`${url}/post/upload/image`, formData, {
                  headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer ${token}`,
                    accept: 'application/json',
                  },
                })
                .then((value) => {
                  observer.next(value.data as string);
                });
            });
          }
          observer.error(error);
        });
    });
  }

  UnloadPost(post: UnloadPostModel): Observable<PostModel | null> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .post(`${url}/post/create`, post, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .pipe(catchError(this.handleError))
        .subscribe(
          (response) => {
            observer.next(response as PostModel);
          },
          (err) => {
            if (err.status === 401 || err.status === 403) {
              this.authService.RefreshToken();
              this.authService.TokenRefreshed.subscribe(() => {
                token = this.authService.GetAccessToken();
                this.http
                  .post(`${url}/post/create`, {
                    headers: { Authorization: `Bearer ${token}` },
                    post,
                  })
                  .subscribe(
                    (response) => {
                      observer.next(response as PostModel);
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

  UnloadContent(data: UnloadContentModel): Observable<string | null> {
    let token = this.authService.GetAccessToken();
    return new Observable((observer) => {
      this.http
        .post(`${url}/post/upload/content`, data, {
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
                  .post(`${url}/post/upload/content`, data, {
                    headers: { Authorization: `Bearer ${token}` },
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

  GetAllPosts(): Observable<Object> {
    return this.http.get(`${url}/post/all`, {
      params: {
        limit: 1000000,
      },
    });
  }

  GetPostsBySkill(skill: string) {
    return this.http.get(`${url}/post/by_skill`, {
      params: {
        name_skill: skill,
        limit: 1000000,
      },
    });
  }

  GetContentByName(name: string) {
    return this.http.get(`${url}/post/content/${name}`);
  }
}
