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

DEVICE='cuda'

st.set_page_config(
    page_title="Stegano",  # default page title
    layout="centered"
)


@st.cache
def cache_model():
    if DEVICE=='cuda':
        torch.backends.cudnn.benchmark = True
    net = EfficientNet.from_name('efficientnet-b1')
    net._fc = nn.Linear(in_features=1280, out_features=4, bias=True)
    checkpoint = torch.load('final_b1.pt', map_location=torch.device(DEVICE))
    net.load_state_dict(checkpoint['model_state_dict'])
    return net.eval().to(DEVICE)


def predict(image):
    net = cache_model()

    transform = albu.Compose([
        ToTensorV2(p=1.0),
    ])

    image.save('model_image.png', quality=100)
    image = cv2.imread('model_image.png', cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)

    if len(image.shape) > 2 and image.shape[2] == 4:
        # convert the image from RGBA2RGB
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    image = transform(image=image)['image'].float() / 255.0

    y_pred = net(image.unsqueeze(0).to(DEVICE))
    # st.write()
    # y_pred = 1 - nn.functional.softmax(y_pred, dim=1).data.cpu().numpy()[:,0]
    y_pred = y_pred.cpu().detach().numpy()
    return y_pred[:, 0], y_pred[:, 1:4]


def fast_encode(message, src_path, dest_path):
    img = stegano.lsbset.hide(src_path, message, generators.eratosthenes())
    img.save(dest_path)
    return img


def fast_decode(src_path):
    message = stegano.lsbset.reveal(src_path, generators.eratosthenes())
    return message

def compare_images(img1, img2):
    from PIL import ImageChops
    return ImageChops.difference(img2, img1)

def contrast_compare_images(img1, img2):
    from PIL import ImageChops
    # img1 = np.array(img1)
    # img2 = np.array(img2)
    # diff = np.absolute(img2-img1)
    diff = np.array(ImageChops.difference(img2, img1))
    #diff = (diff-np.min(diff))/(np.max(diff)-np.min(diff))
    #return Image.fromarray(np.uint8(diff*255))
    return diff

st.markdown(
    "<style> .reportview-container .main footer {visibility: hidden;}    #MainMenu {visibility: hidden;}</style>",
    unsafe_allow_html=True)

st.write('<h1 style="font-weight:400; color:red">Stegano</h1>', unsafe_allow_html=True)
st.write('### End-to-end steganography and steganlysis with Deep Convolutional Neural Networks')

st.write('For best results, use a high resolution (at least 512x512) image.')
mode = st.selectbox("What would you like to do?", ("Encode image", "Decode image", "Run model on image", "Visualize image differences"))

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
                fast_encode(message, img, 'outimage.png')
                img = Image.open('outimage.png')
                st.image(img, width=None, caption='Output steganography encoded image', output_format='png')
        elif mode == 'Decode image':
            if st.button("Run steganography decoding"):
                msg = fast_decode(img)
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
        elif mode == "Visualize image differences":
            userFile_2 = st.file_uploader('Please upload a second image to compare', type=['jpg', 'jpeg', 'png'])
            if st.button("Run image difference"):
                width, height = img.size
                if width > 1024 or height > 1024:
                    ratio = height / width
                    newheight = int(ratio * 1024)

                    img = img.resize((1024, newheight), Image.ANTIALIAS)
                img_2 = Image.open(userFile_2)
                #i = compare_images(img, img_2)
                diff = contrast_compare_images(img, img_2)
                st.image(img, width=None, caption='Image differences', output_format='png')