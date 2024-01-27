import discord
from discord.ext import commands
from discord import Webhook
import datetime
from discord import ui
from discord.interactions import Interaction

class BugReportModal(ui.Modal, title="Bug report."):
    feature = ui.TextInput(label="For what feature is this bug report?", required=True, style=discord.TextStyle.short, placeholder="Moderation.")
    recreation = ui.TextInput(label="Re-Creation steps:", style=discord.TextStyle.long, required=True, min_length=1, placeholder="Ban a user using the bot and wait for it to send the info message.")
    expected_results = ui.TextInput(label="Expected results:", required=True, style=discord.TextStyle.long, placeholder="The bot is supposed to ban the user and send a message with some information about the ban.")
    actual_results = ui.TextInput(label='Actual results:', required=True, style=discord.TextStyle.long, placeholder="The bot sends the info message and immediately deletes it.")
    other_info = ui.TextInput(label="Any additional information you would like to add?", required=False, style=discord.TextStyle.long)
    async def on_submit(self, interaction: Interaction):
        webhook = Webhook.from_url(client=self.client, url='https://discord.com/api/webhooks/1191831095445045489/TBu5Io4ZUL4_6f4L5XEhBHt2K194oy7MTlOqWASJ2vhnn_tTFRDYFl2Dz4ctsidjC0x7')
        embed = discord.Embed(
            title="New bug report.",
            color=discord.Color.orange()
        )
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.add_field(name="Feature:", value=self.feature.value)
        embed.add_field(name="ReCreation:", value=self.recreation.value)
        embed.add_field(name="Expected results:", value=self.expected_results.value)
        embed.add_field(name="Actual results:", value=self.actual_results.value)
        if self.other_info:
            embed.add_field(name="Additional information:", value=self.other_info.value)
        await webhook.send(embed=embed)
        await interaction.response.send_message(content=f"Thank you {interaction.user.mention} for reporting this bug! it has been forwarded to the developers and will be fixed as soon as possible.", ephemeral=True)
    async def on_error(self, interaction: Interaction, error: Exception):
        await interaction.response.send_message('There was a problem... An automatic bug report was sent to the developer.')
        print(error)
    async def on_timeout(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Oops.. you were timeouted meaning you waited too long without inputting any value...", ephemeral=True)

class bot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_resume(self):
        webhook = Webhook.from_url(url='', client=self.client)
        current_time = datetime.datetime.utcnow()
        timestamp_unix = int(current_time.timestamp())
        await webhook.send(f"<t:{timestamp_unix}:f> Bot resumed. Logged in as {self.client.user.name}.")

    @app_commands.command(name="bug", description="Report a bug you found")
    async def bug(self, interaction: discord.Interaction):
        await interaction.reponse.defer(ephemeral=True)
        await interaction.response.send_modal(BugReportModal)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        webhook = Webhook.from_url(url="", client=self.client)
        embed = discord.Embed(
            title="New bot guild!",
            color=0x00A8FB
        )
        embed.add_field(name="Guild:", value=guild.name)
        embed.add_field(name="Guild ID:", value=guild.id)
        await webhook.send(embed=embed)

        @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"Command {commands.CommandNotFound} could not be found.")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Missing {commands.MissingRequiredArgument} argument. Please make sure to fill it so the command will work properly.")
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Insufficient permissions.",
                description=f"This command requires `{commands.MissingPermissions}` permission.",
                color=discord.Color.orange()
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Missing bot permissions.",
                description=f"Kikinator needs to have `{commands.BotMissingPermissions}` permission for this command to work.",
                color=discord.Color.orange()
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.UserNotFound):
            embed = discord.Embed(
                title="User not found",
                description="The specified user could not be found.",
                color=discord.Color.orange()
            )
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(bot(client))
