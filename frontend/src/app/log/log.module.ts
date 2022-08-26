import { NgModule } from '@angular/core';
import { LogComponent } from './log.component';
import { LogRoutingModule } from './log-routing.module';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

@NgModule({
  declarations: [LogComponent, LoginComponent, RegistrationComponent],
  imports: [CommonModule, LogRoutingModule, ReactiveFormsModule, FormsModule],
})
export class LogModule {}
