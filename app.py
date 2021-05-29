from PIL import Image 
import pytesseract 
import sys 
import pdf2image
from pdf2image import convert_from_bytes
import streamlit as st
import os
import streamlit.components.v1 as components
import csv
import base64 
import time
from google_trans_new import google_translator

timestr = time.strftime("%Y%m%d-%H%M%S")
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
language_codes_source = {"Japanese" : "jpn","German" : "deu", "Dutch": "nld", "Spanish" : "spa", "English" : "eng", "Irish" :"gle", "Cantonese" : "chi_sim", "Malay" : "msa", "French" : "fra"}
language_codes_target = {"Japanese" : "ja", "German" : "de", "Dutch": "nl", "Spanish" : "es", "English" : "en", "Irish" :"ga", "Cantonese" : "zh-cn", "Malay" : "ms", "French" : "fr"}

def extract_text(file_path, source_lang):
    PDF_file = file_path
    pages = convert_from_bytes(PDF_file, output_folder=".") 
    source_lang_code = language_codes_source[source_lang]
    images = []
    image_counter = 1
    all_t = ""
    for page in pages:
      filename = "page_" + str(image_counter) + ".jpg"
      st.write(filename)
      page.save(filename, 'JPEG')
      images.append(filename)
      st.spinner(text='In progress...')
      text = pytesseract.image_to_string(filename, lang=source_lang_code)
      all_t += text
      image_counter += 1
    
    for img in images:
        os.remove(img)
    return(all_t)

def upload_document():
    st.title("Pick a source and destination language")
    options_from = st.selectbox('Select the source language',
    ("",'English', 'German' ,'Dutch', 'Cantonese', 'Malay', 'Irish', 'Spanish', 'French', 'Japanese'))
    
    #options_from = st.multiselect('Select the source language',['English', 'German' ,'Dutch', 'Cantonese', 'Malay', 'Irish', 'Spanish', 'French'])
    if options_from != "":
        st.write('The file is in ', options_from)

    #options_to = st.multiselect('Select the destination language',['English', 'German' ,'Dutch', 'Cantonese', 'Malay', 'Irish', 'Spanish', 'French'])
   
    options_to = st.selectbox('Select the destination language',
    ("",'English', 'German' ,'Dutch', 'Cantonese', 'Malay', 'Irish', 'Spanish', 'French', 'Japanese'))
    
    #options_from = st.multiselect('Select the source language',['English', 'German' ,'Dutch', 'Cantonese', 'Malay', 'Irish', 'Spanish', 'French'])
    if options_to != "":
        st.write('The file will be translated ', options_to)

    st.markdown("____________________________________________")
    
    uploaded_file = st.file_uploader("Upload Files", type='pdf')
    if uploaded_file is not None:
        st.write("The translated text will be displayed below \n") 
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(uploaded_file.name)

        source_text = (extract_text(uploaded_file.getvalue(), options_from))
        if source_text == "":
            st.write("Emtpy")
        
        to_text = translate_row(source_text, options_to)
        st.write(to_text) 
        st.write("")

        text_downloader(to_text, uploaded_file.name, options_to)
    return 

def translate_row(row, target_lang):
    target_lang_code = language_codes_target[target_lang]
    translator = google_translator()
    to_lang = translator.translate(row, lang_tgt=target_lang_code)
    return to_lang

def text_downloader(raw_text, fname, target_lang):
    fname = fname.split(".")
    new_filename = "".join(fname[:-1])
    new_filename += "-to-" + target_lang + ".txt"
    b64 = base64.b64encode(raw_text.encode()).decode()
    st.markdown("#### Download File ###")
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href,unsafe_allow_html=True)

upload_document()
