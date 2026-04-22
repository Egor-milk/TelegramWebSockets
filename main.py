import asyncio
import json

from aiogram import Bot, Dispatcher
import websockets
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(
    token=BOT_TOKEN
)
dp = Dispatcher()

binance_url = 'wss://fstream.binance.com/ws/btcusdt@aggTrade'

async def fetch_binance_trades(url: str):
    async with websockets.connect(url) as ws:
        async for msg in ws:
            data = json.loads(msg)
            price = data['p']

async def send_message_to_tg(meg:str):
    


async def main():
    await fetch_binance_trades(binance_url)

if __name__ == '__main__':
    asyncio.run(
        main()
    )