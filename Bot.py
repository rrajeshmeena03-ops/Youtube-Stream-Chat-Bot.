import os
import google.generativeai as genai
from googleapiclient.discovery import build

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_latest_comments():
    channel_response = youtube.channels().list(
        id=CHANNEL_ID,
        part='contentDetails'
    ).execute()
    
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    playlist_response = youtube.playlistItems().list(
        playlistId=uploads_playlist_id,
        part='snippet',
        maxResults=3
    ).execute()

    for item in playlist_response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        
        comments_response = youtube.commentThreads().list(
            videoId=video_id,
            part='snippet',
            maxResults=10
        ).execute()

        for comment_item in comments_response['items']:
            top_comment = comment_item['snippet']['topLevelComment']['snippet']
            author_name = top_comment['authorDisplayName']
            user_text = top_comment['textDisplay']

            prompt = f"User '{author_name}' commented on my YouTube video: '{user_text}'. Reply warmly and concisely in Hindi/Hinglish, mentioning @{author_name}."
            ai_response = model.generate_content(prompt)

            print(f"Replying to {author_name}: {ai_response.text}")

if __name__ == "__main__":
    get_latest_comments()
  
