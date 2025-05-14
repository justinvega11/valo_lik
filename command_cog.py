import discord
from discord.ext import commands
from discord import app_commands

GUILD_ID = discord.Object(id=215291855686991873)


class Client(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"testing, {self.bot.user.name}")

    @commands.Cog.listener()
    async def shutdown(self):
        await self.bot.close()

        
    @app_commands.command(name="get_riot_id", description='Enter your riot name and tag:"username" "Tag" ex: "four inch curve" "NA1"')
    async def get_riot_id(self,interaction: discord.Interaction, username: str, tag: str):
        await interaction.response.send_message(f"Username : {username} Tag: {tag}")

#    @commands.command()
#    async def get_riot_id(self, ctx,arg1,arg2):
#        await ctx.send(f"Username : {arg1} Tag: {arg2}")

async def setup(bot):
    await bot.add_cog(Client(bot))

