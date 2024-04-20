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
        # Video details and comments
        st.markdown(helper.video_info_markdown(data = preprocess.get_video_info(url=url)), unsafe_allow_html = True)

        #Total no of comments
        st.markdown('## Total Comments : ' + str(len(df)))


        #Wordcloud
        st.header('Wordcloud')
        df_wc = helper.create_wordcloud(df=df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words
        st.header('Most common words')
        df_common = helper.most_common_words(df=df)[::-1]
        fig, ax = plt.subplots()
        ax.barh(df_common[0], df_common[1], color = 'red')
        st.pyplot(fig)

        #Timeline
        st.header('Timeline')
        timeline_df = helper.timeline(df=df)
        n = len(timeline_df['yearMonth']) // 10
        fig, ax = plt.subplots()
        ax.plot(timeline_df['yearMonth'], timeline_df['comment_text'])
        if n == 0:
            plt.xticks(rotation = 'vertical')
        else:
            plt.xticks(timeline_df['yearMonth'][::n],rotation = 'vertical')
        st.pyplot(fig)




    else:
        st.text(df)
