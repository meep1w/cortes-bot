import os

import yaml
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

with open(os.getenv('YML_CONF')) as yam:
    YAML = yaml.safe_load(yam)

BOT_TOKEN = YAML['telegram']['bot_token']
POSTBACK_CHANNEL_ID = YAML['telegram']['postback_channel']
ADMIN_ID = YAML['telegram']['admin_id']

reflink = "https://1wcjlr.com/casino/list?open=register&p=rvcf"
promo_code = "C0RTES"

LANGUAGES = ["ru", "en"]
