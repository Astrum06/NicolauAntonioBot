#  Author: Astrum06
#  Discord: Astrum1247 
#  09/03/2021
# 
#
#
#
#
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
from youtube_search import YoutubeSearch
import shutil

token_id = 'TOKEN'
prefix = '!'
bot = commands.Bot(command_prefix=prefix)
players = {}

version = 'version'

@bot.event
async def on_ready():
	print(f"Bot is ready")
	await bot.change_presence(activity=discord.Game(name='v'+version))

@bot.command()
async def bp(ctx, str):
	await ctx.send(str)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def say(ctx, str):
	await ctx.message.delete()
	await ctx.send(str)

@bot.command()
async def test(ctx):
	await ctx.send("Hello")

#----------------------------------------------

@bot.command()
async def name(ctx):
	await ctx.send("<@{}> is your name".format(ctx.message.author.id))

@bot.command()
async def mention(ctx, user:discord.User):
	await ctx.send("<@{}> is your name".format(user.id))

@bot.command()
async def poke (ctx, user:discord.User):
	await ctx.send("<@{}> pokes <@{}>".format(ctx.message.author.id, user.id))

@bot.command()
async def prefix (ctx,*,  newprefix):
	bot.command_prefix = newprefix
	await ctx.send("New prefix is {}".format(newprefix))

#-----------------------------------------------

@bot.command()
async def sum (ctx, a:int, b:int):
	await ctx.send(a+b)
@bot.command()
async def subtract (ctx, c:int, d:int):
	await ctx.send(c-d)
@bot.command()
async def multiply (ctx, e:int, f:int):
	await ctx.send(e*f)
@bot.command()
async def divide (ctx, g:int, h:int):
	if h != 0:
		await ctx.send(g/h)
	else:
		await ctx.send("Cannot divide by 0")

#----------------------------------------------

@bot.command()
@commands.has_role('DJ')
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@bot.command()
@commands.has_role('DJ')
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(pass_context=True, aliases=['p', 'pla'])
@commands.has_role('DJ')
async def play_url(ctx, url: str):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing song")
    print("playing\n")


@bot.command()
@commands.has_role('DJ')
async def play(ctx, search: str):
    results = YoutubeSearch(search, max_results=10).to_dict()
    url = results[0]
    url = 'https://www.youtube.com'+url['url_suffix']
    print(url)

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing song")
    print("playing\n")

    results = 0

@bot.command(pass_context=True, aliases=['pa', 'pau'])
@commands.has_role('DJ')
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@bot.command(pass_context=True, aliases=['r', 'res'])
@commands.has_role('DJ')
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@bot.command(pass_context=True, aliases=['s', 'sto'])
@commands.has_role('DJ')
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")

queues = {}

@bot.command(pass_context=True, aliases=['q', 'que'])
@commands.has_role('DJ')
async def add_url(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    await ctx.send("Adding song to the queue")

    print("Song added to queue\n")

@bot.command(pass_context = True)
async def add(ctx, search: str):
    results = YoutubeSearch(search, max_results=10).to_dict()
    url = results[0]
    url = 'https://www.youtube.com'+url['url_suffix']
    print(url)

    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    await ctx.send("Adding song to the queue")

    print("Song added to queue\n")

@bot.command(pass_context=True, aliases=['n', 'nex'])
@commands.has_role('DJ')
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        await ctx.send("Next Song")
    else:
        print("No music playing")
        await ctx.send("No music playing failed")

@bot.command(pass_context = True)
@commands.has_role('DJ')
async def clearq(ctx):
    os.remove("./Queue")

#----------------------------------------------

@bot.command()
async def pfp(ctx, user:discord.User):
	await ctx.send(user.avatar_url)

@bot.command()
async def mypfp(ctx):
	await ctx.send(ctx.message.author.avatar_url)


#----------------------------------------------

bot.run(token_id)