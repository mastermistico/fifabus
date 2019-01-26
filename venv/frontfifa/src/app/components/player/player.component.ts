import { Component, OnInit } from '@angular/core';
import { xhr } from '../../models/send';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit {

  constructor(private router: Router,
  			  private auth: AuthService) { }
  nameTeam: string
  name: string
  last: string
  position: string
  shirt: number
  photo: any
  dateB: any
  titular: any
  listTit: any = [{'name':true},{'name':false}]

  onPhotoSelected(event){
  	this.photo = <File>event.target.files[0]
  }

  onPlay(){

  	xhr('POST','api/players',{'x-access-token': localStorage.getItem('token'),
  											'Accept': 'application/json'}, {
  											'nombreEquipo': this.nameTeam,
  											'nombre': this.name,
  											'apellido': this.last,
  											'posicion': this.position,
  											'camiseta': this.shirt,
  											'nacimiento': this.dateB,
  											'titular': this.titular
  											}, [this.photo])
  	.then((res) => {
  		console.log(res)
  		this.cleanPlayer()
  	})
  	.catch((err) =>{
  		console.log(err);
  	})
  }

  onCoach(){

  	this.router.navigate(['/coach'])

  }

  cleanPlayer(){
  	this.name = null
  	this.last = null
  	this.position = null
  	this.shirt = null
  	this.photo = null
  	this.dateB = null
  	this.titular = null
  }

  ngOnInit() {
  	this.cleanPlayer()
  }

}
