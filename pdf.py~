from PIL import Image 
import pytesseract 
import sys 
import pdf2image
from pdf2image import convert_from_bytes
import streamlit as st
import os
import pickle

from google_trans_new import google_translator
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

#pytesseract.pytesseract.tesseract_cmd = './.apt/usr/bin/tesseract'
#pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
#pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
#pytesseract.pytesseract.tesseract_cmd = (
#    r'/usr/bin/tesseract'
#)
import csv
page_count = 0

def extract_text(file_path):
    PDF_file = file_path
    # Store all the pages of the PDF in a variable 
    pages = convert_from_bytes(PDF_file, output_folder=".") 

    images = []
    image_counter = 1
    all_t = ""
    # Iterate through all the pages stored above 
    for page in pages:
      filename = "page_" + str(image_counter) + ".jpg"
      st.write(filename)
      page.save(filename, 'JPEG')
      images.append(filename)
      st.spinner(text='In progress...')
      text = pytesseract.image_to_string(filename, lang="kan")
      #st.write(text)
      all_t += text
      image_counter += 1

    FIR_starts = 0
    FIR_ends = 0
    counter = 0
    
    #st.write("the entire case content is ")
    #st.write(all_t)

    for line in all_t.splitlines():
      counter += 1
      if 'ಪ್ರಥಮ ವರ್ತಮಾನ ವರದಿಯ ವಿವರಗಳು' in line:
        st.write("started")
        FIR_starts = counter
      if 'ತೆಗೆದುಕೊಂಡ ಕ್ರಮ' in line:
        FIR_ends = counter
    
    print("THE FIR content is ")
    
    FIR_content = (" ".join(all_t.strip("\n").splitlines()[FIR_starts - 1 : FIR_ends]))    
    print(FIR_content)
    for img in images:
        os.remove(img)
    return(FIR_content)


def translate_row(row):
    translator = google_translator()
    a = translator.translate(row, lang_tgt='en')
    index = a.find("Report")
    index2 = a.rfind("11")
    return a[index+6:index2]

def upload_file():
    st.title("First Information Report Classifier")
    uploaded_file = st.file_uploader("Upload Files", type='pdf')
    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write("This will take a few minutes to process \n") 
        kannada_text = (extract_text(uploaded_file.getvalue()))
        st.write("The case content in kannada is \n")
        print(kannada_text)
        if kannada_text == "":
            st.write("Emtpy")
        st.write(kannada_text)
        st.write("The case content in english is \n")
        english_text = translate_row(kannada_text)
        print(english_text)
        st.write(english_text)
        case_content = english_text

        if st.button("Predict"):
            result = classify_utterance(case_content)
            st.success('The case belongs to class {}'.format(result))
    return 


def classify_utterance(utt):
    # load the vectorizer
    loaded_vectorizer = pickle.load(open('vectorizer1.pickle', 'rb'))

    # load the model
    loaded_model = pickle.load(open('classification1.model', 'rb'))

    # make a prediction
    return(loaded_model.predict(loaded_vectorizer.transform([utt])))

     
def enter_text():
    st.title("First Information Report Classifier")
    case_content = st.text_input("Case Content", "")

    if st.button("Predict"):
        result = classify_utterance(case_content)
        st.success('The output is {}'.format(result))
    return 
