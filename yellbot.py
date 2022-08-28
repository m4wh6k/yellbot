#!/usr/bin/env python3
import logging
import os
import random
import yaml

import discord

logging.basicConfig(level=logging.DEBUG)

with open("whisper_responses.yml", "r") as file:
    whisper_responses: list = yaml.safe_load(file)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def handle_whispered_messages(message: discord.Message):
    """Handles messages that should be yelling in all caps but aren't.
    Responds by yelling at the user"""

    if message.content != message.content.upper():
        content = random.choice(whisper_responses)
        await message.channel.send(content)


@client.event
async def on_ready():
    logging.info(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    await handle_whispered_messages(message)


def main():
    try:
        token = os.environ["DISCORD_BOT_TOKEN"]
    except KeyError:
        logging.critical("DISCORD_BOT_TOKEN env var required but not defined")
        exit(1)
    client.run(token)


if __name__ == "__main__":
    main()
