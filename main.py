import discord
from discord.ext import commands
import random
import youtube_dl
GFL = commands.Bot(command_prefix="pd ")
musics={}
ytdl = youtube_dl.YoutubeDL()



@GFL.event #créé un evenement
async def on_ready():
    print("Le stagiaire est toujours prêt.")

class Video:
    def __init__(self, url):
        video=ytdl.extract_info(url, download = False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@GFL.command()
async def ping(ctx):
    await ctx.send('Pong !')

@GFL.command(aliases=["8ball","test"])
async def _8ball(ctx, *, question):
    responses=["Oui, c'est certain.",
               "Oui",
               "A qui le dis tu ?",
               "Mange tes morts.",
               "Sans aucun doute.",
               "D'après moi, oui.",
               "Franchement, aucunne idée..",
               "Je n' affirmerai ou n'infirmerai rien sans la présence du ministre.",
               "Mais t'es taré? Comment tu peux penser ça?",
               "Non, aucune chance.",
               "Impossible.",
               "Non.",
               "Retire ça tout de suite !"]
    await ctx.send(f'Question: {question}\nRéponse: {random.choice(responses)}')

@GFL.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@GFL.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url,
         before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)

@GFL.command()
async def play(ctx, url=None):
    client = ctx.guild.voice_client
    video = Video(url)
    musics[ctx.guild]=[]
    play_song(client, musics[ctx.guild], video)


GFL.run("NzY1Mzc4MzE1MDQwODQ5OTcz.X4T8Gg.h00yxkOgfsxC9PXkSUrR_V-QZvA")      #Launch
