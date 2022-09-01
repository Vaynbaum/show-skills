import { DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { LinkModel } from 'src/app/shared/models/LinkModel';
import { RoleModel } from 'src/app/shared/models/RoleModel';
import { ShortUserResponseModel } from 'src/app/shared/models/ShortUserResponseModel';
import { SkillModel } from 'src/app/shared/models/SkillModel';
import { SubscribeModel } from 'src/app/shared/models/SubscribeModel';
import { UserModel } from 'src/app/shared/models/UserModel';
import { ProfileService } from 'src/app/shared/services/profile.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  constructor(private profileService: ProfileService, public datepipe: DatePipe) { }

  user: UserModel|null = null;
  date: string|null ='';
  links: LinkModel[] = [];
  formatData(numb: number|undefined) {
    return this.datepipe.transform(numb, 'yyyy/MM/dd')
  }

  ngOnInit(): void {
    this.user=this.profileService.User;
    this.profileService.userInfoUpdated.subscribe(() => {
      this.user=this.profileService.User;
    });
  }
}
