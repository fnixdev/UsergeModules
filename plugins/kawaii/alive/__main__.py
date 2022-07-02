# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

import os
import asyncio

from random import choice

from pyrogram.errors import BadRequest, Forbidden
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultAnimation,
    InlineQueryResultArticle,
    InlineQueryResultPhoto
)

from userge import Message, get_collection, userge, versions as ver, config
from userge.utils import upload_media_tg


SAVED = get_collection("ALIVE_DB")


@userge.on_cmd("alive", about={"header": "Just For Fun"}, allow_channels=False)
async def alive_inline(message: Message):
    try:
        if message.client.is_bot:
            await send_alive_message(message)
        elif userge.has_bot:
            try:
                await send_inline_alive(message)
            except BadRequest:
                await send_alive_message(message)
        else:
            await send_alive_message(message)
    except Exception as e_all:
        await message.err(str(e_all), del_in=10, log=__name__)


@userge.on_cmd(
    "setalive",
    about={
        "header": "Set alive media",
        "description": "you can set custom alive media",
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
            return await message.edit("`no media has been defined yet.`", del_in=5)
        await SAVED.delete_one({"_id": "ALIVE_MEDIA"})
        return await message.edit("`alive media reseted.`", del_in=5)
    replied = message.reply_to_message
    if not replied:
        return await message.err("`Reply to a photo/gif/video to set an Alive Media.`")
    link_ = await upload_media_tg(message)
    media = f"https://telegra.ph{link_}"
    await SAVED.update_one(
            {"_id": "ALIVE_MEDIA"}, {"$set": {"link": media}}, upsert=True
        )
    await message.edit("`Alive Media set successfully!`", del_in=5, log=True)


if userge.has_bot:
    @userge.bot.on_inline_query(
        filters.create(
            lambda _, __, inline_query: (
                inline_query.query
                and inline_query.query.startswith("alive")
                and inline_query.from_user
                and inline_query.from_user.id in config.OWNER_ID
            ),
            name="AliveFilter"
        ),
        group=-1
    )
    async def inline_alive(_, inline_query: InlineQuery):
        results = []
        media = await _get_media()
        buttons = Bot_Alive.alive_buttons()
        alive_info = await Bot_Alive.alive_info()
        if media.endswith((".gif", ".mp4")):
            results.append(
                InlineQueryResultAnimation(
                    animation_url=media,
                    caption=alive_info,
                    reply_markup=buttons,
                )
            )
        else:
            results.append(
                InlineQueryResultPhoto(
                    photo_url=media,
                    caption=alive_info,
                    reply_markup=buttons,
                )
            )
        await inline_query.answer(
            results=results,
            cache_time=5
        )
        inline_query.stop_propagation()


async def send_alive_message(message: Message) -> None:
    global _USER_CACHED_MEDIA, _BOT_CACHED_MEDIA
    chat_id = message.chat.id
    client = message.client
    caption = await Bot_Alive.alive_info()
    if client.is_bot:
        reply_markup = Bot_Alive.alive_buttons()
    else:
        reply_markup = None
    media = await _get_media()
    if media.endswith((".gif", ".mp4")):
        await client.send_animation(
            chat_id,
            animation=media,
            caption=caption,
            reply_markup=reply_markup,
        )
    else:
        await client.send_photo(
            chat_id,
            photo=media,
            caption=caption,
            reply_markup=reply_markup,
        )


async def send_inline_alive(message: Message) -> None:
    _bot = await userge.bot.get_me()
    try:
        i_res = await userge.get_inline_bot_results(_bot.username, "alive")
        i_res_id = (
            (
                await userge.send_inline_bot_result(
                    chat_id=message.chat.id,
                    query_id=i_res.query_id,
                    result_id=i_res.results[0].id,
                )
            )
            .updates[0]
            .id
        )
    except (Forbidden, BadRequest) as ex:
        await message.err(str(ex), del_in=5)
        return
    await message.delete()
    await asyncio.sleep(200)
    await userge.delete_messages(message.chat.id, i_res_id)

async def _get_media() -> str:
    alive_media = await SAVED.find_one({"_id": "ALIVE_MEDIA"})
    if alive_media is None:
        media = choice(ALIVE_DEFAULT)
    else:
        media = alive_media["link"]
    return media


def _get_mode() -> str:
    if userge.dual_mode:
        return "Dual"
    if config.BOT_TOKEN:
        return "Bot"
    return "User"


class Bot_Alive:
    @staticmethod
    async def alive_info() -> str:
        alive_info_ = f"""
╭────────ꕥ Hilzu ꕥ────────
│✾ 𝚖𝚘𝚍𝚎 :  `{_get_mode()}`
│✾ 𝚞𝚙𝚝𝚒𝚖𝚎  :  `{userge.uptime}`
│✾ 𝙷𝚒𝚕𝚣𝚞 𝚅𝚎𝚛𝚜𝚒𝚘𝚗  :  `v{ver.__hilzu_version__}`
│✾ 𝙿𝚢𝚝𝚑𝚘𝚗 𝚅𝚎𝚛𝚜𝚒𝚘𝚗  :  `v{ver.__python_version__}`
╰❑

    ✾ [𝚛𝚎𝚙𝚘](https://github.com/fnixdev/Hilzu) | ✾ [𝚜𝚞𝚙𝚙𝚘𝚛𝚝 ](https://t.me/fnixsup)
"""
        return alive_info_

    @staticmethod
    def alive_buttons() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text="⚙️  𝚌𝚘𝚗𝚏𝚒𝚐", callback_data="settings_btn"),
                InlineKeyboardButton(
                    text="🦋  𝚜𝚝𝚊𝚝𝚞𝚜", callback_data="status_alive"),
            ]
        ]
        return InlineKeyboardMarkup(buttons)


ALIVE_DEFAULT = [
    "https://telegra.ph/file/e9ee28f638a94725e17d9.gif",
    "https://telegra.ph/file/d50793d9b5b1efaff09dc.gif",
    "https://telegra.ph/file/fdb15844c42e0c0965375.mp4"
]
