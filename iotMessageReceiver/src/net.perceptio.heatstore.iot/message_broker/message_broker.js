'use strict';

var amqp = require('amqplib/callback_api');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var pubChannel;
var offlinePubQueue;
var amqpConn;


module.exports = {

	create: function(){
		start();
	},
	
publish: function(exchange, routingKey, content) {
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
}

function start(){
	amqpConn = null;
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

function rabbitUrl() {
	  if (process.env.VCAP_SERVICES) {
//		console.log("VCAPSERVICES: " + process.env.VCAP_SERVICES);  
	    var svcInfo = JSON.parse(process.env.VCAP_SERVICES);
	    for (var label in svcInfo) {
	      var svcs = svcInfo[label];
	      for (var index in svcs) {
	        var uri = svcs[index].credentials.uri;
	        if (uri.lastIndexOf("amqp", 0) == 0) {
	          return uri;
	        }
	      }
	    }
	    return null;
	  }
	  else {
	    //return "amqp://localhost";
	    return "amqp://guest:guest@rabbitmq-service.heatstore:5672"
	  }
	}

function whenConnected() {
	  pubChannel = null;
	  offlinePubQueue = [];
	  startPublisher();
	  startWorker();
	}


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

