import { DatePipe } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LogModule } from './log/log.module';
import { AuthService } from './shared/services/auth.service';
import { CookieService } from './shared/services/cookie.service';
import { EventService } from './shared/services/event.service';
import { FavoriteService } from './shared/services/favorite.service';
import { PostService } from './shared/services/post.service';
import { ProfileService } from './shared/services/profile.service';
import { SkillService } from './shared/services/skill.service';
import { SubscribesService } from './shared/services/subscribes.service';
import { UserService } from './shared/services/user.service';
import { SystemModule } from './system/system.module';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    LogModule,
    HttpClientModule,
    LogModule,
    AppRoutingModule,
    SystemModule,
  ],
  providers: [
    AuthService,
    CookieService,
    ProfileService,
    UserService,
    FavoriteService,
    EventService,
    SkillService,
    SubscribesService,
    PostService,
    DatePipe,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
