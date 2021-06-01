import discord
from discord.ext import commands
import os

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def tony(self,ctx,message):
        if message.content.startswith("tony") or message.content.startswith("Tony"):
            await ctx.send("hello my name is Tony Zhao, i cannot go on the computer past 9pm")

    @commands.command()
    async def asian(self,ctx):
        await ctx.send("the three types of asians are: the smart ones, the karate ones, and the basketball one")

    @commands.command()
    async def shutdown(self,ctx):
        os.system('shutdown -s')


def setup(client):
    client.add_cog(Example(client))
