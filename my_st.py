import streamlit as st
from PIL import Image
import cv2
import torch
from torch import nn
from efficientnet_pytorch import EfficientNet
import albumentations as albu
from albumentations.pytorch.transforms import ToTensorV2
import numpy as np
import stegano
from stegano.lsbset import generators

st.set_page_config(
    page_title="Drought-watch",  # default page title
    layout="centered"
)

@st.cache
def cache_model():
    torch.backends.cudnn.benchmark = True
    net = EfficientNet.from_name('efficientnet-b1')
    net._fc = nn.Linear(in_features=1280, out_features=4, bias=True)
    checkpoint = torch.load('final_b1.pt')
    net.load_state_dict(checkpoint['model_state_dict'])
    return net.eval().cuda()

# https://stackoverflow.com/questions/32213893/how-to-cache-a-large-machine-learning-model-in-flask
def predict(img):
    net = cache_model()

    transform = albu.Compose([
        #albu.Resize(512, 512, p=1.0),
        ToTensorV2(p=1.0),
    ])

    img.save('model_image.png', quality=100)
    img = cv2.imread('model_image.png', cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)

    if len(img.shape) > 2 and img.shape[2] == 4:
        # convert the image from RGBA2RGB
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    img = transform(image=img)['image'].float()/255.0

    y_pred = net(img.unsqueeze(0).cuda())
    #st.write()
    #y_pred = 1 - nn.functional.softmax(y_pred, dim=1).data.cpu().numpy()[:,0]
    y_pred = y_pred.cpu().detach().numpy()
    return y_pred[:, 0], y_pred[:, 1:4]

def fast_encode(message, src_path, dest_path):
    img = stegano.lsbset.hide(src_path, message, generators.eratosthenes())
    img.save(dest_path)
    return img

def fast_decode(src_path):
    message = stegano.lsbset.reveal(src_path, generators.eratosthenes())
    return message

st.markdown("<style> .reportview-container .main footer {visibility: hidden;}    #MainMenu {visibility: hidden;}</style>", unsafe_allow_html=True)

st.write('<h1 style="font-weight:400; color:red">Stego</h1>', unsafe_allow_html=True)
st.write('### End-to-end steganography and steganlysis with Deep Convolutional Neural Networks')

mode = st.selectbox("What would you like to do?", ("Encode image", "Decode image", "Run model on image"))

classes = ['JMiPOD', 'JUNIWARD', 'UERD']

import math

userFile = st.file_uploader('Please upload an image or tfrecord', type=['jpg', 'jpeg', 'png', 'npy'])
if userFile is not None:
    img = Image.open(userFile)
    with st.spinner(text='Loading...'):
        if mode == 'Encode image':

            width, height = img.size
            ratio = math.floor(height / width)
            newheight = ratio * 1024
            img = img.resize((1024, newheight), Image.ANTIALIAS)
            img.save('image.png')
            message = st.text_input("Enter message to encode:")
            if st.button("Run steganography encoding"):
                #img = fast_encode(message, 'image.png', 'outimage.png')
                fast_encode(message, 'image.png', 'outimage.png')
                img = Image.open('outimage.png')
                st.image(img, width=None, caption='Output steganography encoded image', output_format='png')
        elif mode == 'Decode image':
            img.save('decode_image.png')
            if st.button("Run steganography decoding"):
                msg = fast_decode('decode_image.png')
                st.image(img, use_column_width=True, caption="Uploaded image", output_format='png')
                st.success("Message: " + msg)
        elif mode == "Run model on image":
            if st.button("Run model"):
                stego, out = predict(img)
                st.write(stego, out)
                cls = np.argmax(out)
                if stego>0.5:
                    label = f"Likely stegographed, possible algorithm {classes[cls]}"
                else:
                    label = f"Not stegographed"
                st.success(label)

#st.write('Feel free to [download images](https://github.com/stanleyjzheng/drought-watch/tree/master/example_images) to test. There are two file types: conventional images, which are 3 channel (RGB), and npy, which contain 10 channel images resulting in greater accuracy.')
#st.write('Convert from tfrecord to npy with our GitHub repo linked below.')
