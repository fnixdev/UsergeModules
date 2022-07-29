# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" nekos module """

import random

from userge import userge, Message
from userge.utils import get_response

API = "https://nekos.best/api/v2/"
CATEGORIES = [
    "baka",
    "bite",
    "blush",
    "bored",
    "cry",
    "cuddle",
    "dance",
    "facepalm",
    "feed",
    "happy",
    "highfive",
    "hug",
    "kiss",
    "laugh",
    "neko",
    "pat",
    "poke",
    "pout",
    "shrug",
    "slap",
    "sleep",
    "smile",
    "smug",
    "stare",
    "think",
    "thumbsup",
    "tickle",
    "wave",
    "wink",
    "kitsune",
    "waifu",
    "handhold",
    "kick",
    "punch",
    "shoot",
    "husbando",
    "yeet"
]


@userge.on_cmd(
    "neko",
    about={
        "header": "Get SFW stuff from nekos.best",
        "usage": "{tr}neko\n{tr}neko [Choice]",
        "✾ Choice": CATEGORIES,
    },
)
async def nekos_best(message: Message):
    """ get sfw nekos """
    query = message.input_str
    if query:
        lower_choice = str(query).lower()
        if lower_choice in CATEGORIES:
            choice = query
        else:
            await message.err("<code>Invalid input..</code>")
    else:
        choice = random.choice(CATEGORIES)
    reply = message.reply_to_message
    reply_id = reply.id if reply else None
    try:
        resp = await get_response.json(API+choice)
    except Exception:
        return await message.edit("<code>Fail to get image.</code>")
    link = resp["results"][0]["url"]
    if not message.client.is_bot:
        await message.delete()
    if link.endswith(".gif"):
        bool_unsave = not message.client.is_bot
        await message.client.send_animation(
            chat_id=message.chat.id,
            animation=link,
            unsave=bool_unsave,
            reply_to_message_id=reply_id,
        )
    else:
        await message.client.send_photo(
            chat_id=message.chat.id,
            photo=link,
            reply_to_message_id=reply_id
        )
