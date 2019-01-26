import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-coach',
  templateUrl: './coach.component.html',
  styleUrls: ['./coach.component.css']
})


export class CoachComponent implements OnInit {

  constructor(private router: Router,
  			  private auth: AuthService) { }
  nameTeam: string
  name: string
  last: string
  dateB: any
  role: any
  country: any
  listCountry: any = []
  listRole: any = [{'name':'tecnico'},{'name':'asistente'},{'name':'medico'},{'name':'preparador'}]

  onCoach(): void {
    this.auth.couch({'nombreEquipo': this.nameTeam,
    					'nombre': this.name,
    					'apellido': this.last,
    					'nacionalidad': this.country,
    					'nacimiento': this.dateB,
    					'rol': this.role})
    .then((user) => {
      console.log(user.json());
       	this.nameTeam = null
		this.name = null
		this.last = null
		this.country = null
		this.dateB = null
		this.role = null
    })
    .catch((err) => {
      console.log(err);
    });
  }

  getCountry(){
  	this.auth.country().then((country) => {
  		this.listCountry = JSON.parse(country._body)
  	})
  	.catch((err) => {
  		console.log(err);
  	})
  }

  onShow(){
  	this.router.navigate(['/dash'])

  }

  ngOnInit() {
  	this.getCountry()
  }

}
