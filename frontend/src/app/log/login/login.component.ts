import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { AuthModel } from 'src/app/shared/models/AuthModel';
import { FrontendMessage } from 'src/app/shared/models/FrontendMessage';
import { PairTokensModel } from 'src/app/shared/models/PairTokensModel';
import { AuthService } from 'src/app/shared/services/auth.service';
import { CookieService } from 'src/app/shared/services/cookie.service';
import { ProfileService } from 'src/app/shared/services/profile.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css', '../../../assets/styles/alert.css'],
})
export class LoginComponent implements OnInit {
  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private profileService: ProfileService,
    private authService: AuthService
  ) {}
  message: FrontendMessage = {
    text: '',
    type: '',
  };

  ngOnInit(): void {
    this.route.queryParams.subscribe((params: Params) => {
      if (params['authAgain']) {
        this.showMessage({
          text: 'Необходимо снова авторизоваться',
          type: 'warning',
        });
      } else if (params['canLogin']) {
        this.showMessage({
          text: 'Теперь вы можете зайти в систему',
          type: 'success',
        });
      } else if (params['deleteUser']) {
        this.showMessage({
          text: 'Ваш аккаунт успешно удалён',
          type: 'success',
        });
      } else if (params['accessDenied']) {
        this.showMessage({
          text: 'Авторизуйтесь чтобы попасть в систему',
          type: 'warning',
        });
      }
    });
  }
  form: FormGroup = new FormGroup({
    email: new FormControl(null, [Validators.required, Validators.email]),
    password: new FormControl(null, [
      Validators.required,
      Validators.minLength(8),
    ]),
  });

  inputs = {
    email: () => {
      if (this.form?.get?.('email')?.['errors']?.['required']) {
        return 'Email не может быть пустым.';
      }
      if (this.form?.get?.('email')?.['errors']?.['email']) {
        return 'Введите корректный email.';
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

  onSubmit() {
    const { email, password } = this.form.value;
    const user = new AuthModel(email, password);
    this.authService.Login(user).subscribe(
      (response) => {
        let pair = new PairTokensModel(
          (response as PairTokensModel).access_token,
          (response as PairTokensModel).refresh_token
        );
        this.authService.SaveTokens(pair);

        this.profileService.UpdateInformation();
        this.router.navigate(['./home']);
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
