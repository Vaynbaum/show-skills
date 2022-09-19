import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ShortUserResponseModel } from 'src/app/shared/models/ShortUserResponseModel';
import { SubscribeModel } from 'src/app/shared/models/SubscribeModel';
import { UserModel } from 'src/app/shared/models/UserModel';
import { ProfileService } from 'src/app/shared/services/profile.service';

@Component({
  selector: 'app-subs',
  templateUrl: './subs.component.html',
  styleUrls: ['./subs.component.css']
})
export class SubsComponent implements OnInit {

  constructor(private profileService: ProfileService,private router: Router) { }
  user: UserModel|null = null;
  // subs: SubscribeModel[]|undefined =[];
  ngOnInit(): void {
    this.user=this.profileService.User;
    this.profileService.userInfoUpdated.subscribe(() => {
      this.user=this.profileService.User;
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
