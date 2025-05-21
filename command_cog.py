import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, session
from database import SessionLocal
import crud
import aiohttp
import valorant_api
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
        db = SessionLocal()

        try:
            puuid = await valorant_api.get_puuid(username,tag)
            if puuid:

                user = crud.create_user(db,str(interaction.user.id),interaction.user.name,puuid, username,tag)
                await interaction.response.send_message(f"Username : {username} Tag: {tag}  has been added" )
            else:
                raise Exception("get puuid failed")
        finally:
            print("db closing in create user")
            db.close()

        


#    @commands.command()
#    async def get_riot_id(self, ctx,arg1,arg2):
#        await ctx.send(f"Username : {arg1} Tag: {arg2}")

async def setup(bot):
    await bot.add_cog(Client(bot))

