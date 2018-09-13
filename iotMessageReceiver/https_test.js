'use strict';


var utils = require('./src/net.perceptio.heatstore.iot/utilities/utilities');
var fs = require('fs');

var storeDetection = {"id":"0","content":"no hay data"};	


/*
var dirFiles = fs.readdirSync("shared");
console.log(dirFiles.length);
var rnd=Math.floor(Math.random() * dirFiles.length);
console.log(rnd);
console.log(dirFiles[rnd]);*/

/*
var dir = "shared/cam2";
var dirFiles = fs.readdirSync(dir);
console.log(dirFiles.length);
for (let file in dirFiles) {
	var filename = dir+"/"+dirFiles[file];
	fs.unlink(filename, (err) => {
		  if (err) {console.log(err);};
		  console.log(dirFiles[file]+' was deleted');
		});
}*/
/*
var d = new Date();
var seconds = Math.round(d.getTime()/1000);
console.log(seconds);
*/
/*
fs.writeFile("shared/detection.json", JSON.stringify(storeDetection), function(err) {
    if(err) {
        return console.log(err);
    }

    console.log("The file was saved!");
});*/




storeDetection = {
			"id":"1234",
    		"date":"5678",
    		"detections":"detect",
    		"classes":["uno","dos"],
    		"content":"content"};


console.log(storeDetection.classes.length);








