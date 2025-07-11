import os

import yaml
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

with open(os.getenv('YML_CONF')) as yam:
    YAML = yaml.safe_load(yam)

BOT_TOKEN = YAML['telegram']['bot_token']
POSTBACK_CHANNEL_ID = YAML['telegram']['postback_channel']
ADMIN_ID = YAML['telegram']['admin_id']
MINIAPP_URL = YAML['telegram']['miniapp_url']
CHANNEL_URL = YAML['telegram']['link']

LANGUAGES = ["ru", "en"]

IMG_START=os.getenv('IMG_START')
OPEN_SOFT=os.getenv('OPEN_SOFT')
CHANGE_LANG=os.getenv('CHANGE_LANG')
INSTRUCTION=os.getenv('INSTRUCTION')
MAIN_MENU=os.getenv('MAIN_MENU')

WEBHOOK_DOMAIN = YAML['telegram']['webhook']['domain']
WEBHOOK_PATH = YAML['telegram']['webhook']['path']
WEBAPP_PORT=YAML['telegram']['webapp']['port']
WEBAPP_HOST=YAML['telegram']['webapp']['host']
MINIAPP_LINK = YAML['telegram']['miniapp']['link']
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

DB_URL = f"sqlite:///{YAML['database']}"