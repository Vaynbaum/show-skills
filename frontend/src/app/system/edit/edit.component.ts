import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FrontendMessage } from 'src/app/shared/models/FrontendMessage';
import { UserAdditionalDataModel } from 'src/app/shared/models/UserAdditionalDataModel';
import { ProfileService } from 'src/app/shared/services/profile.service';
import { UserService } from 'src/app/shared/services/user.service';

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css', '../../../assets/styles/alert.css']
})
export class EditComponent implements OnInit {

  constructor(private router: Router,private profileService: ProfileService, private userService: UserService) { }
  message: FrontendMessage = {
    text: '',
    type: '',
  };
  form: FormGroup = new FormGroup({
    place_residence: new FormControl(null, [Validators.required]),
    birth_date: new FormControl(null, [Validators.required])
  });
  inputs = {
    place_residence: () => {
      return 'Поле город должно быть заполнено.';
    },
    birth_date: () => {
      return 'Дата рождения должна быть заполнена.';
    }
  }
  ngOnInit(): void {
  }
  onSubmit() {
    const { place_residence, birth_date} = this.form.value;
    const user = new UserAdditionalDataModel(
      new Date(birth_date).getTime(),
      place_residence
    );
    this.userService.Add(user).subscribe(
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
