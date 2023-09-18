import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.errors import MissingPermissions
from discord import Member
import asyncio
from discord import app_commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Howdy hey world!")
    print("-----------------")
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@client.tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction= discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!",
    ephemeral=True)

@client.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}")

@client.command()
async def hello(ctx):
    hello_embed = discord.Embed(title="Hello!",description="Howdy! <a:wave:1152496042286256198>", color=0x00A8FB)
    await ctx.send(embed=hello_embed)

@client.command()
async def info(ctx):
    info_embed = discord.Embed(
        title="Bot info",
        description="",
        color=0x00A8FB
    )
    info_embed.add_field(name=":link: Website", value="coming soon...", inline=False)
    info_embed.add_field(name="<:activedeveloper:1152985937479995432> Development", value="Developed by `kiki124` using discord.py <:dpy:1150111826441404547>", inline=False)

    await ctx.send(embed=info_embed)


@client.command()
async def commands (ctx):
    commands_embed = discord.Embed(
        title="Available commands:",
        description="",
        color=0x00A8FB
    )
    commands_embed.add_field(name="`=info`", value="Gives info about the bot.",inline=False)
    commands_embed.add_field(name="`=commands`", value="Lists all available commands.", inline=False)
    commands_embed.add_field(name="`ban`", value="Temporarily bans a member, Use: `=ban <@mention> <time in days> <reason>`", inline=False)
    commands_embed.add_field(name="`ban`", value="Permanently bans a member, Use: `=ban <mention> <reason>`")
    await ctx.send(embed=commands_embed)

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, duration: int = None, *, reason="No reason provided"):
    embed = discord.Embed(
        title="User Banned",
        description=f"{member.mention} has been banned{' for ' + str(duration) + ' days' if duration else ''}.",
        color=discord.Colour.red()
    )
    embed.add_field(name="Reason", value=reason)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await member.ban(reason=reason)
    await ctx.send(embed=embed)

    if duration:
        unban_task = asyncio.create_task(unban_after_duration(member, duration))
        client.unban_tasks[member.id] = unban_task

async def unban_after_duration(member, duration):
    await asyncio.sleep(duration * 86400)  # 86400 seconds in a day
    await member.guild.unban(member)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        error_embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the `BAN_MEMBERS` permission to use this command.",
            color=discord.Colour.red()
        )
        await ctx.send(embed=error_embed)

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    embed = discord.Embed(
        title="User Kicked",
        description=f"{member.mention} has been kicked.",
        color=discord.Colour.orange()
    )
    embed.add_field(name="Reason", value=reason)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    
    await member.kick(reason=reason)
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        error_embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the `KICK_MEMBERS` permission to use this command.",
            color=discord.Colour.orange()
        )
        await ctx.send(embed=error_embed)

client.unban_tasks = {}

 
client.run("TOKEN")
