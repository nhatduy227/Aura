import pickle
import json
import sys

import numpy as np

from keras.models import load_model
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.image import img_to_array

from PIL import Image
import requests
from io import BytesIO

import traceback
from win32com.client import Dispatch

#constant
speak = Dispatch("SAPI.SpVoice").Speak

def init():
    global caption_model
    global tokenizer
    global encode_model
    global model_path

    global MAX_LEN
    global OUTPUT_DIM
    global WIDTH
    global HEIGHT

    MAX_LEN = 51
    OUTPUT_DIM = 2048
    WIDTH = 299
    HEIGHT = 299

    caption_model = load_model("model/caption_model.h5")
    encode_model = load_model("model/encode_model.h5")

    with open('model/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)


def describeImage(img_url):
    try:
        caption = "startseq"

        img = Image.open(img_url)
        img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        img = img_to_array(img)
        # img = img_url
        # preprocess the image

        img = preprocess_input(img)
        img = np.expand_dims(img, axis=0)

        x1 = encode_model.predict(img)
        x1 = x1.reshape((1, OUTPUT_DIM))

        # generate the caption

        for i in range(MAX_LEN):
            seq = tokenizer.texts_to_sequences([caption])
            x2 = pad_sequences(seq, maxlen=MAX_LEN)

            y = caption_model.predict([x1, x2], verbose=0)
            word = tokenizer.index_word[np.argmax(y)]

            if word == "endseq":
                break

            caption += " " + word

        caption = caption.replace("startseq", "").strip()
        speak(caption)
        return {"caption": caption}

    except Exception as e:
        print(traceback.format_exc())
        return {"error": str(e)}


def describe_video_stream(pipeline):
    init()
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        return

    # img = Image.open(color_frame.get_data())
    # img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    # img = img_to_array(img)

    color_image = np.asarray(color_frame.get_data())
    im = Image.fromarray(color_image)
    im.save("mode3.jpg")
    describeImage("mode3.jpg")




if __name__ == '__main__':
    init()
    describeImage("../img/mr-robot1.jpg")
