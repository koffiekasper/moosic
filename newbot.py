# bot.py
import os
from discord.ext.commands import Bot
import discord
from discord.utils import get
from dotenv import load_dotenv
import sys
import os
from songQueue import SongQueue
import youtube_dl
import pafy
from youtubesearchpython import VideosSearch
import validators


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = Bot("!")

intents = discord.Intents.default()
intents.members = True

limit = 5

songQueue = SongQueue(limit = limit)


@client.command()    
async def play(ctx, *args):
    global vc

    if len(args) > 1:
        link = ""
        for arg in args:
            link += arg + " "
    elif len(args) == 1:
        link = args[0]
    else:
        return False

    user = ctx.message.author.id

    if link != None:
        if not validators.url(link):
            link = VideosSearch(link, limit=1).result()['result'][0]['link']
        songQueue.addSong(user, link)
        await ctx.send(f'Processing song ' + link)

        member = ctx.message.author
        voice_channel = member.voice.channel
        channel=None

        try:
            if voice_channel != None:
                channel = voice_channel.name
                vc = await voice_channel.connect()
            else:
                await ctx.send('User is not in a channel')
        except discord.errors.ClientException:
            pass
       
        #video = pafy.new(link)
        #audiostreams = video.audiostreams
        #bestaudio = video.getbestaudio()
        #bestaudio.download(filepath="./audio.mp3")

        video_info = youtube_dl.YoutubeDL().extract_info(
            url = link,download=False
                )
        filename = f"audio.mp3"
        options = {
                'format':'bestaudio/best',
                "cookiefile":"/home/kasper/audiobot/cookie.txt",
                'preferredcodec':'mp3',
                'keepvideo':False,
                'outtmpl':filename
                }

        os.remove('audio.mp3')

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        vc.stop()
        player = vc.play(discord.FFmpegPCMAudio('./audio.mp3'))

    else:
        await ctx.send("Please provide a valid link")
    return

@client.command()
async def disconnect(ctx):
    for x in client.voice_clients:
        if (x.guild == ctx.message.guild):
            return await x.disconnect()

@client.event
async def on_ready():
    print('Connected to Discord!')
    
client.run(TOKEN)
