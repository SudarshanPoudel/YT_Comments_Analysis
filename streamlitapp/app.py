import streamlit as st
import preprocess
import pandas as pd

st.title("Youtube comments Analyzer")
url = st.text_input("Enter Youtube URL")

if url is not '':
    df = preprocess.preprocess(url=url)
    if(type(df)== pd.core.frame.DataFrame):
        st.dataframe(df)
    else:
        st.text(df)