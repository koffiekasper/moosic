import validators
from youtubesearchpython import VideosSearch
import youtube_dl
import os

class Song:
    def __init__(self, user, arg):
        self.user = user
        if not validators.url(arg):
            self.link = VideosSearch(arg, limit = 1).result()['result'][0]['link']
        else:
            self.link = arg

    def renderAudio(self):
        video_info = youtube_dl.YoutubeDL().extract_info(
            url = self.link, download=False
                )
        filename = f"audio.mp3"
        options = {
                'format':'bestaudio/best',
                'preferredcodec':'mp3',
                'keepvideo':False,
                'outtmpl':filename
                }
        os.remove('audio.mp3')

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        return
