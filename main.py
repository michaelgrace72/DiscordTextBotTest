import dotenv
import os
import discord
from typing import Final
import datetime
import random

dotenv.load_dotenv()

TOKEN: Final[str] = os.getenv('TOKEN')

# STEP 1 BOT SETUP
intents: discord.Intents = discord.Intents.default()
intents.message_content = True
client: discord.Client = discord.Client(intents=intents)

# STEP 2 MESSAGE FUNCTIONALLITY
def get_response(user_input:str) -> str:
  lowered = user_input.lower()
  
  if lowered == '':
    return 'You awfully quite'
  elif lowered == 'hello' or lowered == 'hi':
    return 'Hello!'
  elif lowered == 'bye':
    return 'Goodbye!'
  elif lowered == 'roll':
    return str(random.randint(1, 6))
  else:
    return random.choice([
      'I do not understand',
      'Please try again',
      'Can you rephrase that?'
    ])

async def send_message(message: discord.Message, user_message: str) -> None:
    if not user_message:
        print('No message')
        return
    
    if is_private:= user_message[0:2] == '?/':
        user_message = user_message[2:]
    
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)    
        
# STEP 3 DISCORD BOT STARTUP
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')
    
# STEP 4 DISCORD BOT MESSAGE
@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    time = datetime.datetime.now()
    print(f'{time} {username} in {channel} says: {user_message}')      
    await send_message(message, user_message)
    
# STEP 5 DISCORD BOT RUN
def main() -> None:
    client.run(token=TOKEN) 
    
if __name__ == '__main__':
    main()