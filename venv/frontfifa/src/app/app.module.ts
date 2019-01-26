import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { AuthService } from './services/auth.service';
import { RegisterComponent } from './components/register/register.component';
import { HomeComponent } from './components/home/home.component';
import { PlayerComponent } from './components/player/player.component';
import { CoachComponent } from './components/coach/coach.component';
import { DashComponent } from './components/dash/dash.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    PlayerComponent,
    CoachComponent,
    DashComponent,
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,    
    RouterModule.forRoot([
  		{ path: 'login', component: LoginComponent },
  		{ path: 'register', component: RegisterComponent },
  		{ path: 'home', component: HomeComponent},
  		{ path: 'player', component: PlayerComponent},
  		{ path: 'coach', component: CoachComponent},
  		{ path: 'dash', component: DashComponent}
    ])
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})

export class AppModule { }
