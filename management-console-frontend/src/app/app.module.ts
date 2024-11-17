import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { LogListComponent } from './log-list/log-list.component';
import { LogFormComponent } from './log-form/log-form.component';

const routes: Routes = [
  { path: '', redirectTo: '/logs', pathMatch: 'full' },
  { path: 'logs', component: LogListComponent },
  { path: 'add-log', component: LogFormComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    LogListComponent,
    LogFormComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }