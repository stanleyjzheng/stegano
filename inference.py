import albumentations as albu
import torch
import timm
from torch import nn
from albumentations.pytorch.transforms import ToTensorV2
import cv2
import numpy as np
from PIL import Image
import stegano
from stegano.lsbset import generators

class Alaska_Efficientnet(torch.nn.Module):
    def __init__(self, model_name='efficientnet_b0', out_dim=4, pretrained=False, pool=True):
        super().__init__()
        self.model = timm.create_model(model_name, pretrained=pretrained)
        n_features = self.model.classifier.in_features
        self.pool = pool

        if self.pool:
            self.model.classifier.global_pool = nn.Identity()
            self.model.classifier.fc = nn.Identity()
            self.pooling = nn.AdaptiveAvgPool2d(1)
            self.fc = nn.Linear(n_features, out_dim, bias=True)
        else:
            self.model.classifier = nn.Linear(n_features, out_dim, bias=True)

    def forward(self, x):
        features = self.model(x)

        if self.pool:
            bs = x.size(0)
            pooled_features = self.pooling(features).view(bs, -1)
            features = self.fc(pooled_features)
        return features

def cache_model():
    torch.backends.cudnn.benchmark = True
    net = Alaska_Efficientnet(model_name="efficientnet_b0", pool=False, pretrained=False).cuda()
    checkpoint = torch.load('../input/eb1-weights/best-checkpoint-045epoch_dell.bin')
    net.load_state_dict(checkpoint['model_state_dict']);
    return net.eval()

# https://stackoverflow.com/questions/32213893/how-to-cache-a-large-machine-learning-model-in-flask
def infer(filepath):
    augs = albu.Compose([
        albu.resize(height=512, width=512, p=1.0),
        ToTensorV2(p=1.0),
    ], p=1.0)

    net = cache_model()

    img = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLORBGR2RGB.astype(np.float32))
    img = augs(**{'image': img})['image']

    y_pred = net(img.cuda())
    y_pred = 1 - nn.functional.softmax(y_pred, dim=1).data.cpu().numpy()[:, 0]

    return y_pred

def encode_steno(message, src_path, dest_path):
    img = cv2.imread(src_path)
    height, width, chan = img.shape

    img = np.resize(img, (height*width, chan))

    if chan == 3:
        n = 3
        m = 0
    elif chan == 4:
        n = 4
        m = 1
    else:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    total_pixels = img.size//n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(m, n):
                if index < req_pixels:
                    img[p][q] = int(bin(img[p][q])[2:9] + b_message[index], 2)
                    index += 1

        img=img.reshape(height, width, n)
        cv2.imwrite(dest_path, img)
        print("Image Encoded Successfully")

def decode_steno(src_path):
    img = cv2.imread(src_path)
    height, width, chan = img.shape

    img = np.resize(img, (height*width, chan))

    if chan == 3:
        n = 3
        m = 0
    elif chan == 4:
        n = 4
        m = 1
    else:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    total_pixels = img.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(m, n):
            hidden_bits += (bin(img[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")

stegano_dict = {
    'eratosthenes': generators.eratosthenes,
    'fibonacci': generators.fibonacci,
    'fermat': generators.fermat,
    'identity': generators.identity,
    'log_gen': generators.log_gen,
}

def fast_encode(message, src_path, dest_path):
    img = stegano.lsbset.hide(src_path, message, generators.eratosthenes())
    img.save(dest_path.split('.')[0]+'stego.png')

def fast_decode(src_path):
    message = stegano.lsbset.reveal(src_path, generators.eratosthenes())
    return message
