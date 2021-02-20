import albumentations as albu
import torch
import timm
from torch import nn
from albumentations.pytorch.transforms import ToTensorV2
import cv2
import numpy as np


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