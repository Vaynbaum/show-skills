import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { SystemComponent } from './system.component';
import { HomeComponent } from './home/home.component';
import { SystemRoutingModule } from './system-routing.module';
import { HeaderComponent } from './shared/component/header/header.component';
import { FooterComponent } from './shared/component/footer/footer.component';
import { TopicComponent } from './topic/topic.component';
import { ProfileComponent } from './profile/profile.component';
import { LeftComponent } from './shared/component/left/left.component';
import { RightComponent } from './shared/component/right/right.component';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AdminComponent } from './admin/admin.component';
import { ArticleComponent } from './article/article.component';
import { EditComponent } from './edit/edit.component';
import { GuestComponent } from './guest/guest.component';
import { MeetingComponent } from './meeting/meeting.component';
import { SendComponent } from './send/send.component';
import { SubsComponent } from './subs/subs.component';

@NgModule({
  declarations: [
    SystemComponent,
    HomeComponent,
    HeaderComponent,
    FooterComponent,
    TopicComponent,
    ProfileComponent,
    LeftComponent,
    RightComponent,
    SubsComponent,
    MeetingComponent,
    SendComponent,
    AdminComponent,
    GuestComponent,
    EditComponent,
    ArticleComponent,
  ],
  imports: [
    CommonModule,
    SystemRoutingModule,
    ReactiveFormsModule,
    FormsModule,
  ],
})
export class SystemModule {}
