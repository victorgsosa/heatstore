'use strict';

var utils = require('../utilities/utilities');
var amqp = require('amqplib/callback_api');
var msbroker = require('./message_broker');

var amqpConn;
var pubChannel;
var offlinePubQueue;

module.exports = {
	create: function(){
		start();
			
	},
	
publish: function(exchange, routingKey, content) {
	  console.log("publish llamado",exchange, routingKey);
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
	  pubChannel = null;
	  offlinePubQueue = [];
	  startPublisher();
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
