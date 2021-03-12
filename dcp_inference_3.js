SCHEDULER  = 'https://scheduler.distributed.computer'
process.argv.push('--scheduler', SCHEDULER);
require('dcp-client').initSync(process.argv);

const compute = require('dcp/compute');
const dcpCli = require('dcp/dcp-cli');


doInference = async function(width, height, data) {
    progress(0);
    require("onnxjs-node");
    const np = require("ndarray")
    const ops = require("ndarray-ops")

    const session = new onnx.InferenceSession();
    const url = "https://github.com/stanleyjzheng/stegano/raw/master/final_b1.onnx";
    session.loadModel(url);

    const dataTensor = np(new Float32Array(data), [width, height, 4]);
    const dataProcessedTensor = np(new Float32Array(width * height * 3), [1, 3, width, height]);
    ops.assign(dataProcessedTensor.pick(0, 0, null, null), dataTensor.pick(null, null, 0));
    ops.assign(dataProcessedTensor.pick(0, 1, null, null), dataTensor.pick(null, null, 1));
    ops.assign(dataProcessedTensor.pick(0, 2, null, null), dataTensor.pick(null, null, 2));
    ops.divseq(dataProcessedTensor, 255);
    progress();
    ops.subseq(dataProcessedTensor.pick(0, 0, null, null), 0.485);
    ops.subseq(dataProcessedTensor.pick(0, 1, null, null), 0.456);
    ops.subseq(dataProcessedTensor.pick(0, 2, null, null), 0.406);
    ops.divseq(dataProcessedTensor.pick(0, 0, null, null), 0.229);
    ops.divseq(dataProcessedTensor.pick(0, 1, null, null), 0.224);
    ops.divseq(dataProcessedTensor.pick(0, 2, null, null), 0.225);

    const tensor = new onnx.Tensor(new Float32Array(width * height * 3), 'float32', [1, 3, width, height]);
    (tensor.data).set(dataProcessedTensor.data);
    progress();
    const outputMap = await session.run([tensor]);
    progress(1.0);
    return outputMap;
};

async function postJob(myMaxRuntime) {
    let myKeystore = await dcpCli.getAccountKeystore();

    var fs = require('fs'),
    PNG = require('pngjs').PNG;
    fs.createReadStream('/mnt/data/local/Stanley/uofthacks/testimg.png').pipe(new PNG())
    .on('parsed', async function() {
        width = this.width
        height = this.height
        data = this.data
        job = await compute.for(width, height, data, doInference);
        let myTimer = setTimeout(function(){
            job.cancel();
            console.log('Job reached ' + myMaxRuntime + ' minutes.');
        }, myMaxRuntime * 60 * 1000);
    
        job.public.name = 'Stegano inference';
        job.requires(['pngjs', 'onnxjs-node', 'ndarray', 'ndarray-ops']);
    
        job.on('accepted', () => {
            console.log('Job accepted: ' + job.id);
        });
        job.on('status', (status) => {
            console.log('STATUS:');
            console.log(
                status.total + ' slices posted, ' +
                status.distributed + ' slices distributed, ' +
                status.computed + ' slices computed.'
            );
        });
        job.on('result', (thisOutput) => {
            console.log('RESULT:');
            console.log(thisOutput.result);
        });
    
        try {
            await job.exec(compute.marketValue, myKeystore);
        } catch (myError) {
            console.log('Job halted.');
        }
    
        clearTimeout(myTimer);
    
        return(inference);
    });
}

postJob(0.5)