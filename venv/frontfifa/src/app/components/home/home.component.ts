import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { xhr } from '../../models/send';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router,
  			  private auth: AuthService) { }
  name: string
  country: string
  flag: File = null
  shield: File = null
  listCountry: any = []

  onFlagSelected(event){
  	this.flag = <File>event.target.files[0]
  }

  onShieldSelected(event){
  	this.shield = <File>event.target.files[0]
  	console.log('shield',event)
  }

  getCountry(){
  	this.auth.country().then((country) => {
  		this.listCountry = JSON.parse(country._body)
  	})
  	.catch((err) => {
  		console.log(err);
  	})
  }

  onTeam(){
  	const fd = new FormData();
  	fd.append('bandera', this.flag, this.flag.name)
  	fd.append('nombre', this.name)
  	fd.append('pais', this.country)
  	xhr('POST','api/teams',{'x-access-token': localStorage.getItem('token'),
  											'Accept': 'application/json'}, {
  											'nombre': this.name,
  											'pais': this.country}, [this.flag,this.shield])
  	.then((res) => {
  		console.log(res)
  		this.router.navigate(['/player'])
  	})
  	.catch((err) =>{
  		console.log(err);
  	})
  }

  ngOnInit() {
  	this.getCountry()
  }

}
