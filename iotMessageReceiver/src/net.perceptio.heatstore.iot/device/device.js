'use strict';

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

function Device(id){
	this.id = id;
	this.height = 0;
	this.focalLength = 0;
	this.aDistance = 0;
	this.aX = 0;
	this.aY=0;
	this.bDistance=0;
	this.bX=0;
	this.bY=0;
	this.cDistance=0;
	this.cX=0;
	this.cY=0;
	this.roles=[];
	
	getProperties(this);
}

function getProperties(device){
	var xhr = new XMLHttpRequest();
	var urlDevApi = "https://heatstoreapis0018881710trial.hanatrial.ondemand.com/heatstore-api/cameras/"+device.id
	//console.log("Camera properties: "+urlDevApi);
	xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
	  if (this.readyState === 4) {
	    console.log("API Response: "+this.responseText);
	  }

	});

	xhr.open("GET", urlDevApi);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.setRequestHeader("Cache-Control", "no-cache");
	xhr.send();
}

module.exports={
		Device: Device
}

