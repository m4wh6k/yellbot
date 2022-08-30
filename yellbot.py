#!/usr/bin/env python3
import asyncio
import logging
import os
import re
import random

import discord
import yaml
from aiohttp import web

logging.basicConfig(level=logging.INFO)

with open("whisper_responses.yml", "r") as file:
    whisper_responses: list = yaml.safe_load(file)

with open("unyellable_patterns.yml", "r") as file:
    unyellable_patterns: list = yaml.safe_load(file)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def handle_whispered_messages(message: discord.Message):
    """Handles messages that should be yelling in all caps but aren't.
    Responds by yelling at the user"""

    # Remove message content that can't be yelled
    yellable_msg_content = message.content
    for pattern in unyellable_patterns:
        yellable_msg_content = re.sub(pattern, yellable_msg_content)

    # See if message was yelled. Respond if not
    if yellable_msg_content != yellable_msg_content.upper():
        logging.info(f"Remaining content was not uppercase: {message.content}")
        response = random.choice(whisper_responses)
        await message.channel.send(response)


@client.event
async def on_ready():
    logging.info(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    await handle_whispered_messages(message)


async def health_check(request):
    """Generic health check endpoint"""
    return web.Response(text="OK")


app = web.Application()
app.add_routes([web.get("/health_check", health_check)])


def main():
    try:
        token = os.environ["DISCORD_BOT_TOKEN"]
    except KeyError:
        logging.critical("DISCORD_BOT_TOKEN env var required but not defined")
        exit(1)
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(token))
    web.run_app(app, port=8080, loop=loop)
    loop.run_until_complete()


if __name__ == "__main__":
    main()
