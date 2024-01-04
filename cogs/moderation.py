import discord
from discord.ext import commands
from discord import Member, TextChannel, app_commands
from discord.ext.commands import has_permissions, has_guild_permissions, MissingPermissions, bot_has_permissions, BotMissingPermissions
import os
import asyncio


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(name="kick", description="Kick a user from your server.")
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @app_commands.describe(user="What user do you want to kick?", reason="What is the reason for kicking this user?")
    async def kick(self, ctx, user: Member, reason: str):
        await user.kick(reason=reason)
        await ctx.reply(f"{user.name} ({user.mention}) successfully kicked. \n Reason: {reason} \n Author: {ctx.author.name} ({ctx.author.mention}).")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("Insufficient permissions. \n This command requires `KICK_MEMBERS` permission.")
        elif isinstance(error, BotMissingPermissions):
            await ctx.reply("The bot needs to have `KICK_MEMBERS` permission and have a role above the highest role of this user for you to be able to execute this command.")
        elif isinstance(error, discord.errors.NotFound):
            await ctx.reply(f"User could not be found. Please try again later.")
        
    @commands.hybrid_command(name="ban", description="Ban a user from your server.")
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @app_commands.describe(user="What user do you want to ban?", reason="What is the reason for banning this user?")
    async def ban(self, ctx, user: Member, reason: str = None):
        reason = None if not reason else reason
        await user.ban(reason=reason)
        embed = discord.Embed(
            title=f"User successfully banned.",
            color=0x00A8FB
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="Reason:", value=reason)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="Insufficient permissions.",
                description="This command requires `BAN_MEMBERS` permission.",
                color=discord.Color.orange()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.icon.url)
            await ctx.reply(embed=embed)
        elif isinstance(error, BotMissingPermissions):
            embed = discord.Embed(
                title="Insufficient permissions.",
                description=f"The bot requires `BAN_MEMBERS` permission, and it needs to have a role above the highest role of the user you are trying to ban.",
                color=discord.Color.orange()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
    
    @commands.hybrid_command(name="purge", description="Purge up to 99 messages at a time using the bot.")
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
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.channel.send(embed=embed)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="Insufficient permissions.",
                description="This command requires `MANAGE_MESSAGES` permission.",
                color=discord.Color.orange()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
        elif isinstance(error, BotMissingPermissions):
            embed = discord.Embed(
                title="Insufficient bot permissions.",
                description="The bot needs to have `MANAGE_MESSAGES` permission for you to be able to use this command.",
                color=discord.Color.orange()
                )
            await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(moderation(client))
