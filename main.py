import asyncio
import json
import time

from aiogram import Bot, Dispatcher
import websockets
import os

from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv



load_dotenv()
bot = Bot(token=os.environ.get('BOT_TOKEN'))
user_id = os.environ['USER_ID']

dp = Dispatcher()

binance_url = 'wss://fstream.binance.com/stream?streams=btcusdt@aggTrade/ethusdt@aggTrade'

last_sent_time = 0
prices = {'btcusdt@aggTrade' : 0,
          'ethusdt@aggTrade' : 0}

@dp.message(CommandStart())
async def get_start(message: Message):
    user_id = message.from_user.id
    await message.answer(text=f'{user_id=}')




async def fetch_binance_trades(url: str):
    global last_sent_time
    last_sent_time = time.time()
    async with websockets.connect(url) as ws:
        async for msg in ws:
            data = json.loads(msg)
            prices[data['stream']] = data['data']['p']
            if time.time() - last_sent_time > 5:
                await send_message_to_tg(
                    msg=f'Текущие цены: {prices["btcusdt@aggTrade"]=}, {prices["ethusdt@aggTrade"]=}',
                )
                last_sent_time = time.time()

async def send_message_to_tg(msg:str):
    await bot.send_message(
        chat_id=user_id,
        text=msg,
    )


async def main():
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(fetch_binance_trades(binance_url))
        task_group.create_task(dp.start_polling(bot, handle_signals=False))


if __name__ == '__main__':
    asyncio.run(
        main()
    )