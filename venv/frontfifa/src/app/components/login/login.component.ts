import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/user';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string;
  password: string;
  constructor(private router: Router,
  			  private auth: AuthService) {}
  onLogin(): void {
    this.auth.login({'username': this.username, 'password': this.password})
    .then((user) => {
      localStorage.setItem('token', user.json().token);
      this.router.navigate(['/home'])
    })
    .catch((err) => {
      console.log(err);
    });
  }
}
