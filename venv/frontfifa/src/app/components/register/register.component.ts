import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { User } from '../../models/user';

@Component({
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  user: User = new User();
  constructor(private router: Router,
  			  private auth: AuthService) {}
  onRegister(): void {
    this.auth.register(this.user)
    .then((user) => {
      console.log(user.json());
      this.router.navigate(['/login'])
    })
    .catch((err) => {
      console.log(err);
    });
  }
}
