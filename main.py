import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is ready for use!")
    print("---------------------")

@client.event
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")
        else:
            print(f"Skipped loading Cog. ({filename[:-3]})")

@client.command()
async def sync(ctx, *, guild: int = None):
    synced = await client.tree.sync()
    await ctx.reply(f'Successfully synced {len(synced)} slash command(s).')

client.run(token)
