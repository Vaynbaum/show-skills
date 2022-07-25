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
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

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
  ],
  imports: [
    CommonModule,
    SystemRoutingModule,
    ReactiveFormsModule,
    FormsModule,
  ],
})
export class SystemModule {}
