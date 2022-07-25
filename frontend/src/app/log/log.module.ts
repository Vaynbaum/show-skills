import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { LogComponent } from './log.component';
import { LogRoutingModule } from './log-routing.module';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';

@NgModule({
  declarations: [
    LogComponent,
    LoginComponent,
    RegistrationComponent
  ],
  imports: [
    BrowserModule,
    LogRoutingModule
 ],
})

export class LogModule { }
