import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from commands import register_user_commands
from bot.commands.bot_commands import bot_commands
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas
from sqlalchemy.engine import URL

TOKEN = "5408582460:AAF4gX76bUMQIpf4YD1ycynOenAFzET3JbU"

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

        dp = Dispatcher()
    bot = Bot(TOKEN)
    await bot.set_my_commands(commands=commands_for_bot)
    register_user_commands(dp)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username='aiogram_user',
        host='localhost',
        password='alerusford',
        database='aiogram_db',
        port=5432,

    )
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(' - bot stopped.')
