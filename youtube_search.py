from googleapiclient.discovery import build
import os
import youtube_dl


class search:
    def __init__(self, api_key, channel, voice, keyword):
        self.api_key = api_key
        self.channel = channel
        self.voice = voice
        self.keyword = keyword
        self.song_there = os.path.isfile("song.mp3")

    def start(self):
        song_there = self.song_there
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            self.voice.stop()
            return

        if not self.voice.is_connected:
            self.channel.connect()
        else:
            pass

    def querry_one(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = youtube.search().list(
            part='snippet',
            q=self.keyword,
            type='video'
        )

        # TODO display results ask for choice lol
        response = request.execute()
        videoId = response['items'][0]['id']['videoId']
        return videoId

    def fileRename(self, videoId):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={videoId}'])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
