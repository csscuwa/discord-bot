from discord.ext import tasks, commands
import discord

import requests


class Door(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ping_door_status.start()
        self._session = requests.Session()
        self.current_door_status = None

        self.door_status_channel = self.bot.get_guild(293785967083651074).get_channel(961596047153573948)


    def cog_unload(self):
        self.ping_door_status.cancel()


    @tasks.loop(seconds=5.0)
    async def ping_door_status(self):
        json_data = self._session.get("https://portal.cssc.asn.au/api/door_status").json()
        door_status = int(json_data["door_status"])

        # Only send a message if the status has changed.
        if door_status != self.current_door_status:
            self.current_door_status = door_status
            await self.update_status()



    async def update_status(self):
        if self.current_door_status:
            await self.door_status_channel.send("Door Open")
        else:
            await self.door_status_channel.send("Door Closed")


    @ping_door_status.before_loop
    async def before_ping_door_status(self):
        json_data = self._session.get("https://dash.cssc.asn.au/api/door_status").json()
        self.current_door_status = json_data["door_status"]


async def setup(bot):
    await bot.add_cog(Door(bot))
