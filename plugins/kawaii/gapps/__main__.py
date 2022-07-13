# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" gapps plugin """

import re

from bs4 import BeautifulSoup
from requests import get

from pyrogram import filters
from pyrogram.errors import MessageIdInvalid, MessageNotModified
from pyrogram.types import CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup

from userge import Message, userge, config as Config
from ...builtin import sudo

COMPILE = re.compile(r"(.*)[*]*\-arm")

@userge.on_cmd(
    "gapps", about={
        'header': "get latest google apps"
    }
)
async def latest_gapps(message: Message):
    """ get gapps """
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="11", callback_data="gapps_v|11.0"),
                InlineKeyboardButton(
                    text="12", callback_data="gapps_v|12.0"),
                InlineKeyboardButton(
                    text="12L", callback_data="gapps_v|12.1"),
            ]
        ]
    )
    if message.client.is_bot:
        await userge.bot.send_message(message.chat.id, "**Select gapps version**", reply_markup=reply_markup)
    else:
        await message.delete()
        username = (await userge.bot.get_me()).username
        x = await userge.get_inline_bot_results(username, "gapps")
        await userge.send_inline_bot_result(chat_id=message.chat.id, query_id=x.query_id, result_id=x.results[0].id)


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
                    f"Only {user_dict['flname']} Can Access this...! Build Your Own @fnixsup 🤘",
                    show_alert=True)
        return wrapper

    @userge.bot.on_inline_query(
        filters.create(
            lambda _, __, inline_query: (
                inline_query.query
                and inline_query.query.startswith("gapps")
                and inline_query.from_user
                and inline_query.from_user.id in Config.OWNER_ID
            ),
            name="InlineGapps"
        ),
        group=-2
    )
    async def inline_gap(_, inline_query: InlineQuery):
        results = [
            InlineQueryResultArticle(
                title="Gapps",
                input_message_content=InputTextMessageContent(
                    "**Select gapps version**"
                ),
                url="https://github.com/fnixdev/Hilzu",
                description="Get latest gapps",
                thumb_url="https://telegra.ph/file/aa2776cc8f104120d2e4a.jpg",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="11", callback_data="gapps_v|11.0"),
                            InlineKeyboardButton(
                                text="12", callback_data="gapps_v|12.0"),
                            InlineKeyboardButton(
                                text="12L", callback_data="gapps_v|12.1"),
                        ]
                    ]
                )
            )
        ]
        await inline_query.answer(results=results, cache_time=3)

    # ==  Sector select gapps version

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"gapps_v\|(.*)"))
    @check_owner
    async def gapps_filter_cq(cq: CallbackQuery):
        cb = cq.data.split("|")
        version = cb[1]
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="Flame Gapps", callback_data=f"gapps_flame|{version}"),
                InlineKeyboardButton(
                    text="Nik Gapps", callback_data=f"gapps_nik|{version}"),
            ],
            [
                InlineKeyboardButton(
                    text="Back", callback_data="gapps_main"),
            ]
        ])
        await cq.edit_message_text(text=f"**Select your preferred gapps for {version}**", reply_markup=buttons)


    # ==  Sector select gapps variant

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"gapps_(flame|nik)\|(.*)"))
    @check_owner
    async def gapps_filter_cq(cq: CallbackQuery):
        cb = cq.data.split("|")
        version = cb[1]
        if cb[0] == "gapps_flame":
            if version == "11.0":
                link = "https://sourceforge.net/projects/flamegapps/files/arm64/android-11/"
            elif version == "12.0":
                link = "https://sourceforge.net/projects/flamegapps/files/arm64/android-12/"
            elif version == "12.1":
                link = "https://sourceforge.net/projects/flamegapps/files/arm64/android-12.1/"

        elif cb[0] == "gapps_nik":
            if version == "11.0":
                link = "https://sourceforge.net/projects/nikgapps/files/Releases/NikGapps-R/"
            if version == "12.0":
                link = "https://sourceforge.net/projects/nikgapps/files/Releases/NikGapps-S/"
            if version == "12.1":
                link = "https://sourceforge.net/projects/nikgapps/files/Releases/NikGapps-SL/"
        url = get(link)
        page = BeautifulSoup(url.content, "lxml")
        content = page.tbody.tr
        date = content["title"]
        url2 = get(f"{link}{date}")
        page2 = BeautifulSoup(url2.content, "lxml")
        name = page2.tbody.find_all("th", {'headers': 'files_name_h'})
        btn_sub = []
        buttons = []
        for item in name:
            nam = item.find("a")
            string = nam.span.text
            match = re.search(COMPILE, string)
            btn_sub.append(InlineKeyboardButton(
                text=match.group(1), url=nam['href'])
            )
            if len(btn_sub) == 2:
                buttons.append(btn_sub)
                btn_sub = []
        buttons.append([InlineKeyboardButton(text="Back", callback_data=f"gapps_v|{version}")])
        await cq.edit_message_text(text=f"**Select your preferred gapps version**", reply_markup=InlineKeyboardMarkup(buttons))

    # ==  Main menu

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"gapps_main"))
    @check_owner
    async def gapps_filter_cq(cq: CallbackQuery):
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="11", callback_data="gapps_v|11.0"),
                    InlineKeyboardButton(
                        text="12", callback_data="gapps_v|12.0"),
                    InlineKeyboardButton(
                        text="12L", callback_data="gapps_v|12.1"),
                ]
            ]
        )
        await cq.edit_message_text(text="**Select gapps version**", reply_markup=reply_markup)