import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SubscribeModel } from 'src/app/shared/models/SubscribeModel';
import { UserModel } from 'src/app/shared/models/UserModel';
import { ProfileService } from 'src/app/shared/services/profile.service';

@Component({
  selector: 'app-left',
  templateUrl: './left.component.html',
  styleUrls: ['./left.component.css'],
})
export class LeftComponent implements OnInit {
  constructor(private profileService: ProfileService, private router: Router) {}
  user: UserModel | null = null;
  subs: SubscribeModel[] =[];
  // subs: SubscribeModel[]|undefined =[];
  ngOnInit(): void {
    this.user = this.profileService.User;
    this.profileService.userInfoUpdated.subscribe(() => {
      this.user = this.profileService.User;
      if (this.user?.subscriptions) {
        this.subs = []
        for (let i = 0; i < 10; i++) {
          if (this.user?.subscriptions[i]==undefined){
            break;
          }
          this.subs[i]=this.user?.subscriptions[i];
        }
      }
    });
  }
  goToPerson(username:any){
    this.router.navigate(['/guest'], {
      queryParams: {
        username: username,
      },
    });
  }
}
