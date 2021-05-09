import time

import discord
import random
import json
import requests
import os
from discord.ext import commands, tasks
from itertools import cycle
import youtube_search

# youtube api key
youtube_api_key = 'AIzaSyBZtYWgBBF3UfnWO82NBhfC6DSp2xkD28g'

# TODO create command that allows people to add to boris's stause my taking in a message and adding it to a json file
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', help_command=None ,intents = intents)


# on ready events
@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready')


# tasks
@tasks.loop(seconds=10)
async def change_status():
    f = open('status.json')
    dataloaded = json.load(f)
    status = cycle(random.choice(dataloaded))
    await client.change_presence(activity=discord.Game(next(cycle(status))))


# client events

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


@client.listen()
async def on_message(message):
    if message.content.startswith('hello'):
        print(message)


@client.listen()
async def on_message(message):
    if message.content.startswith('!member'):
        for guild in client.guilds:
            for member in guild.members:
                print(member)  # or do whatever you wish with the member detail


# commands
# create list of commands to make


# help command
@client.command()
async def help(ctx, message="1"):
    colour = 0x00ff00
    if int(message) == 1:
        embedVar = discord.Embed(title="page one", description="Desc", color=colour)
        embedVar.add_field(name="Grandson", value="Makes grandma proud", inline=False)
        embedVar.add_field(name="clear",
                           value="clear messages, state number of messges you want to remove plus one, can only be used by bot owner or server admins",
                           inline=False)
        embedVar.add_field(name="ping", value="pings the bot server", inline=False)
        embedVar.add_field(name="shutup", value="shutup followed by a user @, tells them to shut up", inline=False)
        embedVar.add_field(name="8ball", value="8ball followed by a question, returns an answer", inline=False)
        await ctx.send(embed=embedVar)
    if int(message) == 2:
        embedVar = discord.Embed(title="Title", description="Desc", color=colour)
        embedVar.add_field(name="insult",
                           value="insult followed by a user @, returns an insult dirrected at the @ user", inline=False)
        embedVar.add_field(name="inspire", value="inspire returns an inspirational quote", inline=False)
        embedVar.add_field(name="poop", value="see for a surprise", inline=False)
        await ctx.send(embed=embedVar)
    if int(message) == 3:
        embedVar = discord.Embed(title="Title", description="Desc", color=colour)
        embedVar.add_field(name="join", value="joins the voice channel of the requsting user", inline=False)
        embedVar.add_field(name="leave", value="leaves the current voice channel", inline=False)
        embedVar.add_field(name="pause", value="pauses the current playing sound", inline=False)
        embedVar.add_field(name="resume", value="resumes the paused sound", inline=False)
        embedVar.add_field(name="skip", value="skips the current playing sound", inline=False)
        embedVar.add_field(name="play",
                           value="play followed by a search keyword, keyword searched in youtube engine and returns and play most popular option",
                           inline=False)
        await ctx.send(embed=embedVar)
    else:
        pass


def is_it_me(ctx):
    return ctx.author.id == 429641806888566785


def salami(ctx):
    return ctx.author.id == 387275732268613632


@client.command()
async def add(ctx, *, message):
    status = [message]
    with open('status.json', 'r+') as file:
        data = json.load(file)
        data.append(status)
        file.seek(0)
        json.dump(data, file, indent=4)
    await ctx.send(f'"{message}" has been added to my status cylce')


@client.command()
# @commands.check(salami)
async def grandson(ctx):
    await ctx.send("I love women")


@client.command()
# @commands.has_permissions(manage_messages=True)
@commands.check(is_it_me)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('please pass in all required arguments')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


@client.command(aliases=['shut up', 'shutup'])
async def shut_up(ctx, member: discord.Member):
    await ctx.send(f'ya shut up {member.mention}')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question='am i cool'):
    respomces = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(respomces)}')


@client.command(aliases=['who'])
async def who_asked(ctx):
    await ctx.send('i wonder who asked')


@client.command()
async def insult(ctx, member: discord.Member):
    response = requests.get("https://insult.mattbas.org/api/insult.json")
    json_data = json.loads(response.text)
    await ctx.send(f'{member.mention} {json_data["insult"]}')


def get_quote():
    response = requests.get("Https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)


@client.command()
async def poop(ctx):
    await ctx.send("poopity scoop")


@client.command()
async def mytype(ctx):
    await ctx.send("4'11 newly single latina chicks")


# voice commands

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@join.error
async def join_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send('i am already in the voice call')


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


# TODO add spotify api queue for voice chat https://developer.spotify.com/console/get-search-item/

@client.command(aliases=['stop'])
async def play(ctx, keyword):
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        voice.stop()
        return

    if not voice.is_connected:
        await channel.connect()
    else:
        pass

    search_vid = youtube_search.search(youtube_api_key, channel, voice, keyword)
    vidid = search_vid.querry_one()
    search_vid.fileRename(vidid)
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


# TODO snake game
@client.command()
async def snake(ctx):
    # todo use emojo codes as var to bypass imbed message length max
    wms = ":white_large_square:"
    wms1 = ":white_large_square:"
    wms2 = ":white_large_square:"
    wms3 = ":white_large_square:"
    wms4 = ":white_large_square:"
    wms5 = ":white_large_square:"
    wms6 = ":white_large_square:"
    wms7 = ":white_large_square:"
    wls = ":white_medium_small_square:"
    grid = [(wms + wms + wms + wms + wms + wms + wms),
            (wms + wms1 + wms2 + wms3 + wms4 + wms5 + wms6),
            (wms + wms + wms + wms + wms + wms + wms), (wms + wms + wms + wms + wms + wms + wms),
            (wms + wms + wms + wms + wms + wms + wms), (wms + wms + wms + wms + wms + wms + wms),
            (wms + wms + wms + wms + wms + wms + wms)]

    colour = 0x00ff00
    embedVar = discord.Embed(color=colour)
    for i in range(1):
        embedVar.add_field(name="a",
                           value=f"{grid[0]} \n {grid[1]} \n {grid[2]} \n {grid[3]} \n {grid[4]} \n {grid[5]} \n {grid[6]}",
                           inline=False)

    msg = await ctx.send(embed=embedVar)
    apple = ":apple:"
    print(grid[1])
    line = grid[1].find(wms2)
    print(line)

    # embedVar.remove_field(0)
    '''embedVar.set_field_at(index=0, name="a",
                          value=f"{grid[0]} \n {line} \n {grid[2]} \n {grid[3]} \n {grid[4]} \n {grid[5]} \n {grid[6]}",
                          inline=False)
    time.sleep(2)
    await msg.edit(embed=embedVar)'''


# @someone command
@client.command()
async def someone(ctx):
    # x = ctx.message.guild.members
    guild = ctx.guild
    names = guild.fetch_members(limit=150)
    list = []
    async for member in names:
        list.append(member)
    print()
    user = random.choice(list)

    await ctx.send(f'Hi {user.mention}')


client.run("ODA0NDEyNTkwMjI2ODAwNjgy.YBL9mg.b08RoWS5kKWiNshkXCEgCTuQWM0")
