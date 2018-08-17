var http = require('http');
var amqp = require('amqplib/callback_api');
var URL = require('url');
var htmlEscape = require('sanitizer/sanitizer').escape;
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

'use strict';

function rabbitUrl() {
	  if (process.env.VCAP_SERVICES) {
		console.log("VCAPSERVICES: " + process.env.VCAP_SERVICES);  
	    var svcInfo = JSON.parse(process.env.VCAP_SERVICES);
	    for (var label in svcInfo) {
	      var svcs = svcInfo[label];
	      console.log("label: " + label);
	      for (var index in svcs) {
	        var uri = svcs[index].credentials.uri;
	        console.log("index: " + index);
	        if (uri.lastIndexOf("amqp", 0) == 0) {
	          return uri;
	        }
	      }
	    }
	    return null;
	  }
	  else {
	    return "amqp://localhost";
	  }
	}

var port = process.env.VCAP_APP_PORT || 3000;



//if the connection is closed or fails to be established at all, we will reconnect
var amqpConn = null;
function start() {
  amqp.connect(rabbitUrl() + "?heartbeat=60", function(err, conn) {
    if (err) {
      console.error("[AMQP]", err.message);
      return setTimeout(start, 1000);
    }
    conn.on("error", function(err) {
      if (err.message !== "Connection closing") {
        console.error("[AMQP] conn error", err.message);
      }
    });
    conn.on("close", function() {
      console.error("[AMQP] reconnecting");
      return setTimeout(start, 1000);
    });

    console.log("[AMQP] connected");
    amqpConn = conn;

    whenConnected();
  });
}

var storeDetection;
var storeImage;
function httpServer() {
	  var serv = http.createServer(function(req, res) {
		  res.setHeader("Access-Control-Allow-Headers", "*");
    	  	  res.setHeader("Access-Control-Allow-Origin","*");
    	  	  
	    var url = URL.parse(req.url);
	    if (req.method == 'GET' && url.pathname == '/image') {
	    	console.log("GET: " + url.pathname);
	      
	    	  res.statusCode = 200;
	    	  if(storeImage===undefined){res.write(JSON.stringify({"id":"0","content":"no data"}));}
	    	  else{res.write(JSON.stringify(storeImage));}
	    	  
	      
	      res.end();
	    }
	    else if (req.method == 'GET' && url.pathname == '/detection') {
	    	console.log("GET: " + url.pathname);
		      
	    	  res.statusCode = 200;
	    	  
	    	  if(storeDetection===undefined){res.write(JSON.stringify({"id":"0","content":"no data"}));}
	    	  else{res.write(JSON.stringify(storeDetection));}
	    	  
	      res.end();
	    }
	    else if (req.method == 'POST' && url.pathname == '/') {
	    	console.log("POST: " + url.pathname);  
	    	message = '';
	      req.on('data', function(chunk) { message += chunk; });
	      req.on('end', function() {	    	  	
	        var jsonContent = JSON.parse(message);
	        data = [];
	        for (let elem in jsonContent.messages) {
	        		image = { "id": guid(),
	        		"date":jsonContent.messages[elem].timestamp,
	        		"content":jsonContent.messages[elem].image };
	        		data.push(image);
	        		
	        		storeImage = image;
	        		
	        }
	        //storeImage = data;
	        jsonData = JSON.stringify(data) 
	        console.log("Imagen recibida por POST y enviada a Cola "+ jsonData);
	        publish("", "image_queue", new Buffer(jsonData));
	        res.statusCode = 200;
	        res.setHeader('Location', '/');
	        openHtml(res);
		    writeMessages(res);
		    closeHtml(res);
	        res.end();
	      });
	    }
	    else {
	    	console.log("ERRO: " + "Petición errónea");
	      res.statusCode = 400;
	      res.end("Petición errónea");
	    }
	  });
	  serv.listen(port);
	}



console.log("Starting ... Service URL: " + rabbitUrl());
start()
httpServer();

//---- helpers

function openHtml(res) {
  res.write("<html><body>");
}

function closeHtml(res) {
  res.end("</body></html>");
}

function writeMessages(res) {
  res.write('<p>Mensaje recibido y entregado a Rabbit</p>');
}


function guid() {
	  function s4() {
	    return Math.floor((1 + Math.random()) * 0x10000)
	      .toString(16)
	      .substring(1);
	  }
	  return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
	}

function whenConnected() {
	  startPublisher();
	  startWorker();
	}


var pubChannel = null;
var offlinePubQueue = [];
function startPublisher() {
  amqpConn.createConfirmChannel(function(err, ch) {
    if (closeOnErr(err)) return;
    ch.on("error", function(err) {
      console.error("[AMQP] channel error", err.message);
    });
    ch.on("close", function() {
      console.log("[AMQP] channel closed");
    });

    pubChannel = ch;
    while (true) {
      var m = offlinePubQueue.shift();
      if (!m) break;
      publish(m[0], m[1], m[2]);
    }
  });
}

function publish(exchange, routingKey, content) {
	  try {
	    pubChannel.publish(exchange, routingKey, content, { persistent: true },
	                      function(err, ok) {
	                        if (err) {
	                          console.error("[AMQP] publish", err);
	                          offlinePubQueue.push([exchange, routingKey, content]);
	                          pubChannel.connection.close();
	                        }
	                      });
	  } catch (e) {
	    console.error("[AMQP] publish", e.message);
	    offlinePubQueue.push([exchange, routingKey, content]);
	  }
	}

function closeOnErr(err) {
	  if (!err) return false;
	  console.error("[AMQP] error", err);
	  amqpConn.close();
	  return true;
	}

//A worker that acks messages only if processed succesfully
function startWorker() {
  amqpConn.createChannel(function(err, ch) {
    if (closeOnErr(err)) return;
    ch.on("error", function(err) {
      console.error("[AMQP] channel error Worker", err.message);
    });
    ch.on("close", function() {
      console.log("[AMQP] channel closed Worker");
    });
    ch.prefetch(1);
    ch.assertExchange('locations', 'fanout', {durable: false});
//    ch.assertQueue("image_queue", { durable: true }, function(err, _ok) {
    	ch.assertQueue('', { exclusive: true }, function(err, _ok) {
      if (closeOnErr(err)) return;
//      ch.consume("image_queue", processMsg, { noAck: false });
      ch.bindQueue(_ok.queue, 'locations', '');
      ch.consume(_ok.queue, processMsg, { noAck: true });
      console.log("Image Worker is started");
    });
    
    function processMsg(msg) {
        work(msg, function(ok) {
          try {
            if (ok)
              ch.ack(msg);
            else
              ch.reject(msg, true);
          } catch (e) {
            closeOnErr(e);
          }
        });
      }
    
    });
  }


function work(msg, cb) {
	  console.log("Got Location QUEUE Message: ", msg.content.toString());
	  
	  
	  var jsonLocation = JSON.parse(msg.content.toString());
      var detection;
	  for (let elem in jsonLocation) {
    	  		detection = {
      		"date":jsonLocation[elem].date,
      		"detections":jsonLocation[elem].detections };
    	  		
    	  		storeDetection = {
    	  				"id":jsonLocation[elem].id,
    	  	      		"date":jsonLocation[elem].date,
    	  	      		"detections":jsonLocation[elem].detections, 
    	  	      		"content":jsonLocation[elem].content};
      		
      		jsonData = JSON.stringify(detection) 
      		sendLocation(jsonData);
	        console.log("Location enviado "+ jsonData);
      		
      }
      //cb(true);
	  
	  
	}

function sendLocation(jsonData){
	var xhr = new XMLHttpRequest();
	xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
	  if (this.readyState === 4) {
	    console.log(this.responseText);
	  }

	});

	xhr.open("POST", "https://heatstoreapis0018881710trial.hanatrial.ondemand.com/heatstore-api/image-api/image");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.setRequestHeader("Cache-Control", "no-cache");
	xhr.send(jsonData);
}




