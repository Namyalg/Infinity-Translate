from PIL import Image 
import pytesseract 
import sys 
import pdf2image
from pdf2image import convert_from_bytes
import streamlit as st
import os
import pickle

import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

from google_trans_new import google_translator
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
import csv
page_count = 0

def extract_text(file_path):
    PDF_file = file_path
    pages = convert_from_bytes(PDF_file, output_folder=".") 

    images = []
    image_counter = 1
    all_t = ""
    for page in pages:
      filename = "page_" + str(image_counter) + ".jpg"
      st.write(filename)
      page.save(filename, 'JPEG')
      images.append(filename)
      st.spinner(text='In progress...')
      text = pytesseract.image_to_string(filename, lang="dan")
      all_t += text
      image_counter += 1
    
    for img in images:
        os.remove(img)
    return(all_t)


def translate_row(row):
    translator = google_translator()
    a = translator.translate(row, lang_tgt='en')
    return a

def upload_file():
    st.title("Dutch to English")
    uploaded_file = st.file_uploader("Upload Files", type='pdf')
    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write("This will take a few minutes to process \n") 
        dutch_text = (extract_text(uploaded_file.getvalue()))
        if dutch_text == "":
            st.write("Emtpy")
        #st.write(dutch_text)
        st.write("The case content in english is \n")
        english_text = translate_row(dutch_text)

        st.write(english_text) 
        st.write("")
        text_downloader(english_text)
    return 

def text_downloader(raw_text):
	b64 = base64.b64encode(raw_text.encode()).decode()
	new_filename = "new_text_file_{}_.txt".format(timestr)
	st.markdown("#### Download File ###")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
	st.markdown(href,unsafe_allow_html=True)

     

