from os import getenv
from linebot import LineBotApi, WebhookHandler

# Manual Set up
LINE_BOT_API = LineBotApi(getenv("LINE_CHANNEL_ACCESS_TOKEN"))
HANDLER = WebhookHandler(getenv("LINE_CHANNEL_SECRET"))
GITHUB_NAME = getenv("GITHUB_NAME")

# Acquire by Creating and Connecting Neon Database
DATABASE_URL = getenv("DATABASE_URL")
