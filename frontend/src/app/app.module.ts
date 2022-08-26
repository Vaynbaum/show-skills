import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LogModule } from './log/log.module';
import { AuthService } from './shared/services/auth.service';
import { CookieService } from './shared/services/cookie.service';
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
  providers: [AuthService, CookieService],
  bootstrap: [AppComponent],
})
export class AppModule {}
