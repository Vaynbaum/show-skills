import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { SignupModel } from '../../shared/models/SignupModel';
import { AuthService } from 'src/app/shared/services/auth.service';
import { HttpErrorResponse } from '@angular/common/http';
@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css'],
})
export class RegistrationComponent implements OnInit {
  constructor(private router: Router, private authService: AuthService) {}
  msg = '';
  form: FormGroup = new FormGroup({
    email: new FormControl(null, [Validators.required, Validators.email]),
    username: new FormControl(null, [Validators.required]),
    lastname: new FormControl(null, [Validators.required]),
    firstname: new FormControl(null, [Validators.required]),
    password: new FormControl(null, [
      Validators.required,
      Validators.minLength(8),
    ]),
  });
  ngOnInit(): void {}

  onSubmit() {
    const { email, lastname, firstname, username, password } = this.form.value;
    const user = new SignupModel(
      email,
      password,
      lastname,
      firstname,
      username
    );

    this.authService.Registration(user).subscribe(
      (response) => {
        console.log(response);
      },
      (err) => {
        this.msg = err;
        console.log(err);
      }
    );
  }
}
