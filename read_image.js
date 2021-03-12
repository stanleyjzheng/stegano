var PNG = require('png-js');

var myimage = new PNG('/mnt/data/local/Stanley/uofthacks/model_image.png');

var width  = myimage.width;
var height = myimage.height;

console.log(width+height)

myimage.decode(function (pixels) {
    //
});



// let x = openFile("https://upload.wikimedia.org/wikipedia/commons/6/6a/512x512-No-Noise.jpg")
// console.log(x)