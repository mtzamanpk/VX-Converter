import re
import os
import discord
from discord.ext import commands
from flask import Flask
import threading
from keep_alive import keep_alive

keep_alive()

TOKEN = os.environ.get('DISCORD_TOKEN')
BOT_PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    converted_message = convert_links(message.content)
    if converted_message != message.content:
        sent_message = await message.channel.send(f'{message.author.mention} Converted link: {converted_message}')

        # Delete the original message sent by the author
        await delete_unconverted_message(message, sent_message)

    await bot.process_commands(message)

def convert_links(content):
    # Convert TikTok links
    tiktok_pattern = r'https://vm.tiktok.com/'
    tiktok_replacement = r'https://vm.vxtiktok.com/'
    content = re.sub(tiktok_pattern, tiktok_replacement, content)

    # Convert Instagram links
    instagram_pattern = r'https://instagram.com/'
    instagram_replacement = r'https://ddinstagram.com/'
    content = re.sub(instagram_pattern, instagram_replacement, content)

    # Convert web TikTok links
    web_tiktok_pattern = r'https://www.tiktok.com/'
    web_tiktok_replacement = r'https://vxtiktok.com/'
    content = re.sub(web_tiktok_pattern, web_tiktok_replacement, content)

    # Convert "x" links
    x_pattern = r'https://x.com/'
    x_replacement = r'https://fixupx.com/'
    content = re.sub(x_pattern, x_replacement, content)

    # Convert Twitter links
    twitter_pattern = r'https://twitter.com/'
    twitter_replacement = r'https://vxtwitter.com/'
    content = re.sub(twitter_pattern, twitter_replacement, content)

    return content

async def delete_unconverted_message(original_message, converted_message):
    try:
        # Fetch the message sent by the author
        author_message = await original_message.channel.fetch_message(original_message.id)

        # Check if the message is still unconverted and sent by the author
        if author_message.content == original_message.content and author_message.author == original_message.author:
            await author_message.delete()
    except discord.Forbidden:
        print('Bot does not have permission to delete messages.')
    except discord.NotFound:
        print('Message not found for deletion.')
    except discord.HTTPException as e:
        print(f'An error occurred while deleting a message: {e}')

def run_bot():
    bot.run(TOKEN)
    
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
