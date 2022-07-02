# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

import os

from random import choice

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
