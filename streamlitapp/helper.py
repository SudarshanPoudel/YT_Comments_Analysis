from wordcloud import WordCloud

def create_wordcloud(df):
    wc =WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    df_wc = wc.generate(df['comment_text'].str.cat(sep=" "))
    return df_wc