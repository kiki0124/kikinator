import discord
from discord.ext import commands
from discord.ext.commands import has_guild_permissions, MissingPermissions, Group, has_permissions, bot_has_permissions, BotMissingPermissions
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

    @commands.hybrid_command(name="avatar", description="Get the avatar of a user")
    @app_commands.describe(user="The avatar of what user?")
    async def avatar(self, ctx,  user: Optional[Member] = None):
        user = ctx.author if user is None else user
        embed = discord.Embed(
            title=f"Avatar for {user}.",
            color=0x00A8FB
        )
        embed.set_image(url=user.avatar.url)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="banner", description="Get the banner of a user.")
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

    @commands.hybrid_command(name='coinflip', description="Flip a coin!")
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

    @commands.hybrid_command(name="serverinfo", description="Gives information about the current server.")
    async def serverinfo(self, ctx):
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
        embed = discord.Embed(
            title=f'Member count for {ctx.guild.name}',
            description=f'**Members** {ctx.guild.member_count}',
            color=0x00A8FB
        )
        await ctx.reply(embed=embed)

async def setup(client):
  await client.add_cog(utility(client))
