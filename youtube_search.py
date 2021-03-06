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

    def input_regonition(self):
        if self.keyword[0:4] == "yout" or self.keyword[0:5] == "https" or self.keyword[0:3] == "www":
            return self.keyword
        else:
            print(self.keyword)
            return self.querry_keywordsearch()

    def querry_keywordsearch(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = youtube.search().list(
            part='snippet',
            q=self.keyword,
            type='video'
        )

        # TODO display results ask for choice lol
        response = request.execute()
        videoId = response['items'][0]['id']['videoId']
        videoURL = f'https://www.youtube.com/watch?v={videoId}'
        return videoURL


    def fileRename(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download('https://www.youtube.com/watch?v=94zTrkr5_xY')
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
