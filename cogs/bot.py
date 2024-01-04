import discord
from discord.ext import commands
from discord import Webhook
import datetime
from discord import ui
from discord.interactions import Interaction

class bot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_resume(self):
        webhook = Webhook.from_url(url='', client=self.client)
        current_time = datetime.datetime.utcnow()
        timestamp_unix = int(current_time.timestamp())
        await webhook.send(f"<t:{timestamp_unix}:f> Bot resumed. Logged in as {self.client.user.name}.")

    

async def setup(client):
    await client.add_cog(bot(client))
