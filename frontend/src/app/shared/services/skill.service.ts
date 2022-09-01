import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ResponseItemsModel } from '../models/ResponseItemsModel';
import { SkillModel } from '../models/SkillModel';
import { AuthService } from './auth.service';
import { url } from './config';

@Injectable({
  providedIn: 'root',
})
export class SkillService {
  constructor(private authService: AuthService, private http: HttpClient) {}

  GetSkills(): Observable<Object> {
    return this.http.get(`${url}/skill/all`, {
      params: {
        limit: 1000000,
      },
    });
  }
}
