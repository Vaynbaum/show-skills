import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { UserModel } from 'src/app/shared/models/UserModel';
import { SubscribeModel } from 'src/app/shared/models/SubscribeModel';
import { ProfileService } from 'src/app/shared/services/profile.service';
import { elementAt } from 'rxjs';
import { UserService } from 'src/app/shared/services/user.service';

@Component({
  selector: 'app-guest',
  templateUrl: './guest.component.html',
  styleUrls: ['./guest.component.css'],
})
export class GuestComponent implements OnInit {
  username = '';
  sUser: UserModel | null = null;
  user: UserModel | null = null;
  subs: SubscribeModel[] | undefined;
  bool: Boolean = false;
  constructor(
    private profileService: ProfileService,
    private userService: UserService,
    private route: ActivatedRoute
  ) {}
  ngOnInit(): void {
    this.route.queryParams.subscribe((params: Params) => {
      this.username = params['username'];
      console.log(this.username);
    });
    let element = <HTMLInputElement>document.getElementById('is3dCheckBox');
    this.bool = element.checked;

    this.user = this.profileService.User;
    this.userService.GetUserByUsername(this.username).subscribe((response) => {
      console.log(response);
      this.sUser = response as UserModel;
      console.log(this.sUser?.email);
    });

    if (this.user?.subscriptions) {
      let l = this.user?.subscriptions.length;
      for (let i = 0; i < l; i++) {
        if (this.user?.subscriptions == undefined) {
          break;
        } else if (
          this.user.subscriptions[i].favorite.username == this.username
        ) {
          element.checked = true;
          break;
        }
      }
    }
    this.subs = this.user?.subscriptions;
    this.profileService.userInfoUpdated.subscribe(() => {
      this.user = this.profileService.User;
      this.userService.GetUserByUsername(this.username).subscribe((result) => {
        this.sUser = result ? (result as UserModel) : null;
      });
      // this.sUser=this.profileService.SUser;
      console.log(this.sUser);
      if (this.user?.subscriptions) {
        let l = this.user?.subscriptions.length;
        for (let i = 0; i < l; i++) {
          if (this.user?.subscriptions == undefined) {
            break;
          } else if (
            this.user.subscriptions[i].favorite.username == this.username
          ) {
            element.checked = true;
            break;
          }
        }
      }
    });
  }
  update() {
    var element = <HTMLInputElement>document.getElementById('is3dCheckBox');
    if (element.checked == true) {
      this.userService.UnloadSub(this.username).subscribe((result) => {
        this.profileService.UpdateInformation();
      });
    } else {
      this.userService.DeleateSub(this.username).subscribe((result) => {
        this.profileService.UpdateInformation();
      });
    }
  }
}
