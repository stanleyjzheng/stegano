require("onnxjs-node");
const np = require("ndarray")
const ops = require("ndarray-ops")

const session = new onnx.InferenceSession();

const url = "./final_b1.onnx";
session.loadModel(url);

let image = "image.png"
//imageData = loadImage(image);
// idk you can do some magic
// here, we need to do read the image in a format that is convertible to this numpy format. Float32Array.

const { data, width, height } = imageData;

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



//const outputMap = await session.run(inputs);
//const outputTensor = outputMap.values().next().value;