import dotenv
import os
import discord
from discord.ext import commands
from typing import Final
from youtube_dl import YoutubeDL
import youtubesearchpython
import datetime
import random


dotenv.load_dotenv()
token: Final[str] = os.getenv('TOKEN')

client = commands.Bot(command_prefix='./', intents=discord.Intents.all())

# Functions
def search_song(query):
    with YoutubeDL({}) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info:
            # Select the first result
            return info['entries'][0]['url']
        else:
            return None

# Command
@client.command(alias=['hi'])
async def hello(ctx):
  await ctx.send(f'Hello! {ctx.author.mention}')

# @client.command()
# async def shutdown(ctx):
#   await ctx.send('Shutting down...')
#   await client.close()

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
  # if member.avatar_url:
  #       embed.set_image(url=member.avatar_url)
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

# # read blocked words
# def read_blocked_words(filename):
#     with open(filename, 'r') as file:
#         blocked_words = file.read().split(',')
#     return [word.strip() for word in blocked_words]
# blocked_words = read_blocked_words('youtube-blacklist-words_comma-separated-text-file.txt')

# @client.event
# async def on_message(message):
#   for word in blocked_words:
#     if word in message.content:
#       await message.delete()
#       await message.channel.send(f'{message.author.mention} Do not use that word!')
#   await client.process_commands(message)


def ytsearch(title):
    try:
        searchresult = youtubesearchpython.VideosSearch(title, limit=1)
        result = searchresult.result()
        if result and 'result' in result and result['result']:
          theresult = result['result'][0]
          return theresult['link'], theresult['title']
        else:
            return None
    except Exception as e:
        print(f"Error occurred during YouTube search: {e}")
        return None
      
      
@client.command()
async def ytplay(ctx, *args):
  name = ' '.join(args)
  url, title = ytsearch(name)
  
  if url is None:
    await ctx.send('No results found')
    return
    
  voice_channel = ctx.author.voice.channel
  if voice_channel:
    voice_client = await voice_channel.connect()
    await ctx.send(f'Connected to voice channel: {voice_channel}')
  
    try:
      voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: print('done', e))
      await ctx.send(f"Playing {title}")
    except Exception as e:
      print(f"Error occurred during audio playback: {e}")
      await ctx.send(f"Error occurred during audio playback: {e}")
  else:
    await ctx.send("You are not connected to a voice channel")
  

# @client.command()
# async def play(ctx, url):
#     voice_channel = ctx.author.voice.channel
#     if voice_channel:
#         vc = await voice_channel.connect()
#         await ctx.send('Connected to voice channel')
#         ydl_opts = {
#             'format': 'bestaudio',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }
#         with YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
#             url2 = info['formats'][0]['url']
#             vc.play(discord.FFmpegPCMAudio(url2))
#     else:
#         await ctx.send("You are not connected to a voice channel")



# Log
@client.event
async def on_ready() -> None:
  print(f'{client.user} has connected to Discord!')

def main() -> None:
  client.run(token=token)
  
if __name__ == '__main__':
  main()