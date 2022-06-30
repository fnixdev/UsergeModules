## == Modules Userge by fnix
#
# ==

import os
import random

from telegraph import upload_file
from userge import Message, get_collection, userge, versions as ver, config
from userge.versions import __python_version__


SAVED = get_collection("ALIVE_DB")

ALIVE_MSG = {}

async def _init():
    global ALIVE_MEDIA, ALIVE_MSG  # pylint: disable=global-statement
    link = await SAVED.find_one({"_id": "ALIVE_MEDIA"})
    if link:
        ALIVE_MEDIA = link["link"]
    _AliveMsg = await SAVED.find_one({"_id": "CUSTOM_MSG"})
    if _AliveMsg:
        ALIVE_MSG = _AliveMsg["data"]

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
    link_ = await upload_media_(message)
    media = f"https://telegra.ph{link_}"
    await SAVED.update_one(
            {"_id": "ALIVE_MEDIA"}, {"$set": {"link": media}}, upsert=True
        )
    await message.edit("`Alive Media definida com sucesso!`", del_in=5, log=True)


@userge.on_cmd(
    "setamsg",
    about={
        "header": "Define uma mensagem para alive",
        "description": "Voçê pode definir uma mensagem para aparecer em seu Alive",
    },
)
async def save_msg_alive(message: Message):
    """set alive msg"""
    rep = message.input_or_reply_raw
    if not rep:
        return await message.edit("`Você precisa digitar ou responder a uma mensagem pra salva-la`", del_in=6)
    if len(rep) > 500:
        return await message.edit("`Essa mensagem é muito longa, o limite é de 500 caracteres.`", del_in=5)
    try:
        await SAVED.update_one(
            {"_id": "ALIVE_MSG"}, {"$set": {"data": rep}}, upsert=True
        )
        await message.edit("`Mensagem para alive definida com sucesso!`", del_in=5, log=True)
    except Exception as e:
        await message.err(f"Invalid Syntax\n\n`{e}`")


@userge.on_cmd(
    "alive",
    about={
        "header": "Alive apenas",
    },
)
async def view_del_ani(message: Message):
    """new alive"""
    _findpma = await SAVED.find_one({"_id": "ALIVE_MEDIA"})
    _findamsg = await SAVED.find_one({"_id": "ALIVE_MSG"})
    if _findpma is None:
        media = "https://telegra.ph/file/8bfc66ff423f8263f8ca4.png"
    else:
        media = _findpma.get("link")
    if _findamsg is None:
        mmsg = random.choice(FRASES)
    else:
        mmsg = _findamsg.get("data")
    msg = "ᴏɪ ᴍᴇsᴛʀᴇ, ᴋᴀɴɴᴀx ɪ'ᴛs ᴀʟɪᴠᴇ"
    alive_msg = f"""
{msg}

{mmsg}

• **Modo** :  `{_get_mode()}`
• **Uptime**  :  `{userge.uptime}`
• **Bot Version**  :  `v{ver.__loader_version__}`
• **Python Version**  :  `v{ver.__python_version__}`

    ✨ [sᴜᴘᴏʀᴛᴇ ](https://t.me/fnixsup) | 👾 [ʀᴇᴘᴏ](https://github.com/fnixdev/Kanna-X)
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


@userge.on_cmd(
    "delamsg",
    about={
        "header": "Delete alive message",
        "description": "Retorna a mensagem de Alive「 para o padrão",
      },
)
async def del_a_msg(message: Message):
    """del msg alive"""
    _findamsg = await SAVED.find_one({"_id": "ALIVE_MSG"})
    if _findamsg is None:
        await message.edit("`Você ainda não definiu uma mensagem para Alive`", del_in=5)
    else:
        await SAVED.find_one_and_delete({"_id": "ALIVE_MSG"})
        await message.edit("`Alive msg excluida`", del_in=5, log=True)
 


async def upload_media_(message: Message):
    replied = message.reply_to_message
    if not (
        (replied.photo and replied.photo.file_size <= _T_LIMIT)
        or (replied.animation and replied.animation.file_size <= _T_LIMIT)
        or (
            replied.video
            and replied.video.file_name.endswith((".mp4", ".mkv"))
            and replied.video.file_size <= _T_LIMIT
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mkv")
            )
            and replied.document.file_size <= _T_LIMIT
        )
    ):
        await message.err("not supported!")
        return
    await message.edit("`processando...`")
    dl_loc = await message.client.download_media(
        message=message.reply_to_message,
        file_name=Config.DOWN_PATH,
        progress=progress,
        progress_args=(message, "tentando fazer download"),
    )
    await message.edit("`fazendo upload no telegraph...`")
    try:
        response = upload_file(dl_loc)
    except Exception as t_e:
        await message.err(t_e)
        return
    os.remove(dl_loc)
    return str(response[0])

FRASES = (
    "ʟᴇᴍʙʀᴇ-sᴇ ᴅᴀ ʟɪᴄ̧ᴀ̃ᴏ ᴇ ɴᴀ̃ᴏ ᴅᴀ ᴅᴇᴄᴇᴘᴄ̧ᴀ̃ᴏ.",
    "ᴠᴏᴄᴇ̂ ɴᴀ̃ᴏ ᴄᴏɴʜᴇᴄᴇ ᴀs ᴘᴇssᴏᴀs, ᴠᴏᴄᴇ̂ ᴄᴏɴʜᴇᴄᴇ ᴀᴘᴇɴᴀs ᴏ ǫᴜᴇ ᴇʟᴀs ᴘᴇʀᴍɪᴛᴇᴍ ǫᴜᴇ ᴠᴏᴄᴇ̂ ᴠᴇᴊᴀ.",
    "ᴀs ᴠᴇᴢᴇs ᴀs ǫᴜᴇsᴛᴏ̃ᴇs sᴀ̃ᴏ ᴄᴏᴍᴘʟɪᴄᴀᴅᴀs ᴇ ᴀs ʀᴇsᴘᴏsᴛᴀs sᴀ̃ᴏ sɪᴍᴘʟᴇs.",
    "ᴀᴍᴀʀ ᴀʟɢᴜᴇ́ᴍ ᴘʀᴏꜰᴜɴᴅᴀᴍᴇɴᴛᴇ ʟʜᴇ ᴅᴀ́ ꜰᴏʀᴄ̧ᴀ; sᴇʀ ᴀᴍᴀᴅᴏ ᴘʀᴏꜰᴜɴᴅᴀᴍᴇɴᴛᴇ ʟʜᴇ ᴅᴀ́ ᴄᴏʀᴀɢᴇᴍ.",
    "ᴠᴏᴄᴇ̂ ɴᴀ̃ᴏ ᴇ́ ᴅᴇʀʀᴏᴛᴀᴅᴏ ǫᴜᴀɴᴅᴏ ᴘᴇʀᴅᴇ, ᴍᴀs sɪᴍ ǫᴜᴀɴᴅᴏ ᴠᴏᴄᴇ̂ ᴅᴇsɪsᴛᴇ.",
    "ʜᴀ ᴍᴏᴍᴇɴᴛᴏs ǫᴜᴇ ᴠᴏᴄᴇ̂ ᴘʀᴇᴄɪsᴀ ᴅᴇsɪsᴛɪʀ ᴅᴇ ᴀʟɢᴜᴍᴀ ᴄᴏɪsᴀ ᴘᴀʀᴀ ᴘʀᴇsᴇʀᴠᴀʀ ᴀ ᴏᴜᴛʀᴀ.",
    "ᴀ ᴠɪᴅᴀ ᴅᴀs ᴘᴇssᴏᴀs ɴᴀ̃ᴏ ᴀᴄᴀʙᴀ ǫᴜᴀɴᴅᴏ ᴇʟᴀs ᴍᴏʀʀᴇᴍ, ᴍᴀs sɪᴍ ǫᴜᴀɴᴅᴏ ᴘᴇʀᴅᴇᴍ ᴀ ꜰᴇ́.",
    "sᴇ ᴠᴏᴄᴇ̂ ᴇsᴛᴀ́ ᴠɪᴠᴏ ᴘᴏᴅᴇ ʀᴇᴄᴏᴍᴇᴄ̧ᴀʀ. ɴɪɴɢᴜᴇ́ᴍ ᴛᴇᴍ ᴏ ᴅɪʀᴇɪᴛᴏ ᴅᴇ ᴛᴇ ᴛɪʀᴀʀ ɪssᴏ.",
    "ᴏ ᴘᴇssɪᴍɪsᴍᴏ, ᴅᴇᴘᴏɪs ᴅᴇ ᴠᴏᴄᴇ̂ sᴇ ᴀᴄᴏsᴛᴜᴍᴀʀ ᴀ ᴇʟᴇ, ᴇ́ ᴛᴀ̃ᴏ ᴀɢʀᴀᴅᴀ́ᴠᴇʟ ǫᴜᴀɴᴛᴏ ᴏ ᴏᴛɪᴍɪsᴍᴏ.",
    "ᴘᴇʀᴅᴏᴀʀ ᴇ́ ʟɪʙᴇʀᴛᴀʀ ᴏ ᴘʀɪsɪᴏɴᴇɪʀᴏ... ᴇ ᴅᴇsᴄᴏʙʀɪʀ ǫᴜᴇ ᴏ ᴘʀɪsɪᴏɴᴇɪʀᴏ ᴇʀᴀ ᴠᴏᴄᴇ̂.",
    "ᴛᴜᴅᴏ ᴏ ǫᴜᴇ ᴜᴍ sᴏɴʜᴏ ᴘʀᴇᴄɪsᴀ ᴇ́ ᴀʟɢᴜᴇ́ᴍ ǫᴜᴇ ᴀᴄʀᴇᴅɪᴛᴇ ǫᴜᴇ ᴇʟᴇ ᴘᴏssᴀ sᴇʀ ʀᴇᴀʟɪᴢᴀᴅᴏ.",
    "ɴᴀ̃ᴏ ᴇsᴘᴇʀᴇ ᴘᴏʀ ᴜᴍᴀ ᴄʀɪsᴇ ᴘᴀʀᴀ ᴅᴇsᴄᴏʙʀɪʀ ᴏ ǫᴜᴇ ᴇ́ ɪᴍᴘᴏʀᴛᴀɴᴛᴇ ᴇᴍ sᴜᴀ ᴠɪᴅᴀ.",
    "ᴏ ᴘᴇssɪᴍɪsᴍᴏ, ᴅᴇᴘᴏɪs ᴅᴇ ᴠᴏᴄᴇ̂ sᴇ ᴀᴄᴏsᴛᴜᴍᴀʀ ᴀ ᴇʟᴇ, ᴇ́ ᴛᴀ̃ᴏ ᴀɢʀᴀᴅᴀ́ᴠᴇʟ ǫᴜᴀɴᴛᴏ ᴏ ᴏᴛɪᴍɪsᴍᴏ.",
    "ᴅᴇsᴄᴏʙʀɪʀ ᴄᴏɴsɪsᴛᴇ ᴇᴍ ᴏʟʜᴀʀ ᴘᴀʀᴀ ᴏ ǫᴜᴇ ᴛᴏᴅᴏ ᴍᴜɴᴅᴏ ᴇsᴛᴀ́ ᴠᴇɴᴅᴏ ᴇ ᴘᴇɴsᴀʀ ᴜᴍᴀ ᴄᴏɪsᴀ ᴅɪꜰᴇʀᴇɴᴛᴇ.",
    "ɴᴏ ꜰᴜɴᴅᴏ ᴅᴇ ᴜᴍ ʙᴜʀᴀᴄᴏ ᴏᴜ ᴅᴇ ᴜᴍ ᴘᴏᴄ̧ᴏ, ᴀᴄᴏɴᴛᴇᴄᴇ ᴅᴇsᴄᴏʙʀɪʀ-sᴇ ᴀs ᴇsᴛʀᴇʟᴀs.",
)