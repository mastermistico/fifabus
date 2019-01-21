import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import { User } from '../models/user';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class AuthService {
  private BASE_URL: string = 'http://localhost:5000/api';
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  constructor(private http: Http) {}
  login(user: any): Promise<any> {
    let url: string = `${this.BASE_URL}/token`;
    let boa = user.username+':'+user.password;
    this.headers.append('Authorization', 'Basic ' +
      	btoa(boa))
	
   	return this.http.get(url,{headers: this.headers}).toPromise();	
  }
  register(user: any): Promise<any> {
    let url: string = `${this.BASE_URL}/users`;
    return this.http.post(url, user, {headers: this.headers}).toPromise();
  }  
}
