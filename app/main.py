if __name__ == "__main__":
    import asyncio
    import logging

    from bot.start_bot import start_bot

    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())
