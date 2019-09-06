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
//	  console.log("GET_IMAGE");
	      
  	  if(storedImage===undefined){res.write(JSON.stringify({"id":"0","content":"no data"}));}
  	  else{res.write(JSON.stringify(storedImage));}
  	  
  	return 200;
	},
	
	get_detection: function(req,res){
//	 console.log("GET_DETECTION");
	 var path="shared/detection.json";
	   if(fs.existsSync(path)){
		   res.write(fs.readFileSync(path));
	   }else{
		   res.write(JSON.stringify({"id":"0","content":"no data"}));
	   }     	  
  	return 200;
	},
	
	get_detectioncam1: function(req,res){
//	 console.log("GET_DETECTION CAM 1");
	 var path="shared/detectioncam1.json";
	   if(fs.existsSync(path)){
		   res.write(fs.readFileSync(path));
	   }else{
		   res.write(JSON.stringify({"id":"0","content":"no data"}));
	   }     	  
	 return 200;
	},
	
	get_detectioncam2: function(req,res){
	// console.log("GET_DETECTION CAM 2");
	 //var path="shared/detectioncam2.json";
	 var dir = "shared/cam2";
	 var dirFiles = fs.readdirSync(dir);
	 var rnd=Math.floor(Math.random() * dirFiles.length);
	 var path=dir+"/"+dirFiles[rnd];
	  if(fs.existsSync(path)){
		   res.write(fs.readFileSync(path));
	   }else{
		   res.write(JSON.stringify({"id":"0","content":"no data"}));
	   }     	  
	 return 200;
	},
	
	get_detectioncam3: function(req,res){
//	 console.log("GET_DETECTION CAM 3");
	 //var path="shared/detectioncam3.json";
	 var dir = "shared/cam3";
	 var dirFiles = fs.readdirSync(dir);
	 var rnd=Math.floor(Math.random() * dirFiles.length);
	 var path=dir+"/"+dirFiles[rnd];
	   if(fs.existsSync(path)){
		   res.write(fs.readFileSync(path));
	   }else{
		   res.write(JSON.stringify({"id":"0","content":"no data"}));
	   }     	  
	 return 200;
	},
	
	get_detectionhermeco: function(req,res){
	//	 console.log("GET_DETECTION CAM HERMECO");
		 var dir = "shared/hermeco";
		 var dirFiles = fs.readdirSync(dir);
		 var rnd=Math.floor(Math.random() * dirFiles.length);
		 var path=dir+"/"+dirFiles[rnd];
		   if(fs.existsSync(path)){
			   res.write(fs.readFileSync(path));
		   }else{
			   res.write(JSON.stringify({"id":"0","content":"no data"}));
		   }     	  
		 return 200;
	},
	
	get_delcam2: function(req,res){
		var dir = "shared/cam2";
		var dirFiles = fs.readdirSync(dir);
	//	console.log(dirFiles.length);
		for (let file in dirFiles) {
			var filename = dir+"/"+dirFiles[file];
			fs.unlink(filename, (err) => {
				  if (err) {console.log(err);};
				  console.log(dirFiles[file]+' was deleted');
				});
		}
		return 200;
	},
	
	get_delcam3: function(req,res){
		var dir = "shared/cam3";
		var dirFiles = fs.readdirSync(dir);
		//console.log(dirFiles.length);
		for (let file in dirFiles) {
			var filename = dir+"/"+dirFiles[file];
			fs.unlink(filename, (err) => {
				  if (err) {console.log(err);};
				  console.log(dirFiles[file]+' was deleted');
				});
		}
		return 200;
	},
	
	get_delhermeco: function(req,res){
		var dir = "shared/hermeco";
		var dirFiles = fs.readdirSync(dir);
		//console.log(dirFiles.length);
		for (let file in dirFiles) {
			var filename = dir+"/"+dirFiles[file];
			fs.unlink(filename, (err) => {
				  if (err) {console.log(err);};
				  console.log(dirFiles[file]+' was deleted');
				});
		}
		return 200;
	},
	
	get_health: function(req,res){
		return 200;
	},
	
	post_iotmms: function(req,res,message){
		var image;
    		var data;
    		var d = new Date();
    		var seconds = d.getTime();
    		//console.log("POST_IOTMMS");
    		var jsonContent = JSON.parse(message);    
        data = [];
        for (let elem in jsonContent.messages) {
        		image = { 
        		"camera": jsonContent.device,
        		"id": utils.guid(),
        		"date":seconds,
        		"content":jsonContent.messages[elem].image };
        		data.push(image);
        		storedImage = image;	        		
        }
        res.statusCode = 200;
        var jsonData = JSON.stringify(data) ;
        //console.log("PRE VIDEO MESSAGE: "+message);
        //console.log("HTTP Handler PID: "+process.pid);
       // console.log("Imagen recibida por POST y enviada a Rabbit. Camara: "+ jsonContent.device);
        //console.log("POST VIDEO MESSAGE: "+jsonData);
        mspublisher.publish("", "images", new Buffer(jsonData));
        return 200;	      
	}
  
	
};