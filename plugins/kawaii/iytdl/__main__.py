# == kang from https://github.com/lostb053/Userge-Plugins/tree/dev/plugins/utils/iytdl

import re
import os
import ujson
import wget

from iytdl import main
from . import PATH
from uuid import uuid4

from pyrogram import filters
from pyrogram.errors import MediaEmpty, MessageIdInvalid, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InlineQuery, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent

from userge import Message, config as Config, userge
from ...builtin import sudo


class YT_Search_X:
    def __init__(self):
        if not os.path.exists(PATH):
            with open(PATH, "w") as f_x:
                ujson.dump({}, f_x)
        with open(PATH) as yt_db:
            self.db = ujson.load(yt_db)

    def store_(self, rnd_id: str, results: dict):
        self.db[rnd_id] = results
        self.save()

    def save(self):
        with open(PATH, "w") as outfile:
            ujson.dump(self.db, outfile, indent=4)


ytsearch_data = YT_Search_X()


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

    # https://gist.github.com/silentsokolov/f5981f314bc006c82a41
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
        link = regex.match(query)
        results = []
        found_ = True
        if link is None:
            search_key = rand_key()
            YT_DB[search_key] = query
            search = await main.VideosSearch(query).next()
            resp = (search.result()).get("result")
            if len(resp) == 0:
                found_ = False
            else:
                outdata = await result_formatter(resp)
                key_ = rand_key()
                ytsearch_data.store_(key_, outdata)
                vid_id = outdata[1]["video_id"]
                buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"1/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|1")
                    ],
                    [
                        InlineKeyboardButton(
                            "Download", callback_data=f"yt_gen|{vid_id}")
                    ]
                ])
                caption = outdata[1]["message"]
                photo = outdata[1]["thumb"]
        else:
            return
        if found_:
            results.append(
                        InlineQueryResultPhoto(
                            photo_url=photo,
                            title=link,
                            description="Click to Download",
                            caption=caption,
                            reply_markup=buttons,
                        )
                    )
        else:
            results.append(
                        InlineQueryResultArticle(
                            title="not Found",
                            input_message_content=InputTextMessageContent(
                                f"no results for `{query}`"
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
            out+=f"\nPublished {i['publishedTime']}\n"
            out+=f"\n<b>❯ Duration:</b> {i['duration']}"
            out+=f"\n<b>❯ Views:</b> {i['viewCount']['short']}"
            out+=f"\n<b>❯ Uploader:</b> <a href={i['channel']['link']}>{i['channel']['name']}</a>\n\n"
            if i['descriptionSnippet']:
                for t in i['descriptionSnippet']:
                    out+=t['text']
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"1/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|1")
                    ],
                    [
                        InlineKeyboardButton("Download", callback_data=f"yt_gen|{i['id']}")
                    ]
                ]
            )
            try:
                await userge.bot.send_photo(m.chat.id, i["thumbnails"][1 if len(i["thumbnails"])>1 else 0]["url"].split("?")[0], caption=out, reply_markup=btn)
            except MediaEmpty:
                await userge.bot.send_photo(m.chat.id, "https://camo.githubusercontent.com/8486ea960b794cefdbbba0a8ef698d04874152c8e24b3b26adf7f50847d4a3a8/68747470733a2f2f692e696d6775722e636f6d2f51393443444b432e706e67", caption=out, reply_markup=btn)

        else:
            key = match.group("id")
            x = await main.Extractor().get_download_button(key)
            rand = rand_key()
            img = wget.download(x.image_url, out=f"{rand}.png")
            await m.reply_photo(f"{rand}.png", caption=x.caption, reply_markup=x.buttons)


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
        out+=f"\nPublished {i['publishedTime']}\n"
        out+=f"\n<b>❯ Duration:</b> {i['duration']}"
        out+=f"\n<b>❯ Views:</b> {i['viewCount']['short']}"
        out+=f"\n<b>❯ Uploader:</b> <a href={i['channel']['link']}>{i['channel']['name']}</a>\n\n"
        if i['descriptionSnippet']:
            for t in i['descriptionSnippet']:
                out+=t['text']
        if page==0:
            if len(search['result'])==1:
                return await cq.answer("That's the end of list", show_alert=True)
            scroll_btn = [
                [
                    InlineKeyboardButton(f"1/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|1")
                ]
            ]
        elif page==len(search['result'])-1:
            scroll_btn = [
                [
                    InlineKeyboardButton(f"Back", callback_data=f"ytdl_scroll|{search_key}|{len(search['result'])-2}")
                ]
            ]
        else:
            scroll_btn = [
                [
                    InlineKeyboardButton(f"Back", callback_data=f"ytdl_scroll|{search_key}|{page-1}"),
                    InlineKeyboardButton(f"{page+1}/{len(search['result'])}", callback_data=f"ytdl_scroll|{search_key}|{page+1}")
                ]
            ]
        btn = [
            [
                InlineKeyboardButton("Download", callback_data=f"yt_gen|{i['id']}")
            ]
        ]
        btn = InlineKeyboardMarkup(scroll_btn+btn)
        try:
            await cq.edit_message_media(InputMediaPhoto(i["thumbnails"][1 if len(i["thumbnails"])>1 else 0]["url"].split("?")[0], caption=out), reply_markup=btn)
        except MediaEmpty:
            await cq.edit_message_media(InputMediaPhoto("https://camo.githubusercontent.com/8486ea960b794cefdbbba0a8ef698d04874152c8e24b3b26adf7f50847d4a3a8/68747470733a2f2f692e696d6775722e636f6d2f51393443444b432e706e67", caption=out), reply_markup=btn)


    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"yt_(gen|dl)\|(.*)"))
    @check_owner
    async def ytdl_gendl_callback(cq: CallbackQuery):
        callback = cq.data.split("|")
        key = callback[1]
        if callback[0]=="yt_gen":
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



async def result_formatter(results: list):
    output = {}
    for index, r in enumerate(results, start=1):
        thumb = (r.get("thumbnails").pop()).get("url")
        upld = r.get("channel")
        title = f'<a href={r.get("link")}><b>{r.get("title")}</b></a>\n'
        out = title
        if r.get("descriptionSnippet"):
            out += "<code>{}</code>\n\n".format(
                "".join(x.get("text") for x in r.get("descriptionSnippet"))
            )
        out += f'<b>❯  Duration:</b> {r.get("accessibility").get("duration")}\n'
        views = f'<b>❯  Views:</b> {r.get("viewCount").get("short")}\n'
        out += views
        out += f'<b>❯  Upload date:</b> {r.get("publishedTime")}\n'
        if upld:
            out += "<b>❯  Uploader:</b> "
            out += f'<a href={upld.get("link")}>{upld.get("name")}</a>'
        v_deo_id = r.get("id")
        output[index] = dict(
            message=out,
            thumb=thumb,
            video_id=v_deo_id,
            list_view=f'<img src={thumb}><b><a href={r.get("link")}>{index}. {r.get("accessibility").get("title")}</a></b><br>',
        )

    return 