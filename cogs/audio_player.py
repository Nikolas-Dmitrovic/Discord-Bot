import os
import discord
from discord.ext import commands
from googleapiclient.discovery import build
import youtube_dl

# TODO add error handling
# TODO add url detetor and bypass

youtube_api_key = 'AIzaSyBZtYWgBBF3UfnWO82NBhfC6DSp2xkD28g'


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
            # ydl.download(f'{url}')
            ydl.download('https://www.youtube.com/watch?v=UtZBA1bVbcs&ab_channel=ASAPROCKYUPTOWNASAPROCKYUPTOWN')
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")


class music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    # add more error handling
    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await ctx.se1nd('i am already in the voice call')

    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command()
    async def skip(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await voice.stop()

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await voice.pause()

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await voice.resume()

    @commands.command()
    async def play(self, ctx, *, keyword):
        channel = ctx.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
            '''if not voice.is_connect():

                channel.connect()
                if song_there:
                    os.remove("song.mp3")'''
        except PermissionError:
            voice.stop()
            return

        search_vid = search(youtube_api_key, channel, voice, keyword)
        vidid = search_vid.input_regonition()
        search_vid.fileRename(vidid)
        voice.play(discord.FFmpegPCMAudio("song.mp3"))


def setup(client):
    client.add_cog(music(client))
