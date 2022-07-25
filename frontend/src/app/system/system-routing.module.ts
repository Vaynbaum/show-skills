import {NgModule} from '@angular/core';
import {Router, RouterModule, Routes} from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { SystemComponent } from './system.component';
import { TopicComponent } from './topic/topic.component';

const routes: Routes = [
  {path: '', component: SystemComponent, children: [
      {path:'home', component: HomeComponent},
      {path:'topic', component: TopicComponent},
      {path:'profile', component: ProfileComponent}
  ] }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SystemRoutingModule { }
