import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LogModule } from './log/log.module';
import { SystemModule } from './system/system.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    LogModule,
    AppRoutingModule,
    SystemModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
