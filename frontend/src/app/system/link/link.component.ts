import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FrontendMessage } from 'src/app/shared/models/FrontendMessage';
import { LinkModel } from 'src/app/shared/models/LinkModel';
import { UserAdditionalDataModel } from 'src/app/shared/models/UserAdditionalDataModel';
import { ProfileService } from 'src/app/shared/services/profile.service';
import { UserService } from 'src/app/shared/services/user.service';

@Component({
  selector: 'app-link',
  templateUrl: './link.component.html',
  styleUrls: ['./link.component.css']
})
export class LinkComponent implements OnInit {

  constructor(private router: Router,private profileService: ProfileService, private userService: UserService) { }
  message: FrontendMessage = {
    text: '',
    type: '',
  };
  form: FormGroup = new FormGroup({
    name: new FormControl(null, [Validators.required]),
    url: new FormControl(null, [Validators.required])
  });
  inputs = {
    name: () => {
      return 'Поле название должно быть заполнено.';
    },
    url: () => {
      return 'Поле url должно быть заполнено.';
    }
  }
  ngOnInit(): void {
  }
  onSubmit() {
    const { name, url} = this.form.value;
    const link = new LinkModel(
      name,
      url
    );
    this.userService.AddLink(link).subscribe(
      (response) => {
        this.profileService.UpdateInformation();
        this.router.navigate(['/profile']);
      },
      (err) => {
        this.showMessage({ text: err.error.detail, type: 'danger' });
      }
    );
  }

  private showMessage(message: FrontendMessage) {
    this.message = message;

    window.setTimeout(() => {
      this.message.text = '';
    }, 5000);
  }

}
