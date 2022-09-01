import { DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { EventModel, Offline, Online } from 'src/app/shared/models/EventModel';
import { ProfileService } from 'src/app/shared/services/profile.service';

@Component({
  selector: 'app-meeting',
  templateUrl: './meeting.component.html',
  styleUrls: ['./meeting.component.css'],
})
export class MeetingComponent implements OnInit {
  constructor(private profileService: ProfileService, public datepipe: DatePipe) {}
  events: EventModel[] = [];
  srcOnline = '../../../../../assets/images/online.png';
  srcOffline = '../../../../../assets/images/offline.png';
  selectSrc(format: string) {
    if (format === Online) {
      return this.srcOnline;
    } else if (format === Offline) return this.srcOffline;
    else return '';
  }

  formatData(numb: number) {
    return this.datepipe.transform(numb, 'yyyy/MM/dd')
  }
  ngOnInit(): void {
    this.events = this.profileService.Events;
    this.profileService.eventInfoUpdated.subscribe(() => {
      this.events = this.profileService.Events;
    });
  }
}
