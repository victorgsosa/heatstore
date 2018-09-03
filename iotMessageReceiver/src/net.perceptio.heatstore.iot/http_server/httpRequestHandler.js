'use strict';

var utils = require('../utilities/utilities');
var mspublisher = require('../message_broker/mspublisher');
var devices = require('../device/device');
var Device = devices.Device;
var fs = require('fs');



var storedImage;
var storedDetection;

module.exports={
	
	get_image: function(req,res){
	  console.log("GET_IMAGE");
	      
  	  if(storedImage===undefined){res.write(JSON.stringify({"id":"0","content":"no data"}));}
  	  else{res.write(JSON.stringify(storedImage));}
  	  
  	return 200;
	},
	
	get_detection: function(req,res){
	 console.log("GET_DETECTION");
	 var path="shared/detection.json";
	   if(fs.existsSync(path)){
		   res.write(fs.readFileSync(path));
	   }else{
		   res.write(JSON.stringify({"id":"0","content":"no data"}));
	   }   
  	 
  	  //if(storedDetection===undefined){res.write(JSON.stringify({"id":"0","content":"no data"}));}
  	  //else{res.write(JSON.stringify(storedDetection));}
  	  //res.write(JSON.stringify(utils.detection));
  	  
  	  
  	return 200;
	},
	
	get_health: function(req,res){
		return 200;
	},
	
	post_iotmms: function(req,res,message){
		var image;
    		var data;
    		console.log("POST_IOTMMS");
    		var jsonContent = JSON.parse(message);    
        data = [];
        for (let elem in jsonContent.messages) {
        		image = { 
        		"camera": jsonContent.device,
        		"id": utils.guid(),
        		"date":jsonContent.messages[elem].timestamp,
        		"content":jsonContent.messages[elem].image };
        		data.push(image);
        		storedImage = image;	        		
        }
        res.statusCode = 200;
        var jsonData = JSON.stringify(data) ;
        console.log("HTTP Handler PID: "+process.pid);
        console.log("Imagen recibida por POST y enviada a Rabbit. Camara: "+ jsonContent.device);
        mspublisher.publish("", "images", new Buffer(jsonData));
        return 200;	      
	}
  
	
};