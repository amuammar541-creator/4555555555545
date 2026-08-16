"""
Main entry point for the Telegram Bot.
"""

import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import config
from app.bot.router import router
from app.database.database import init_database
from app.telegram.userbot_manager import UserbotManager
from app.utils.logger import setup_logging


async def main():
    """Main entry point for the application."""
    
    # Ensure required directories exist
    Path("data").mkdir(exist_ok=True)
    Path("exports").mkdir(exist_ok=True)
    Path("sessions").mkdir(exist_ok=True)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        await init_database()
        
        # Initialize bot
        logger.info("Initializing bot...")
        bot = Bot(token=config.BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        dp.include_router(router)
        
        # Initialize userbot (will be started when needed)
        logger.info("Userbot manager initialized")
        userbot_manager = UserbotManager()
        
        logger.info("Bot started successfully!")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
