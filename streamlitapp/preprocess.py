from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

#Define API keys
api_key = 'AIzaSyCI1IHdWg8rJVabzIQ6VFGxaaytT76G5Ok'
youtube = build(serviceName='youtube', version='v3', developerKey=api_key)  

# Function to get Video ID from URL
def get_video_id(video_url):
    import re
    pattern = r"(?<=v=)[\w-]+(?=&|$)|(?<=youtu.be/)[\w-]+(?=&|$|\?)"
    match = re.search(pattern, video_url)
    if match:
        return match.group(0)
    else:
        return None
    
# function that fetches basic video information from youtube
def get_video_info(url):
    video_id = get_video_id(video_url=url)
    request = youtube.videos().list(part = 'snippet', id = video_id)
    response = request.execute()
    data = dict(channel_name = response['items'][0]['snippet']['channelTitle'],
                relese_date = response['items'][0]['snippet']['publishedAt'][:10],
                title = response['items'][0]['snippet']['title'],
                thumbnail = response['items'][0]['snippet']['thumbnails']['maxres']['url']
                )
    return data


# Main function that returns final df of comments
def preprocess(url):
    video_id = get_video_id(video_url=url)
    if(video_id):
        comment_data = get_comments(video_id=video_id)
        df = pd.DataFrame(comment_data)

        df['published_date'] = pd.to_datetime(df['published_date'])
        df['year'] = df['published_date'].dt.year
        df['month'] = df['published_date'].dt.month_name()
        df['day'] = df['published_date'].dt.day
        df['hour'] = df['published_date'].dt.hour

        return df
    else:
        return "Invalid URL"

    


# Function that fetches Comments using youtube API
def get_comments(video_id):    
    comments = []

    # It fetches first 100 comments only
    request = youtube.commentThreads().list(part = 'snippet', videoId = video_id, maxResults = 100)
    response = request.execute()
    for comment in response['items']:
        comments.append(dict(published_date = comment['snippet']['topLevelComment']['snippet']['publishedAt'],
                   user = comment['snippet']['topLevelComment']['snippet']['authorDisplayName'].replace('@', ''),
                   comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal'],
                   like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']))

    # Loop till we fetch all comments 
    while(True):
        # Try to obtain nest page token
        try:
            nextPageToken = response['nextPageToken']

        #If it don't exist break the loop
        except KeyError:
            break

        # fetch next page comments 
        nextPageToken = response['nextPageToken']
        nextReq = youtube.commentThreads().list(part = 'snippet', videoId = video_id, maxResults = 100, pageToken = nextPageToken)
        response = nextReq.execute()
        for comment in response['items']:
            comments.append(dict(published_date = comment['snippet']['topLevelComment']['snippet']['publishedAt'],
                    user = comment['snippet']['topLevelComment']['snippet']['authorDisplayName'].replace('@', ''),
                    comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal'],
                    like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']))
        
    if(len(comments) == 0):
        return 'Invalid URL'
    return comments