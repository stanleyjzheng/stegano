# import streamlit as st
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

DEVICE = "cpu"

# st.set_page_config(page_title="Stegano", layout="centered")  # default page title


# @st.cache
def cache_model():
    if DEVICE == "cuda":
        torch.backends.cudnn.benchmark = True
    net = EfficientNet.from_name("efficientnet-b1")
    net._fc = nn.Linear(in_features=1280, out_features=4, bias=True)
    checkpoint = torch.load("final_b1.pt", map_location=torch.device(DEVICE))
    net.load_state_dict(checkpoint["model_state_dict"])
    return net.eval().to(DEVICE)


# https://stackoverflow.com/questions/32213893/how-to-cache-a-large-machine-learning-model-in-flask
def predict(image):
    net = cache_model()

    transform = albu.Compose(
        [
            ToTensorV2(p=1.0),
        ]
    )

    image.save("model_image.png", quality=100)
    image = cv2.imread("model_image.png", cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)

    if len(image.shape) > 2 and image.shape[2] == 4:
        # convert the image from RGBA2RGB
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    image = transform(image=image)["image"].float() / 255.0

    y_pred = net(image.unsqueeze(0).to(DEVICE))
    # st.write()
    # y_pred = 1 - nn.functional.softmax(y_pred, dim=1).data.cpu().numpy()[:,0]
    y_pred = y_pred.cpu().detach().numpy()
    return y_pred[:, 0], y_pred[:, 1:4]


def fast_encode(message, src_path):
    img = stegano.lsbset.hide(src_path, message, generators.eratosthenes())
    return img


# a stanleyzheng.ca 184.168.131.241
# cname www mighty-ravine-rt8xlwpm632si7s4ccr3jyv2.herokudns.com
# 96.51.150.211
def fast_decode(src_path):
    message = stegano.lsbset.reveal(src_path, generators.eratosthenes())
    return message


"""
st.markdown(
    "<style> .reportview-container .main footer {visibility: hidden;}    #MainMenu {visibility: hidden;}</style>",
    unsafe_allow_html=True)

st.write('<h1 style="font-weight:400; color:red">Stegano</h1>', unsafe_allow_html=True)
st.write('### End-to-end steganography and steganlysis with Deep Convolutional Neural Networks')

st.write('For best results, use a high resolution (at least 512x512) image.')
mode = st.selectbox("What would you like to do?", ("Encode image", "Decode image", "Run model on image"))

classes = ['JMiPOD', 'JUNIWARD', 'UERD']

import math

userFile = st.file_uploader('Please upload an image', type=['jpg', 'jpeg', 'png'])
if userFile is not None:
    img = Image.open(userFile)
    with st.spinner(text='Loading...'):
        if mode == 'Encode image':
            print(img.size)
            message = st.text_input("Enter message to encode:")
            if st.button("Run steganography encoding"):
                width, height = img.size
                if width > 1024 or height > 1024:
                    ratio = height / width
                    newheight = int(ratio * 1024)

                    img = img.resize((1024, newheight), Image.ANTIALIAS)
                img.save('image.png')
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
                if stego > 0.5:
                    label = f"Likely stegographed, possible algorithm {classes[cls]}"
                else:
                    label = f"Not stegographed"
                st.success(label)
"""
