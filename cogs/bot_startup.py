import discord
from discord.ext import commands, tasks
from itertools import cycle
import json
import random



class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print('bot is online')

    @tasks.loop(seconds=10)
    async def change_status(self):
        f = open('status.json')
        dataloaded = json.load(f)
        status = cycle(random.choice(dataloaded))
        await self.client.change_presence(activity=discord.Game(next(cycle(status))))

    # commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


def setup(client):
    client.add_cog(Example(client))
