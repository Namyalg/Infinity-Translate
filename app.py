from multiapp import MultiApp
import streamlit as st

from pdf import upload_file

def foo():
    st.title("Foo")
    return 

app = MultiApp()


#app.add_app("Foo", foo)
app.add_app("Upload the case file", upload_file)
app.run()
