import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CKEditorModule } from 'ng2-ckeditor';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TestEditorComponent } from './test-editor/test-editor.component';

@NgModule({
  declarations: [
    AppComponent,
    TestEditorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    CKEditorModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
