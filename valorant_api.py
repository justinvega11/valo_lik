import aiohttp
import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()
Riot_API = os.getenv("Riot_API")

async def get_puuid(username,tag):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}"
        headers = {
            "Authorization": Riot_API 
        }

        async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    puuid = data["data"]["puuid"]
                    print(f"Current return of PUUID {puuid}, Return type: {type(puuid)}")
                    return puuid
                else:
                    print(f"Error: {response.status}, {await response.text()}")
                    return None
            