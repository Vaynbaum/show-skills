import {NgModule} from '@angular/core';
import {Router, RouterModule, Routes} from '@angular/router';
import { LogComponent } from './log.component';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';

const routes: Routes = [
  {path: '', component: LogComponent, children: [
    {path:'login', component: LoginComponent},
    {path:'registration', component: RegistrationComponent}
  ] }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LogRoutingModule { }
