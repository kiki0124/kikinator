import discord
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands import MissingPermissions, Group, has_permissions, bot_has_permissions, BotMissingPermissions
from discord import Member, app_commands, TextChannel
import asyncio
import re
import traceback
import random
import requests
import json
import os
from typing import Optional

class utility(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(name="ping", description="Get the bot's response time.")
    async def ping(self, ctx):
        await ctx.reply(f"Pong! bot latency: {round(self.client.latency * 1000)}ms.")

    @commands.hybrid_command(name="avatar", description="Get the avatar of a user", aliases=["pfp", "useravatar", "profilepicture", "profilepic"])
    @app_commands.describe(user="The avatar of what user?")
    async def avatar(self, ctx,  user: Optional[Member] = None):
        user = ctx.author if user is None else user
        embed = discord.Embed(
            title=f"Avatar for {user}.",
            color=0x00A8FB
        )
        embed.set_image(url=user.avatar.url)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="banner", description="Get the banner of a user.", aliases=["userbanner"])
    @app_commands.describe(user="The banner of what user?")
    async def banner(self, ctx, user: Member = None):
        user = ctx.author if not user else user
        fetched_user = await self.client.fetch_user(user.id)
        if fetched_user.banner:
            embed = discord.Embed(
                title=f"Banner for {user.name}",
                color=0x00A8FB
            )
            embed.set_image(url=fetched_user.banner.url)
            await ctx.reply(embed=embed)
        elif not fetched_user.banner:
            await ctx.reply(f"The specified user `{user}` does not have a banner set or could not be found.")

    @commands.hybrid_command(name='coinflip', description="Flip a coin!", aliases=["flipacoin", "coin"])
    async def coinflip(self, ctx):
        string_list = ["heads", "tails"]
        embed = discord.Embed(
            title=f"It's {random.choice(string_list)}!",
            color=0x00A8FB
        )
        embed.set_image(url='https://cdnb.artstation.com/p/assets/images/images/052/459/869/original/jovo-arezina-coin-flip.gif?1659865199')
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        greetings_pattern = r'\b(hi|hey|hello|howdy|sup|yo)\b'
        if re.search(greetings_pattern, message.content, re.IGNORECASE):
            emoji = "<a:wave:1152496042286256198>"
            await message.add_reaction(emoji)
            await self.client.process_commands(message)

    @commands.hybrid_group(name="help", with_app_command=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title="Available commands.",
            description="Use /help moderation, /help utility or /help bot to get more specific information."
        )
        embed.add_field(name="Moderation commands:", value="`-Kick` Kicks a member from the guild. \n `-ban` Bans a member from the guild. \n `-purge` Quickly removes up to 99 messages. \n ", inline=False)
        embed.add_field(name="Utility commands:", value="`-userinfo` Get information about the specified user. \n`-avatar` Get the specified user's avatar. \n `-banner` Get the specified user's banner. \n `-serverinfo` Get information about the server. \n `-about` Get information about the bot and the bot's team. \n `-invite` Invite the bot to your server!. \n `-ping` Get the bot's latency.", inline=False)
        embed.add_field(name="Fun commands:", value="`-dadjoke` Get a random dad joke \n ")
        await ctx.reply(embed=embed)
    
    @help.command()
    async def moderation(self, ctx):
        embed = discord.Embed(
            title="Moderation commands.",
            color=0x00A8FB,
        )
        embed.add_field(name="`kick`", value="Kick a member from the guild, Use: `-kick @member reason`", inline=False)
        embed.add_field(name="ban", value="Bans a user from the guild,")
        await ctx.reply(embed=embed)


    @commands.hybrid_command(name='dadjoke', description="Get a dadjoke!")
    async def dadjoke(self, ctx):
        limit = 2
        api_url = 'https://api.api-ninjas.com/v1/dadjokes?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': ''})
    
        if response.status_code == requests.codes.ok:
            data = response.json()
            joke = data[0]['joke']
            await ctx.reply(joke)
        else:
            await ctx.reply(f"There was an error... {response.status_code}, {response.text}")

    @commands.hybrid_command(name="roleinfo", description="Gives information about the specified role!")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    @app_commands.describe(role="Information about what role do you want to get?")
    async def roleinfo(self, ctx, role: discord.Role):
        await ctx.defer()
        embed = discord.Embed(
            title="Role information",
            color=role.color
        )
        embed.add_field(name="Role:", value=role.mention, inline=False)
        embed.add_field(name="Name:", value=role.name, inline=False)
        embed.add_field(name="ID:", value=f"`{role.id}`", inline=False)
        embed.add_field(name="Color:", value=role.color, inline=False)
        embed.add_field(name="Members", value=len(role.members), inline=False)
        embed.add_field(name="Created at:", value=f"<t:{int(role.created_at.timestamp())}:F> (<t:{int(role.created_at.timestamp())}:R>)", inline=False)
        embed.add_field(name="Hoisted", value=role.hoist, inline=False)
        embed.add_field(name="Position:", value=role.position, inline=False)
        if role.icon:
            embed.set_image(url=role.icon.url)
        await ctx.reply(embed=embed)

    @roleinfo.error
    async def userinfo_error(self, ctx, error ):
        if isinstance(error, BotMissingPermissions):
            embed = discord.Embed(
                title="Insufficient bot permissions.",
                description="The bot needs to have `MANAGE_ROLES` permission for this command to work.",
                color=discord.Color.orange()
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="Insufficient permissions.",
                description="You need to have `MANAGE_ROLES` permission to be able to use this command.",
                color=0x00A8FB
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name="serverinfo", description="Gives information about the current server.", aliases=["guildinfo"])
    async def serverinfo(self, ctx):
        await ctx.defer()
        embed = discord.Embed(
            title=f'Info for {ctx.guild.name}',
            color=0x00A8FB
        )
        embed.add_field(name="Guild ID:", value=ctx.guild.id, inline=False)
        embed.add_field(name="Member count:", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Guild owner:", value=f"{ctx.guild.owner.name} ({ctx.guild.owner.mention}).", inline=False)
        embed.add_field(name="Created at:", value=f'<t:{int(ctx.guild.created_at.timestamp())}:F> (<t:{int(ctx.guild.created_at.timestamp())}:R>)', inline=False)
        embed.add_field(name="Roles:", value=len(ctx.guild.roles))
        embed.set_image(url=ctx.guild.icon)
        if ctx.guild.banner:
            embed.set_thumbnail(url=ctx.guild.banner)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="membercount", description="Get the member count of this server.")
    async def membercount(self, ctx):
        await ctx.defer()
        embed = discord.Embed(
            title=f'Member count for {ctx.guild.name}',
            description=f'**Members** {ctx.guild.member_count}',
            color=0x00A8FB
        )
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="userinfo", description="Get information about a user.")
    @app_commands.describe(user="Information about what user?")
    async def userinfo(self, ctx, user: Member = None):
        await ctx.defer()
        user = ctx.author if not user else user
        fetched_user = await self.client.fetch_user(user.id)
        embed = discord.Embed(
            title=f"Information for {user.name}",
            color=0x00A8FB
        )
        embed.add_field(name="User:", value=f"{user.name} ({user.mention})", inline=False)
        embed.add_field(name="User ID:", value=user.id, inline=False)
        embed.add_field(name="Bot?", value=user.bot, inline=False)
        embed.add_field(name="Created at:", value=f'<t:{int(user.created_at.timestamp())}:F> (<t:{int(user.created_at.timestamp())}:R>)', inline=False)
        if user in ctx.guild.members:
            embed.add_field(name="Joined at:", value=f"<t:{int(user.joined_at.timestamp())}:F> (<t:{int(user.joined_at.timestamp())}:R>)", inline=False)
        embed.set_image(url=user.avatar.url)
        if fetched_user.banner:
            embed.set_thumbnail(url=fetched_user.banner.url)
        await ctx.reply(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply("User could not be found.")

    @commands.hybrid_command(name="about", description="Get information about the bot!")
    async def about(self, ctx):
        await ctx.defer()
        embed = discord.Embed(
            title='Bot information.',
            color=0x00A8FB
        )
        embed.add_field(name="Development:", value="[kiki124](https://kiki124.vercel.app)")
        embed.add_field(name="Server:", value="https://discord.gg/zkbPFwwzVJ")
        embed.add_field(name="Bot's github repository:", value="https://github.com/kiki0124/discord_bot")
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="invite", description="Invite the bot to your server!")
    async def invite(self, ctx):
        await ctx.defer()
        embed = discord.Embed(
            title=f"Invite the bot to your server!",
            description="Use [this link](https://discord.com/api/oauth2/authorize?client_id=1149388511590486057&permissions=8&scope=bot)",
            color=0x00A8FB
        )
        embed.set_footer(text=ctx.user.name, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

        @commands.hybrid_command(name="poll", description="Send a poll using the bot!")
    async def poll(self, ctx, question: str):
        await ctx.defer()
        embed = discord.Embed(
            title=f" New poll!",
            description=question,
            color=0x00A8FB
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        message = await ctx.reply(embed=embed)
        yes_emoji = "<:Yes:1087612813700239360>"
        no_emoji = "<:No:1087612645995204648>"
        await message.add_reaction(yes_emoji)
        await message.add_reaction(no_emoji)

    @commands.hybrid_group(name="afk", with_app_command=True)
    async def afk(self, ctx: commands.Context):
        await ctx.reply(f"Wrong command... Use </afk set:1201855045721661500> or </afk remove:1201855045721661500>.")
    
    @afk.command(name="set", description="Set a custom AFK status.")
    @app_commands.describe(status="What do you want your custom status to be?")
    async def set(self, ctx: commands.Context, status: str):
        if ctx.author.id not in afk_dict:
            data = {"status": status, "timestamp": round(ctx.message.created_at.timestamp())}
            afk_dict[ctx.author.id] = data
            embed = discord.Embed(
                title="AFK status saved!",
                description=f"Successfully saved your custom AFK status as `{status}`",
                color=0x00A8FB
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
        elif ctx.author.id in afk_dict:
            await ctx.reply("You are already AFK... Use </afk remove:1201855045721661500> to remove your AFK status.")
    
    @afk.command(name="remove", description="Remove your AFK status.")
    async def remove(self, ctx: commands.Context):
        if ctx.author.id in afk_dict:
            afk_dict.pop(ctx.author.id)
            await ctx.reply("Successfully removed your custom afk status.")
        elif ctx.author.id not in afk_dict:
            await ctx.reply("You are not currently afk...")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            if not message.content.startswith("-"):
                if message.author.id in afk_dict:
                    afk_dict.pop(message.author.id)
                    await message.reply("You are no longer AFK!")
                elif message.mentions:
                    for User in message.mentions:
                        if User.id in afk_dict:
                            timestamp = afk_dict[User.id]["timestamp"]
                            status = afk_dict[User.id]["status"]
                            nickname = User.nick
                            if not User.nick:
                                nickname = User.name
                            embed = discord.Embed(
                                title=f"User is currently AFK.",
                                description=f"[{nickname}](https://discordapp.com/users/{User.id}) is AFK since <t:{timestamp}:R> (<t:{timestamp}:f>).",
                                color=0x00A8FB
                            )
                            embed.set_footer(text=message.author.name, icon_url=message.author.avatar.url)
                            embed.add_field(name="Status:", value=status, inline=False)
                            await message.reply(embed=embed)
                        else:
                            return
            elif message.content.startswith('-'):
                return
        elif message.author.bot == True:
            return
        await self.client.process_commands(message)
        
async def setup(client):
  await client.add_cog(utility(client))
