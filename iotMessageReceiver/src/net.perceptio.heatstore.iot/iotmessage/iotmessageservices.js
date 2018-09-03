'use strict';

var XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;
var routes = require('../utilities/routes');
var fs = require('fs');

module.exports={
	
	map_locator: function(jsondata){
		var detection;
		var storeDetection;
		
		for (let elem in jsondata) {
  	  		detection = {
  	  	"camera":jsondata[elem].camera,			
    		"date":jsondata[elem].date,
    		"detections":jsondata[elem].detections };

  	  		
  	  	storeDetection = {
	  				"id":jsondata[elem].id,
	  	      		"date":jsondata[elem].date,
	  	      		"detections":jsondata[elem].detections, 
	  	      		"content":jsondata[elem].content};	
  	  		  		
		}
		
		fs.writeFile("shared/detection.json", JSON.stringify(storeDetection), function(err) {
	  	      if(err) {
	  	          return console.log(err);
	  	      }
	
	  	      console.log("The file was saved!");
	  	  });
		
		
		return detection;
	},
	
	map_post: function(jsondata){
		console.log("Llamado a MAP_POST");
		var map;
		for (let elem in jsondata) {
  	  		map = {
  	  	"camera":jsondata[elem].camera,			
    		"date":jsondata[elem].date
  	  		};  		
		}
		return map;
	},
	
	put_counter_in: function(post_response,jsondata){
		var counter_in;
		var image_id;
		for (let elem in post_response) {
  	  			image_id = post_response[elem].id;
  	  		}
		if(image_id = null){return null;}	
		
		for (let elem in jsondata) {
  	  		counter_in = {
  	  			"images"	:[{"id":image_id}],
  	  			"embeddings": jsondata[elem].embeddings
  	  			};
  	  		}
		return counter_in;
		
	},
	
	put_counter_out: function(){},
	
	put_classificator: function(post_response,jsondata){
		var classificator;
		var image_id=post_response.id;
		var secuence;
		var embeddings=[];
		var classes=[];
		var iotservice = this;
		console.log("EN PUT_CLASSIFICATOR");
		
		for (let elem in jsondata) {
			for (let embed in jsondata[elem].embeddings) {
				embeddings=[];
				secuence = 1;
				for (let embedval in jsondata[elem].embeddings[embed] ) {
					var data={
							"sequence":secuence,
							"value":jsondata[elem].embeddings[embed][embedval]
					}
					embeddings.push(data);
					secuence++;
				}
				classificator = {
			  			"images"	:[{"id":image_id}],
			  			"embeddings": embeddings,
			  			"classifiers":[ {"name": "gender",
			  				"value":jsondata[elem].classes[embed].gender
			  				}]
			  			};
				iotservice["put"](classificator);
			}	
		}
	},
	
	post: function(postdata, queue,jsondata){		
		console.log("Llamado POST a API: ",JSON.stringify(postdata))
		var iotservice = this;
		
		var xhr = new XMLHttpRequest();
		xhr.withCredentials = true;		
		xhr.addEventListener("readystatechange", function () {
		  if (this.readyState === 4) {
			  console.log("Response POST recibido");
			  	console.log(this.responseText);
			    
			    if(queue=="COUNTER_IN"||queue=="CLASSIFICATOR"){
				    	var action = "put_"+queue.toLowerCase();
				    	iotservice[action](JSON.parse(this.responseText),jsondata);
				}
		  }

		});	
		console.log("POST abierto para URL", routes.post);
		xhr.open("POST", routes.post);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.setRequestHeader("Cache-Control", "no-cache");
		xhr.send(JSON.stringify(postdata));
		console.log("JSON enviado");
	},
	
	
	
	put: function(jsondata){		
		console.log("Llamado PUT a API: ",JSON.stringify(jsondata))
		var xhr = new XMLHttpRequest();
		xhr.withCredentials = true;		
		xhr.addEventListener("readystatechange", function () {
		  if (this.readyState === 4) {
			  console.log("Response PUT recibido");
			    console.log(this.responseText);
		  }

		});		
		xhr.open("PUT", routes.put);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.setRequestHeader("Cache-Control", "no-cache");
		xhr.send(JSON.stringify(jsondata));
	}
	
}