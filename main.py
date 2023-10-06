import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, is_owner
from discord.ext.commands.errors import MissingPermissions
from discord import Member
import asyncio
from discord import app_commands
import re
# If some emojis are not working, then you'll need to replace them with custom emojis from your server or from server that your bot is at.

# Put in your desired prefix in the command.prefix=""
client = commands.Bot(command_prefix="=", intents=discord.Intents.all())


@client.event
async def on_ready():
    # Replace with your guild ID for the bot to show Watching <member count> members.
    guild_id = 1085226468600193137
    guild = discord.utils.get(client.guilds, id=guild_id)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f'{guild.member_count} players.'))
    print("Bot is ready for use!")
    print("---------------------")
    try:
        # Syncs all slash commands with discord.
        synced = await client.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@client.tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!", ephemeral=True)

@client.tree.command(name="say", description="Send a message using the bot")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    embed = discord.Embed(
        title=f"Message from {interaction.user.display_name}.",
        description=f"{thing_to_say}",
        color=0x00A8FB  # You can change this color to whatever hex color you want just put 0x<hex color only number>
    )
    embed.set_author(name=interaction.user.display_name,
                     icon_url=interaction.user.avatar)
    embed.set_footer(
        text=f"This message was sent by {interaction.user.display_name}.")
    await interaction.response.send_message(embed=embed)

@client.command()
async def avatar(ctx, *, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(
        title=f"Avatar for {member}",
        color=0x00A8FB
    )
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)


@client.tree.command(name="avatar", description="Get the avatar of a user.")
@app_commands.describe(member="The avatar of what user?")
async def avatar(Interaction: discord.Interaction, member: Member = None):
    member = Interaction.user if not member else member
    embed = discord.Embed(
        title=f"Avatar for {member}",
        color=0x00A8FB
    )
    embed.set_image(url=member.avatar.url)
    await Interaction.response.send_message(embed=embed)

@client.tree.command(name="invite", description="Invite the bot to your server!")
async def invite(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Invite the bot!",
        # Replace this link with the invite link for your bot.
        description="Use [this link](https://discord.com/api/oauth2/authorize?client_id=1149388511590486057&permissions=8&scope=bot) to invite the bot.",
        color=0x00A8FB
    )
    await interaction.response.send_message(embed=embed)


@client.command()
async def hello(ctx):
    hello_embed = discord.Embed(
        title="Hello!", description="Howdy! <a:wave:1152496042286256198>", color=0x00A8FB)
    await ctx.send(embed=hello_embed)

@client.tree.command(name="info", description="Get information about the bot!")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot info",
        color=0x00A8FB
    )
    embed.add_field(name=":link: Website",
                    value="Coming soon...", inline=False)
    embed.add_field(name="<:activedeveloper:1152985937479995432> Development",
                    value="Developed by `kiki124` using discord.py <:dpy:1150111826441404547>", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="commands", description="Get all of the available commands.")
async def commands(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Available commands:",
        color=0x00A8FB
    )
    embed.add_field(
        name="`/info`", value="Gives information about the bot.", inline=False)
    embed.add_field(name="`/invite`",
                    value="Invite the bot to your server!", inline=False)
    embed.add_field(name="`/commands`",
                    value="Get all of the available commands.", inline=False)
    embed.add_field(
        name="`=ban`", value="Temporarily ban a member, Use: `=ban <@mention> <days>")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="banner", description="Get the banner of a user.")
@app_commands.describe(user="The banner of what user?")
async def banenr (Interaction: discord.Interaction, user: Member):
    fetched_user = await client.fetch_user(user.id)
    if fetched_user.banner:
        embed = discord.Embed(
            title=f"Banner of {fetched_user}",
            color=0x00A8FB
        )
        embed.set_image(url=fetched_user.banner.url)
        await Interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="User does not have a banner.",
            description="The specified user does not have a banner.",
            color=discord.Colour.orange()
        )
        await Interaction.response.send_message(embed=embed)

@client.command(name="banner", description="Get the banner of a user.")
async def banner(ctx, user: discord.Member):
    # Fetch the user to get the banner
    fetched_user = await client.fetch_user(user.id)

    if fetched_user.banner:
        embed = discord.Embed(
            title=f"Banner for {fetched_user}",
            color=0x00A8FB
        )
        embed.set_image(url=fetched_user.banner.url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="User does not have a banner.",
            color=discord.Colour.red(),
            description="The specified user does not have a banner."
        )
        await ctx.send(embed=embed)

@client.command()
async def commands(ctx):
    embed = discord.Embed(
        title="Available commands:",
        description="",
        color=0x00A8FB
    )
    embed.add_field(
        name="`/info`", value="Gives info about the bot.", inline=False)
    embed.add_field(name="`=commands`",
                    value="Lists all available commands.", inline=False)
    embed.add_field(
        name="`ban`", value="Temporarily bans a member, Use: `=ban <@mention> <time in days> <reason>`", inline=False)
    embed.add_field(
        name="`ban`", value="Permanently bans a member, Use: `=ban <mention> <reason>`")
    await ctx.send(embed=embed)

@client.tree.command(name="purge", description="Quickly remove a number of messages")
@app_commands.describe(amount="How many messages should the bot remove?")
@has_permissions(manage_messages=True)
async def purge(Interaction: discord.Interaction, amount: int):
    embed=discord.Embed(
        title="Success",
        description=f"Successfully purged {amount} messages.",
        color=0x00A8FB
    )
    embed.set_author(name=Interaction.user.name, icon_url=Interaction.user.avatar.url)
    await Interaction.channel.purge(limit=int(amount) +1)
    await Interaction.response.send_message(embed=embed, ephemeral=True)
@purge.error
async def purge_error(Interaction, error):
    if isinstance (error, MissingPermissions):
        embed=discord.Embed(
            title="Insufficient permissions",
            description="This command requries `MANAGE_MESSAGES` permission.",
            color=discord.Colour.red()
        )
        await Interaction.response.send_message(embed=embed)

@client.command()
@has_permissions(manage_messages=True)
async def purge(ctx, amt):
    await ctx.channel.purge(limit=int(amt) + 1)
    embed = discord.Embed(
        title="Success.",
        description=f"Successfully purged {amt} messages.",
        color=0x00A8FB
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await asyncio.sleep(5)
    await ctx.send(embed=embed)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, MissingPermissions):
        purge_error_message = discord.Embed(
            title="Error",
            description="This command requires `MANAGE_MESSAGES` permission.",
            color=discord.Colour.red()
        )
        await ctx.send(embed=purge_error_message)

@client.tree.command(name="ban", description="Permanently ban a member.")
@app_commands.describe(user="What user do you want to ban?", reason="What are they banned for?", message_user="Should the bot DM the user?")
@has_permissions(ban_members=True)
async def ban(Interaction: discord.Interaction, user: discord.Member, reason: str, message_user: bool):
    embed = discord.Embed(
        title=f"{user} successfully banned",
        color=0x00A8FB
    )
    embed.add_field(name="reason", value=reason)
    embed.add_field(name="Time", value="Permanent")
    embed.set_author(name=Interaction.user, icon_url=Interaction.user.avatar.url)
    dm_embed = discord.Embed(
        title=f"You were banned.",
        color=0x00A8FB
    )
    dm_embed.add_field(name="Server", value=Interaction.guild, inline=False)
    dm_embed.add_field(name="Server ID", value=Interaction.guild.id, inline=False)
    dm_embed.add_field(name="reason", value=f"{reason}", inline=False)
    dm_embed.set_footer(text="This is an automated message.")

    await user.ban(reason=reason)
    await Interaction.response.send_message(embed=embed)
    if message_user is True: await user.send(embed=dm_embed)


@ban.error
async def ban_error (Interaction, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
        title="Insufficient permissions.",
        description="This command requires `BAN_MEMBERS` permission.",
        color=discord.Colour.red()
    )
        await Interaction.response.send_message(embed=embed)

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, duration: int = None, *, reason="No reason provided"):
    embed = discord.Embed(
        title="User Banned",
        description=f"{member.mention} has been banned{' for ' + str(duration) + ' days' if duration else ''}.",
        color=0x00A8FB
    )
    embed.add_field(name="Reason", value=reason)
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)

    await member.ban(reason=reason)
    await ctx.send(embed=embed)
    if duration:
        unban_task = asyncio.create_task(
            unban_after_duration(member, duration))
        client.unban_tasks[member.id] = unban_task
async def unban_after_duration(member, duration):
    await asyncio.sleep(duration * 86400)  # 86400 seconds in a day
    await member.guild.unban(member)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        ban_error_embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the `BAN_MEMBERS` permission to use this command.",
            color=discord.Colour.red()
        )
        await ctx.send(embed=ban_error_embed)

@client.tree.command(name="kick", description="kicks a member")
@app_commands.describe(user = "What user do you want to kick?", reason="What was the user kicked for?", message_user = "Should the bot message the user?")
@has_permissions(kick_members = True)
async def kick(Interaction: discord.Interaction, user: Member, message_user: bool, reason: str):
    embed=discord.Embed(
        title=f"User successfully kicked.",
        description=f"{user} has been kicked.",
        color=0x00A8FB
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_author(name=Interaction.user, icon_url=Interaction.user.avatar.url)
    dm_embed = discord.Embed(
        title="You were kicked.",
        color=0x00A8FB
    )
    dm_embed.add_field(name="Reason:", value=reason, inline=False)
    dm_embed.add_field(name="Server:", value=Interaction.guild, inline=False)
    dm_embed.add_field(name="Server ID:", value=Interaction.guild.id, inline=False)
    dm_embed.set_footer(text="This is an automated message.")
    await Interaction.response.send_message(embed=embed)
    await user.kick(reason=reason)
    if message_user is True: 
        await user.send(embed=dm_embed)
    
@kick.error
async def kick_error(Interaction, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Insufficient permissions.",
            description="This command requires `KICK_MEMBERS` permission.",
            color=discord.Colour.red()
        )
        await Interaction.response.send_message(embed=embed)

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    embed = discord.Embed(
        title="User successfully kicked",
        description=f"{member} has been kicked.",
        color=0x00A8FB
    )
    embed.add_field(name="Reason", value=reason)
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)

    await member.kick(reason=reason)
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        error_embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the `KICK_MEMBERS` permission to use this command.",
            color=discord.Colour.red()
        )
        await ctx.send(embed=error_embed)

# Used to unban members when the time for their temporary ban is over.
client.unban_tasks = {}

client.run(TOKEN)  # Put in your bot token between ""
