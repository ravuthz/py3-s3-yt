from dotenv import load_dotenv

load_dotenv()

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# client_secret_345354458517-0kqbjrb0rlatn3g64rc5djhbdtdab3r2.apps.googleusercontent.com

credentials = Credentials.from_authorized_user_file('./client_secret.json', ['https://www.googleapis.com/auth/youtube'])

local_file_path = "/tmp/"
yt_developerKey=os.getenv('YT_DEVELOPER_KEY')

def upload_video(video_file_path, title, description, privacy_status):
    try:
        youtube = build("youtube", "v3", developerKey=yt_developerKey, credentials=credentials)

        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": privacy_status
                }
            },
            media_body=MediaFileUpload(video_file_path, mimetype="video/mp4")
        )

        response = request.execute()
        print("Video uploaded successfully.")
        print("Video ID: ", response['id'])
    except HttpError as error:
        print("An error occurred while uploading the video: ", error)