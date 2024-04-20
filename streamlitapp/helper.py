from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import re


def video_info_markdown(data):
    markdown = """
        <h2>{channel_name}</h2>
        <img src = '{thumbnail}' width = "100%">'
        <h3>{title} <span style = "font-size: 1.2rem"> ({relese_date})</span></h3>
    """.format(**data)

    return markdown

def timeline(df):
    timeline_df = df.groupby(['year', 'month']).count()['comment_text'].reset_index()
    yearMonth = []
    for i in range (timeline_df.shape[0]):
        yearMonth.append(timeline_df['month'][i] + '-' + str(timeline_df['year'][i]))
    timeline_df['yearMonth'] = yearMonth
    return timeline_df



def create_wordcloud(df):
    wc =WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    df_wc = wc.generate(df['comment_text'].str.cat(sep=" "))
    return df_wc

def most_common_words(df):
    f = open('streamlitapp/stopwords.txt', 'r')
    stop_words = f.read().split('\n')

    words = []
    for comment in df['comment_text']:
        for word in comment.lower().split():
            if word not in stop_words and re.match(r'^[^\W\d]*[a-zA-Z][^\W\d]*$', word):
                words.append(word.capitalize())
    df = pd.DataFrame(Counter(words).most_common(20))
    return df
            
