'use strict';

var services=require('./iotmessageservices');
var XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;
var routes = require('../utilities/routes');

class Iotmessage{
	
	constructor(jdata){
//		console.log("Creando iotmessage");
		this.jsondata = JSON.parse(jdata);
		this.iotmsg="";
		this.queue=""
	}
	
	map(queue_name){
		this.queue=queue_name;
//		console.log("Mapeando iotmessage");
		var action;
		if(this.queue=="COUNTER_IN"|this.queue=="CLASSIFICATOR"){
			action = "map_post"
		}else
		{
			action = "map_"+queue_name.toLowerCase();
		}
		
		this.iotmsg=services[action](this.jsondata);
//		console.log("Llamado a action",action);
//		console.log("Queue map name: ",this.queue);
	}
	
	post(){		
		services["post"](this.iotmsg,this.queue,this.jsondata);
	}
}

module.exports = Iotmessage;