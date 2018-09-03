'use strict';


var utils = require('./src/net.perceptio.heatstore.iot/utilities/utilities');
var fs = require('fs');

var storeDetection = {"id":"0","content":"no hay data"};	
	  		


fs.writeFile("shared/detection.json", JSON.stringify(storeDetection), function(err) {
    if(err) {
        return console.log(err);
    }

    console.log("The file was saved!");
});