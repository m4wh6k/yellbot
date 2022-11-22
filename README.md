# yellbot
Discord bot for the YELLING server

# Usage
- requires at least python 3.9 and pip
- `pip install -r requirements.txt`
- `yellbot.py` is the bot service entrypoint
- `DISCORD_BOT_TOKEN` must be set as an environment variable
- On port `8080` at the path `/health_check` the bot service runs a healthcheck
  endpoint
