# == kang from https://github.com/lostb053/Userge-Plugins/tree/dev/plugins/utils/iytdl

import re
import os
import json
import wget

from iytdl import main
from uuid import uuid4
from re import compile as comp_regex

from pyrogram import filters
from pyrogram.errors import MediaEmpty, MessageIdInvalid, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InlineQuery, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent

from userge import Message, config as Config, userge
from userge.utils import get_response
from ...builtin import sudo

YOUTUBE_REGEX = comp_regex(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")


if userge.has_bot:
    def check_owner(func):
        async def wrapper(_, c_q: CallbackQuery):
            if c_q.from_user and c_q.from_user.id in (list(Config.OWNER_ID) + list(sudo.USERS)):
                try:
                    await func(c_q)
                except MessageNotModified:
                    await c_q.answer("Nothing Found to Refresh 🤷‍♂️", show_alert=True)
                except MessageIdInvalid:
                    await c_q.answer("Sorry, I Don't Have Permissions to edit this 😔",
                                     show_alert=True)
            else:
                user_dict = await userge.bot.get_user_dict(Config.OWNER_ID[0])
                await c_q.answer(
                    f"Only {user_dict['flname']} Can Access this...! Build Your Own @TheUserge 🤘",
                    show_alert=True)
        return wrapper

    ytdl = main.iYTDL(Config.LOG_CHANNEL_ID,
                      download_path="userge/plugins/utils/iytdl/")

    regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
    YT_DB = {}

    def rand_key():
        return str(uuid4())[:8]

    @userge.bot.on_inline_query(
        filters.create(
            lambda _, __, inline_query: (
                inline_query.query
                and inline_query.query.startswith("ytdl ")
                and inline_query.from_user
                and inline_query.from_user.id in Config.OWNER_ID
            ),
            # https://t.me/UserGeSpam/359404
            name="YtdlInline"
        ),
        group=-2
    )
    async def inline_iydl(_, inline_query: InlineQuery):
        query = inline_query.query.split("ytdl ")[1].strip()
        match = regex.match(query)
        results = []
        found_ = True
        if match is None:
            search_key = rand_key()
            YT_DB[search_key] = query
            search = await main.VideosSearch(query).next()
            try:
                i = search['result'][0]
            except IndexError:
                found_ = False
            out = f"<b><a href={i['link']}>{i['title']}</a></b>"
            title_ = i['title']
            thumb = i["thumbnails"][1 if len(
                        i["thumbnails"]) > 1 else 0]["url"].split("?")[0]
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"1/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|1")
                    ],
                    [
                        InlineKeyboardButton(
                            "Download", callback_data=f"yt_gen|{i['id']}")
                    ]
                ]
            )
        else:
            key = match.group("id")
            x = await main.Extractor().get_download_button(key)
            rand = rand_key()
            img = wget.download(x.image_url, out=f"{rand}.png")
            title_ = query
            thumb = f"{rand}.png"
            btn = x.buttons
            out = x.caption
        if found_:
            results.append(
                InlineQueryResultPhoto(
                    photo_url=thumb,
                    title=title_,
                    description="click to download",
                    caption=out,
                    reply_markup=btn,
                )
            )
        else:
            results.append(
                InlineQueryResultArticle(
                    title="not Found",
                    input_message_content=InputTextMessageContent(
                        f"Nenhum resultado encontrado para `{query}`"
                    ),
                    description="INVALID",
                )
            )
        await inline_query.answer(
            results=results,
            cache_time=5
        )
        inline_query.stop_propagation()


    @userge.on_cmd("iytdl", about={
        'header': "Advanced YTDL",
        'usage': "{tr}iytdl URL or Query"})
    async def iytdl_ub_cmd(m: Message):
        query = m.input_str
        match = regex.match(query)
        if match is None:
            search_key = rand_key()
            YT_DB[search_key] = query
            search = await main.VideosSearch(query).next()
            i = search['result'][0]
            out = f"<b><a href={i['link']}>{i['title']}</a></b>"
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"1/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|1")
                    ],
                    [
                        InlineKeyboardButton(
                            "Download", callback_data=f"yt_gen|{i['id']}")
                    ]
                ]
            )
            try:
                await userge.bot.send_photo(m.chat.id, i["thumbnails"][1 if len(i["thumbnails"]) > 1 else 0]["url"].split("?")[0], caption=out, reply_markup=btn)
            except MediaEmpty:
                await userge.bot.send_photo(m.chat.id, "https://camo.githubusercontent.com/8486ea960b794cefdbbba0a8ef698d04874152c8e24b3b26adf7f50847d4a3a8/68747470733a2f2f692e696d6775722e636f6d2f51393443444b432e706e67", caption=out, reply_markup=btn)
        else:
            key = match.group("id")
            x = await main.Extractor().get_download_button(key)
            rand = rand_key()
            img = wget.download(x.image_url, out=f"{rand}.png")
            await userge.bot.send_photo(m.chat.id, photo=f"{rand}.png", caption=x.caption, reply_markup=x.buttons)

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"ytdl_scroll\|(.*)"))
    @check_owner
    async def ytdl_scroll_callback(cq: CallbackQuery):
        callback = cq.data.split("|")
        search_key = callback[1]
        page = int(callback[2])
        query = YT_DB[search_key]
        search = await main.VideosSearch(query).next()
        i = search['result'][page]
        out = f"<b><a href={i['link']}>{i['title']}</a></b>"
        if page == 0:
            if len(search['result']) == 1:
                return await cq.answer("That's the end of list", show_alert=True)
            scroll_btn = [
                [
                    InlineKeyboardButton(
                        f"1/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|1")
                ]
            ]
        elif page == len(search['result'])-1:
            scroll_btn = [
                [
                    InlineKeyboardButton(
                        f"Back", callback_data=f"ytdl_scroll|{search_key}|{len(search['result'])-2}")
                ]
            ]
        else:
            scroll_btn = [
                [
                    InlineKeyboardButton(
                        f"Back", callback_data=f"ytdl_scroll|{search_key}|{page-1}"),
                    InlineKeyboardButton(
                        f"{page+1}/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|{page+1}")
                ]
            ]
        btn = [
            [
                InlineKeyboardButton(
                    "Download", callback_data=f"yt_gen|{i['id']}")
            ]
        ]
        btn = InlineKeyboardMarkup(scroll_btn+btn)
        try:
            await cq.edit_message_media(InputMediaPhoto(i["thumbnails"][1 if len(i["thumbnails"]) > 1 else 0]["url"].split("?")[0], caption=out), reply_markup=btn)
        except MediaEmpty:
            await cq.edit_message_media(InputMediaPhoto("https://camo.githubusercontent.com/8486ea960b794cefdbbba0a8ef698d04874152c8e24b3b26adf7f50847d4a3a8/68747470733a2f2f692e696d6775722e636f6d2f51393443444b432e706e67", caption=out), reply_markup=btn)

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"yt_(gen|dl)\|(.*)"))
    @check_owner
    async def ytdl_gendl_callback(cq: CallbackQuery):
        callback = cq.data.split("|")
        key = callback[1]
        if callback[0] == "yt_gen":
            x = await main.Extractor().get_download_button(key)
            rand = rand_key()
            img = wget.download(x.image_url, out=f"{rand}.png")
            try:
                await cq.edit_message_media(InputMediaPhoto(f"{rand}.png", caption=x.caption), reply_markup=x.buttons)
            except MediaEmpty:
                await cq.edit_message_media(InputMediaPhoto("https://camo.githubusercontent.com/8486ea960b794cefdbbba0a8ef698d04874152c8e24b3b26adf7f50847d4a3a8/68747470733a2f2f692e696d6775722e636f6d2f51393443444b432e706e67", caption=x.caption), reply_markup=x.buttons)
        else:
            uid = callback[2]
            type_ = callback[3]
            if type_ == "a":
                format_ = "audio"
            else:
                format_ = "video"
            upload_key = await ytdl.download("https://www.youtube.com/watch?v="+key, uid, format_, cq, True, 3)
            await ytdl.upload(userge.bot, upload_key, format_, cq, True)
