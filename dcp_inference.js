SCHEDULER  = 'https://scheduler.distributed.computer'
process.argv.push('--scheduler', SCHEDULER);
require('dcp-client').initSync(process.argv);

const compute = require('dcp/compute');
const dcpCli = require('dcp/dcp-cli');
const onnx = require('onnxjs-node');
const session = new onnx.InferenceSession();
//const url = "https://github.com/stanleyjzheng/stegano/raw/master/final_b1.onnx";
const url = './final_b1.onnx';
console.log(session);
session.loadModel(url);
const np = require("ndarray");
const ops = require("ndarray-ops");

module.exports = {
    // doInference = async function(width, height, data) {
    //     require("onnxjs-node");
    //     const np = require("ndarray")
    //     const ops = require("ndarray-ops")

    //     const session = new onnx.InferenceSession();
    //     const url = "https://github.com/stanleyjzheng/stegano/raw/master/final_b1.onnx";
    //     session.loadModel(url);

    //     const dataTensor = np(new Float32Array(data), [width, height, 4]);
    //     const dataProcessedTensor = np(new Float32Array(width * height * 3), [1, 3, width, height]);
    //     ops.assign(dataProcessedTensor.pick(0, 0, null, null), dataTensor.pick(null, null, 0));
    //     ops.assign(dataProcessedTensor.pick(0, 1, null, null), dataTensor.pick(null, null, 1));
    //     ops.assign(dataProcessedTensor.pick(0, 2, null, null), dataTensor.pick(null, null, 2));
    //     ops.divseq(dataProcessedTensor, 255);
    //     ops.subseq(dataProcessedTensor.pick(0, 0, null, null), 0.485);
    //     ops.subseq(dataProcessedTensor.pick(0, 1, null, null), 0.456);
    //     ops.subseq(dataProcessedTensor.pick(0, 2, null, null), 0.406);
    //     ops.divseq(dataProcessedTensor.pick(0, 0, null, null), 0.229);
    //     ops.divseq(dataProcessedTensor.pick(0, 1, null, null), 0.224);
    //     ops.divseq(dataProcessedTensor.pick(0, 2, null, null), 0.225);

    //     const tensor = new onnx.Tensor(new Float32Array(width * height * 3), 'float32', [1, 3, width, height]);
    //     (tensor.data).set(dataProcessedTensor.data);
    //     const outputMap = await session.run([tensor]);
    //     return outputMap;
    // };
    //require("onnxjs-node");
    //const session = new onnx.InferenceSession();
    ////const url = "https://github.com/stanleyjzheng/stegano/raw/master/final_b1.onnx";
    //const url = "./final_b1.onnx" console.log(session) session.loadModel(url);


    async doInference(width, height, data) {
        const dataTensor = np(new Float32Array(data), [width, height, 4]);
        const dataProcessedTensor = np(new Float32Array(width * height * 3), [1, 3, width, height]);
        ops.assign(dataProcessedTensor.pick(0, 0, null, null), dataTensor.pick(null, null, 0));
        ops.assign(dataProcessedTensor.pick(0, 1, null, null), dataTensor.pick(null, null, 1));
        ops.assign(dataProcessedTensor.pick(0, 2, null, null), dataTensor.pick(null, null, 2));
        ops.divseq(dataProcessedTensor, 255);
        ops.subseq(dataProcessedTensor.pick(0, 0, null, null), 0.485);
        ops.subseq(dataProcessedTensor.pick(0, 1, null, null), 0.456);
        ops.subseq(dataProcessedTensor.pick(0, 2, null, null), 0.406);
        ops.divseq(dataProcessedTensor.pick(0, 0, null, null), 0.229);
        ops.divseq(dataProcessedTensor.pick(0, 1, null, null), 0.224);
        ops.divseq(dataProcessedTensor.pick(0, 2, null, null), 0.225);
        const tensor = new onnx.Tensor(new Float32Array(width * height * 3), 'float32', [1, 3, width, height]);
        (tensor.data).set(dataProcessedTensor.data);
        const outputMap = await session.run([tensor]);
        return outputMap
    }
};
