import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Howdy hey world!")
    print("-----------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am kiki's bot!")

@client.command()
async def info(ctx):
    await ctx.send("Bot made using discord.py <:python:1149634717113647154>, by `kiki124`.")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1085275183507587155)
    await channel.send("Hello")

@client.command(pass_context = True )
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command!")

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")
client.run("TOKEN")
