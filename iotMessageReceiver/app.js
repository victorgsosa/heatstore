'use strict';

var http_server = require('./src/net.perceptio.heatstore.iot/http_server/http_server');
var mspublisher = require('./src/net.perceptio.heatstore.iot/message_broker/mspublisher');
var msworker = require('./src/net.perceptio.heatstore.iot/message_broker/msworker');
var cluster = require('cluster');

var queues = [
	{
		"queue":	"COUNTER_IN",
		"workerid":0
	},
	{
		"queue":	"COUNTER_OUT",
		"workerid":0
	},
	{
		"queue":	"CLASSIFICATOR",
		"workerid":0
	},
	{
		"queue":	"LOCATOR",
		"workerid":0
	}
];


if(cluster.isMaster){
	http_server.create();
	mspublisher.create();
	
	for (let elem in queues){
		var worker_env = {};
		worker_env["QUEUE_NAME"] = queues[elem].queue;
		cluster.fork(worker_env);
	}
	cluster.on('online', function(worker) {
        console.log('Worker ' + worker.process.pid + ' is online');
    });

}
else{
	msworker.create();
}
