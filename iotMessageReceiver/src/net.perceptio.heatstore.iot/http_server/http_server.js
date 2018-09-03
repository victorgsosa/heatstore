'use strict';

var http = require('http');
var URL = require('url');
var htmlEscape = require('sanitizer/sanitizer').escape;
var httpRequestHandler = require('./httpRequestHandler');

module.exports = {
create: function() { 
	
	  //var port = process.env.VCAP_APP_PORT || 8081;
	var port = process.env.VCAP_APP_PORT || 3000;
	  var serv = http.createServer(function(req, res) {
		  res.setHeader("Access-Control-Allow-Headers", "*");
	  	  res.setHeader("Access-Control-Allow-Origin","*");
	  	  
	    var url = URL.parse(req.url);
	    var action;
		console.log(req.method + ": " + url.pathname);	    	
	    	action = req.method.toLowerCase() + url.pathname;
	    action =	action.replace('/','_');
	    	console.log("ACTION: " + action);
	    if (req.method == 'GET') {
		    	try{
		    		res.statusCode = httpRequestHandler[action](req,res);
		    		res.end();
		    	}catch(err){
		    		console.log("ERROR: " + err.name +" Message: "+err.message);
		    		res.statusCode = 200;
		    		res.end("success");
		    	}
		    	
		    	 
		    
	    }else if (req.method == 'POST' ) { 
	    	var message = '';
	      req.on('data', function(chunk) { message += chunk;});
	      req.on('end', function() {	
			    	  
	    	  		try{
				    		var statusCode = httpRequestHandler[action](req,res,message);
				    		res.statusCode = 200;
				    		res.end();
				    	}catch(err){
				    		console.log("ERROR: " + err.name +" Message: "+err.message);
				    		res.statusCode = 502;
				    		res.end("Bad endpoint");
				    	}
	    	  
	      });    
	    }
	    else {
	    	console.log("ERRO: " + "Petición errónea");
	      res.statusCode = 400;
	      res.end("Petición errónea");
	    }
	  });
	  serv.listen(port);
	  console.log("Listening server port "+port);
	}
}