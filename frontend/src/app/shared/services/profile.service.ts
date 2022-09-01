import { HttpErrorResponse } from '@angular/common/http';
import { EventEmitter, Injectable, Output } from '@angular/core';
import { throwError } from 'rxjs';
import { EventModel } from '../models/EventModel';
import { UserModel } from '../models/UserModel';
import { AuthService } from './auth.service';
import { EventService } from './event.service';
import { UserService } from './user.service';

@Injectable({
  providedIn: 'root',
})
export class ProfileService {
  public User: UserModel | null = null;
  public Events: EventModel[] = [];
  @Output() userInfoUpdated: EventEmitter<any> = new EventEmitter();
  @Output() eventInfoUpdated: EventEmitter<any> = new EventEmitter();
  constructor(
    private authService: AuthService,
    private userService: UserService,
    private eventService: EventService,
  ) {}
  
  UpdateInformation() {
    this.userService.GetFullInformationAuthUser().subscribe((result) => {
      this.User = result;
      this.userInfoUpdated.emit();
    });
    this.eventService.GetEventsFavorites().subscribe((result) => {
      this.Events = result ? result.items : [];
      this.eventInfoUpdated.emit();
    });
  }
}
