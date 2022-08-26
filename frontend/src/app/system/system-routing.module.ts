import {NgModule} from '@angular/core';
import {Router, RouterModule, Routes} from '@angular/router';
import { AdminComponent } from './admin/admin.component';
import { ArticleComponent } from './article/article.component';
import { EditComponent } from './edit/edit.component';
import { GuestComponent } from './guest/guest.component';
import { HomeComponent } from './home/home.component';
import { MeetingComponent } from './meeting/meeting.component';
import { ProfileComponent } from './profile/profile.component';
import { SendComponent } from './send/send.component';
import { SubsComponent } from './subs/subs.component';
import { SystemComponent } from './system.component';
import { TopicComponent } from './topic/topic.component';

const routes: Routes = [
  {path: '', component: SystemComponent, children: [
      {path:'home', component: HomeComponent},
      {path:'topic', component: TopicComponent},
      {path:'profile', component: ProfileComponent},
      {path:'subs', component: SubsComponent},
      {path:'meeting', component: MeetingComponent},
      {path:'send', component: SendComponent},
      {path:'article', component: ArticleComponent},
      {path:'guest', component: GuestComponent},
      {path:'edit', component: EditComponent},
      {path:'admin', component: AdminComponent}
  ] }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SystemRoutingModule { }
