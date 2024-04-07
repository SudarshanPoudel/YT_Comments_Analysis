import streamlit as st
import preprocess
import helper
import pandas as pd
import matplotlib.pyplot as plt

st.title("Youtube comments Analyzer")
url = st.text_input("Enter Youtube URL")

if url is not '':
    df = preprocess.preprocess(url=url)
    if(type(df)== pd.core.frame.DataFrame):

        #Wordcloud
        st.header('Wordcloud')
        df_wc = helper.create_wordcloud(df=df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Dataframe
        st.header('Data Frame')
        st.dataframe(df)



    else:
        st.text(df)
