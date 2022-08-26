import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { SignupModel } from '../../shared/models/SignupModel';
import { AuthService } from 'src/app/shared/services/auth.service';
import { FrontendMessage } from 'src/app/shared/models/FrontendMessage';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css'],
})
export class RegistrationComponent implements OnInit {
  constructor(private router: Router, private authService: AuthService) {}
  message: FrontendMessage = {
    text: '',
    type: '',
  };
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

  inputs = {
    lastname: () => {
      return 'Поле фамилия должно быть заполнено.';
    },
    firstname: () => {
      return 'Имя должно быть заполнено.';
    },
    username: () => {
      return 'Ник должен быть заполнен.';
    },
    email: () => {
      if (this.form?.get?.('email')?.['errors']?.['required']) {
        return 'Email не может быть пустым.';
      }
      if (this.form?.get?.('email')?.['errors']?.['email']) {
        return 'Введите корректный email.';
      }
      if (this.form?.get?.('email')?.['errors']?.['forbiddenEmail']) {
        return 'Email уже занят.';
      }
      return '';
    },
    password: () => {
      if (this.form?.get?.('password')?.['errors']?.['required']) {
        return 'Пароль не может быть пустым.';
      }
      if (
        this.form?.get?.('password')?.['errors']?.['minlength'] &&
        this.form?.get?.('password')?.['errors']?.['minlength'][
          'requiredLength'
        ]
      )
        return `Пароль должен быть больше ${
          this.form.get('password')?.['errors']?.['minlength']?.[
            'requiredLength'
          ]
        } символов. Сейчас ${
          this.form.get('password')?.['errors']?.['minlength']?.['actualLength']
        }.`;
      return '';
    },
  };

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
        this.router.navigate(['/login'], {
          queryParams: {
            canLogin: true,
          },
        });
      },
      (err) => {
        this.showMessage({ text: err, type: 'danger' });
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
