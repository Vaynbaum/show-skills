import { Component, OnInit } from '@angular/core';
import { ProfileService } from './shared/services/profile.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = 'project';
  constructor(private profileService: ProfileService) {}
  ngOnInit(): void {
    this.profileService.UpdateInformation();
  }
}
