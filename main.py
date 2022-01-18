from discord.ext import commands
from dotenv import load_dotenv
import os

from utils.database import *

load_dotenv()

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

@client.event
async def on_ready():
  print("@=============@")
  print("   BOT ONLINE  ")
  print("@=============@")
  
@client.cooldown(1, 2, commands.BucketType.guild)
@client.has_permissions(ban_members=True)
@client.command()
async def changeprefix(self, ctx, prefix : str = None):
  if prefix != None:
    res = await change_prefix(ctx.guild.id, prefix)
      if res == False:
        return await ctx.channel.send(f"{ctx.author.name}, esse prefixo é **igual** ao atual.")
      return await ctx.channel.send(f"{ctx.author.name}, prefixo regional alterado para ``{prefix}``")
@changeprefix.error
async def changeprefix_error(self, ctx, error): print(error)

@client.command()
async def money(ctx):
  await ctx.channel.send(f"{ctx.author.name}, você tem {await get_user_money(ctx.guild.id, ctx.author.id)} em money!")

client.run(os.getenv("token"))