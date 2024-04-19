import dotenv
import os
import discord
from discord.ext import commands
from typing import Final
from youtube_dl import YoutubeDL
import datetime
import random
import asyncio

import ytmusic
import help

dotenv.load_dotenv()
token: Final[str] = os.getenv('TOKEN')
client = commands.Bot(command_prefix='./', intents=discord.Intents.all())

client.remove_command('help')

# Basic Command
@client.command(alias=['hi'])
async def hello(ctx):
  await ctx.send(f'Hello! {ctx.author.mention}')

@client.command(alias=['userinfo'])
async def whoami(ctx, member: discord.Member = None):
  if member is None:
    member = ctx.author
  embed = discord.Embed(
    title='User Information',
    description=f'{member.mention}', 
    color=discord.Color.blue(),
    timestamp=ctx.message.created_at
  )
  embed.set_thumbnail(url=member.avatar)
  embed.add_field(name='ID', value=member.id, inline=False)
  embed.add_field(name='Name', value=f'{member.display_name}#{member.discriminator}', inline=False)
  embed.add_field(name='Created At', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
  embed.add_field(name='Joined At', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
  embed.add_field(name='Top Role', value=member.top_role, inline=False)
  embed.add_field(name='Roles', value=' '.join([role.mention for role in member.roles]), inline=False)
  embed.add_field(name='Nick', value=member.nick, inline=False)
  await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def serverinfo(ctx):
  embed = discord.Embed(
    title='Server Information',
    description=f'{ctx.guild.name}', 
    color=discord.Color.blue(),
    timestamp=ctx.message.created_at
  )
  embed.set_thumbnail(url=ctx.guild.icon)
  embed.add_field(name='ID', value=ctx.guild.id, inline=False)
  embed.add_field(name='Owner', value=ctx.guild.owner, inline=False)
  embed.add_field(name='Created At', value=ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
  embed.add_field(name='Members', value=ctx.guild.member_count, inline=False)
  embed.add_field(name='Roles', value=' '.join([role.mention for role in ctx.guild.roles]), inline=False)
  embed.add_field(name='Channels', value=' '.join([channel.mention for channel in ctx.guild.channels]), inline=False)
  await ctx.send(embed=embed)
  
@client.command()
async def roll(ctx):
  await ctx.send(f'You rolled a {random.randint(1, 6)}')


#Log
@client.event
async def on_ready() -> None:
  print(f'{client.user} has connected to Discord!')

async def main():
    async with client:
        await client.add_cog(help.help_cog(client))
        await client.add_cog(ytmusic.music_cog(client))
        await client.start(token)

asyncio.run(main())