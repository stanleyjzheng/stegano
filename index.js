const dcp = require('./dcp_inference');
const fs = require('fs');
console.log('yes');

async function postJob(myMaxRuntime) {
    console.log('yes');
    let PNG = require('pngjs').PNG;
    fs.createReadStream('./test_img.png').pipe(new PNG())
    .on('parsed', async function() {
        width = this.width;
        height = this.height;
        data = this.data;
        x = await dcp.doInference(width, height, data);
        console.log(x);
    });
}

postJob(0.5);
