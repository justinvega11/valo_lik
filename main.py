import discord
import command_cog
from discord.ext import commands
from discord import app_commands
from discord.ui import View
import logging
from dotenv import load_dotenv
import os
import asyncio
import sys
import signal
import aiohttp


GUILD_ID = discord.Object(id=215291855686991873)


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(file_handler)

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())


@bot.event
async def on_ready():
    logger.info(f'Bot connected as {bot.user}')
    try:
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"synced {len(synced)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occured: ",e)


async def load():
    await bot.load_extension("command_cog")

async def main():
    async with bot:
        logger.info("Starting bot...")
        await load()
        logger.info("Loading bot...")
       # await bot.run(token,log_handler=handler,log_level=logging.DEBUG)
        try:
            await bot.start(token)
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt.")
        except discord.LoginFailure:
            logger.error("Invalid token provided.")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
        finally:
            if not bot.is_closed():
                await bot.close()
            logger.info("Bot has shut down.")


if __name__ == "__main__":
    try:
        # For proper signal handling
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Add signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: loop.stop())
        
        # Run the bot
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt.")
    except discord.LoginFailure:
        logger.error("Invalid token provided.")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        # Clean up
        if not bot.is_closed():
            loop.run_until_complete(bot.close())
        
        # Cancel all running tasks
        tasks = asyncio.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()
        
        # Run until all tasks are cancelled
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        
        # Close the loop
        loop.close()
        logger.info("Bot has shut down.")