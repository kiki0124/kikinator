import discord
from discord.ext import commands
from discord import Member, TextChannel, app_commands
from discord.ext.commands import has_permissions, MissingPermissions, bot_has_permissions, BotMissingPermissions
import os
import asyncio
import datetime

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(name="kick", description="Kick a user from your server.")
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @app_commands.describe(user="What user do you want to kick?", reason="What is the reason for kicking this user?")
    async def kick(self, ctx: commands.Context, user: Member, reason: str):
        await ctx.defer()
        if user.id == ctx.author.id:
            embed = discord.Embed(
                title="There was a problem...",
                description="You cannot kick yourself.",
                color=discord.Color.orange()
            )
            await ctx.reply(embed=embed)
        elif user.id == ctx.guild.owner.id:
            embed = discord.Embed(
                title="Insufficient permissions.",
                color=discord.Color.orange(),
                description=f"You cannot kick {user.mention} because they are the owner of this server."
            )
            await ctx.reply(embed=embed)
        elif user.top_role >= ctx.guild.me.top_role:
            embed = discord.Embed(
                title="Insufficient bot permissions.",
                color=discord.Color.orange(),
                description="The bot's highest role needs to be above the highest role of the user you are trying to kick."
            )
            await ctx.reply(embed=embed, mention_author=False)
        elif user.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="Insufficient permissions.",
                description=f"{user.mention}'s highest role is your highest role or is higher than your highest role.",
                color=discord.Color.orange()
            )
            await ctx.reply(embed=embed)
        else:
            await user.kick(reason=reason)
            embed = discord.Embed(
                title=f"{user.name} successfully kicked.",
                color=0x00A8FB
            )
            embed.add_field(name="Reason:", value=reason)
            embed.add_field(name="User:", value=f"{user.mention} | {user.name} | {user.id}")
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
    
    @commands.hybrid_command(name="ban", description="Ban a user from your server.")
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @app_commands.describe(user="What user do you want to ban?", reason="What is the reason for banning this user?")
    async def ban(self, ctx: commands.Context, user: Member, reason: str):
        await ctx.defer()
        if user.id == ctx.author.id:
            embed = discord.Embed(
                title="There was a problem...",
                description="You cannot ban yourself.",
                color=discord.Color.orange()
            )
            await ctx.reply(embed=embed)
        elif user.id == ctx.guild.owner.id:
            embed = discord.Embed(
                title="Insufficient permissions.",
                color=discord.Color.orange(),
                description=f"You cannot ban {user.mention} because they are the owner of this server."
            )
            await ctx.reply(embed=embed)
        elif user.top_role >= ctx.guild.me.top_role:
            embed = discord.Embed(
                title="Insufficient bot permissions.",
                color=discord.Color.orange(),
                description="Kikinator's highest role needs to be above the highest role of the user you are trying to ban."
            )
            await ctx.reply(embed=embed, mention_author=False)
        elif user.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="Insufficient permissions.",
                description=f"{user.mention}'s highest role is your highest role or is higher than your highest role.",
                color=discord.Color.orange()
            )
            await ctx.reply(embed=embed)
        else:
            await user.ban(reason=reason)
            embed = discord.Embed(
                title=f"{user.name} successfully banned.",
                color=0x00A8FB
            )
            embed.add_field(name="Reason:", value=reason)
            embed.add_field(name="User:", value=f"{user.mention} | {user.name} | {user.id}")
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
          
    @commands.hybrid_command(name="purge", description="Purge up to 99 messages at a time using the bot.", aliases=["deletemessages", "delmsgs", "delmsg", "deletemsg", "deletemsgs", "clean", "clear"])
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    @app_commands.describe(amount="How many messages do you want to purge? maximum is 99.", channel="From what channel do you want to purge messages?")
    async def purge(self, ctx, amount: int, channel: discord.TextChannel = None):
        channel = ctx.channel if not channel else channel
        if amount >= 100:
            await ctx.reply(f"You tried to purge {amount} messages. the highest amount allowed at a time is 99.")
        elif amount <= 99:
            await channel.purge(limit=amount+1, reason=f"Purged by {ctx.author.name}")
            await asyncio.sleep(5)
            embed = discord.Embed(
                title='Purge successful.',
                description=f'Successfully purged {amount} messages from {channel.mention}.',
                color=0x00A8FB
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await asyncio.sleep(3)
            await channel.send(embed=embed)


async def setup(client):
    await client.add_cog(moderation(client))
