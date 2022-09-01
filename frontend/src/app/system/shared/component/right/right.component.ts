import { Component, OnInit } from '@angular/core';
import { EventModel, Offline, Online } from 'src/app/shared/models/EventModel';
import { ProfileService } from 'src/app/shared/services/profile.service';

@Component({
  selector: 'app-right',
  templateUrl: './right.component.html',
  styleUrls: ['./right.component.css'],
})
export class RightComponent implements OnInit {
  constructor(private profileService: ProfileService) {}
  offCount: number = 0;
  onCount: number = 0;
  ngOnInit(): void {
    this.countEventsFormat();
    this.profileService.eventInfoUpdated.subscribe(() => {
      this.countEventsFormat();
    });
  }
  countEventsFormat() {
    this.offCount = 0;
    this.onCount = 0;
    this.profileService.Events.forEach((event) => {
      if (event.format_event === Offline) this.offCount++;
      else if (event.format_event === Online) this.onCount++;
    });
  }
}
