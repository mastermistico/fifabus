import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class AuthService {
  private BASE_URL: string = 'api';
  private headers: Headers = new Headers({'Content-Type': 'application/json'				  
  										  });
  constructor(private http: Http) {
  	  this.headers.append('Access-Control-Allow-Origin', 'http://localhost:5000');
  	  this.headers.append('Access-Control-Allow-Credentials', 'true');
  	  //this.headers.append('GET', 'POST', 'OPTIONS');
  }

  login(user: any): Promise<any> {
    console.log({'user':user})
    let url: string = `${this.BASE_URL}/login`;	
   	return this.http.post(url, user, {headers: this.headers}).toPromise();	
  }
  register(user: any): Promise<any> {
    let url: string = `${this.BASE_URL}/users`;
    return this.http.post(url, user, {headers: this.headers}).toPromise();
  }
  country(): Promise<any>{
  	let url: string = `${this.BASE_URL}/country`;
  	return this.http.get(url, {headers: this.headers}).toPromise();
  }
  couch(couch: any): Promise<any>{
  	let url: string = `${this.BASE_URL}/coachs`;
  	this.headers.append('x-access-token',localStorage.getItem('token'))
  	return this.http.post(url, couch, {headers: this.headers}).toPromise();
  }
}
