'use strict';

var utils = require('../utilities/utilities');
var amqp = require('amqplib/callback_api');
const Iotmessage = require('../iotmessage/iotmessage');

var amqpConn;

module.exports = {

		create: function(){
			start();
		}
}

function start(){
	amqpConn = null;
	amqp.connect(utils.rabbitUrl() + "?heartbeat=60", function(err, conn) {
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


function whenConnected() {
	  startWorker();
	}

function closeOnErr(err) {
	  if (!err) return false;
	  console.error("[AMQP] error", err);
	  amqpConn.close();
	  start();
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
    ch.assertExchange(process.env["QUEUE_NAME"], 'fanout', {durable: false});
    	ch.assertQueue('', { exclusive: true }, function(err, _ok) {
      if (closeOnErr(err)) return;
      ch.bindQueue(_ok.queue, process.env["QUEUE_NAME"], '');
      ch.consume(_ok.queue, processMsg, { noAck: true });
      console.log("Image Worker is started for: "+process.env["QUEUE_NAME"]);
    });
    
    function processMsg(msg) {
        work(msg, function(ok) {
          try {
            if (ok)
              ch.ack(msg);
            else
              ch.reject(msg, true);
          } catch (e) {
           // closeOnErr(e);
            console.error("[AMQP] error", e);
          }
        });
      }
    
    });
  }


function work(msg, cb) {
//	  console.log("Got Location QUEUE Message for: "+process.env["QUEUE_NAME"]);
	  var iotmessage = new Iotmessage(msg.content.toString());
	  iotmessage.map(process.env["QUEUE_NAME"]);
	  //iotmessage.map("LOCATOR");
	  iotmessage.post();
		  
	  
	/*  var jsonLocation = JSON.parse();
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
    		
    }*/
	}



