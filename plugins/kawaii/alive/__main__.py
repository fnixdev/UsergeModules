## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

import os
import random

from userge import Message, get_collection, userge, versions as ver, config
from userge.utils import progress, upload_media_tg


SAVED = get_collection("ALIVE_DB")

ALIVE_MSG = {}

async def _init():
    global ALIVE_MEDIA, ALIVE_MSG  # pylint: disable=global-statement
    link = await SAVED.find_one({"_id": "ALIVE_MEDIA"})
    if link:
        ALIVE_MEDIA = link["link"]


def _get_mode() -> str:
    if userge.dual_mode:
        return "Dual"
    if config.BOT_TOKEN:
        return "Bot"
    return "User"

@userge.on_cmd(
    "setamedia",
    about={
        "header": "Set alive media",
        "description": "Voçê pode definir uma mídia para aparecer em seu Alive",
        "flags": {
            "-r": "reset alive media.",
        },
    },
)
async def ani_save_media_alive(message: Message):
    """set media alive"""
    found = await SAVED.find_one({"_id": "ALIVE_MEDIA"})
    if "-r" in message.flags:
        if not found:
            return await message.edit("`Nenhuma Media foi definida ainda.`", del_in=5)
        await SAVED.delete_one({"_id": "ALIVE_MEDIA"})
        return await message.edit("`Alive Media restaurada para o padrão.`", del_in=5)
    replied = message.reply_to_message
    if not replied:
        return await message.err("`Responda a uma foto/gif/video para definir uma Alive Media.`")
    link_ = await upload_media_tg(message)
    media = f"https://telegra.ph{link_}"
    await SAVED.update_one(
            {"_id": "ALIVE_MEDIA"}, {"$set": {"link": media}}, upsert=True
        )
    await message.edit("`Alive Media definida com sucesso!`", del_in=5, log=True)


@userge.on_cmd(
    "alive",
    about={
        "header": "Alive apenas",
    },
)
async def view_del_ani(message: Message):
    """new alive"""
    _findpma = await SAVED.find_one({"_id": "ALIVE_MEDIA"})
    if _findpma is None:
        media = "https://telegra.ph/file/d50793d9b5b1efaff09dc.gif"
    else:
        media = _findpma.get("link")
    alive_msg = f"""
╭────────ꕥ Hilzu ꕥ────────
│✾ 𝚖𝚘𝚍𝚎 :  `{_get_mode()}`
│✾ 𝚞𝚙𝚝𝚒𝚖𝚎  :  `{userge.uptime}`
│✾ 𝙷𝚒𝚕𝚣𝚞 𝚅𝚎𝚛𝚜𝚒𝚘𝚗  :  `v{ver.__hilzu_version__}`
│✾ 𝙿𝚢𝚝𝚑𝚘𝚗 𝚅𝚎𝚛𝚜𝚒𝚘𝚗  :  `v{ver.__python_version__}`
╰❑

    ✾ [𝚛𝚎𝚙𝚘](https://github.com/fnixdev/Hilzu) | ✾ [𝚜𝚞𝚙𝚙𝚘𝚛𝚝 ](https://t.me/fnixsup)
"""
    if media.endswith((".gif", ".mp4")):
        await message.client.send_animation(
            chat_id=message.chat.id,
            animation=media,
            caption=alive_msg
        )
    else:
        await message.client.send_photo(
            chat_id=message.chat.id, photo=media, caption=alive_msg
        )
    await message.delete()

