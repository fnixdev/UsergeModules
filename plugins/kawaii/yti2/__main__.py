# == kang from https://github.com/lostb053/Userge-Plugins/tree/dev/plugins/utils/iytdl

from fileinput import filename
import json

from youtubesearchpython import SearchVideos
from re import A, compile as comp_regex
from iytdl import main

from pyrogram import filters
from pyrogram.errors import MessageIdInvalid, MessageNotModified
from pyrogram.types import CallbackQuery, InlineQuery, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent

from userge import Message, userge, config as Config
from userge.utils import get_response
from ...builtin import sudo

LOGGER = userge.getLogger(__name__)
YOUTUBE_REGEX = comp_regex(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)


@userge.on_cmd(
    "yti",
    about={
        'header': "Advanced YTDL",
        'usage': "{tr}yti URL or Query"}
)
async def yti_ub_cmd(m: Message):
    reply = m.reply_to_message
    query = None
    if m.input_str:
        query = m.input_str
    elif reply:
        if reply.text:
            query = reply.text
        elif reply.caption:
            query = reply.caption
    if not query:
        return await m.err("Input or reply to a valid youtube URL", del_in=5)
    await m.edit(f"🔎 Searching Youtube for: <code>'{query}'</code>")
    link_ = get_link(query)
    id_ = get_yt_video_id(link_)
    thumb_ = await get_ytthumb(id_)
    x = await main.Extractor().get_download_button(id_)
    if m.client.is_bot:
        await m.delete()
        await userge.bot.send_photo(m.chat.id, thumb_, caption=x.caption, reply_markup=x.buttons)
    else:
        bot = await userge.bot.get_me()
        x = await userge.get_inline_bot_results(bot.username, f"ytdl {query}")
        await m.delete()
        await userge.send_inline_bot_result(
            chat_id=m.chat.id, query_id=x.query_id, result_id=x.results[0].id
        )


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

    ytdl = main.iYTDL(Config.LOG_CHANNEL_ID, download_path="userge/plugins/kawaii/iytdl/ytdl")

    @userge.bot.on_inline_query(
        filters.create(
            lambda _, __, inline_query: (
                inline_query.query
                and inline_query.query.startswith("yti ")
                and inline_query.from_user
                and inline_query.from_user.id in Config.OWNER_ID
            ),
            name="YtInline"
        ),
        group=-2
    )
    async def inline_iydl(_, inline_query: InlineQuery):
        query = inline_query.query.split("yti ")[1].strip()
        results = []
        link_ = get_link(query)
        id_ = get_yt_video_id(link_)
        x = await main.Extractor().get_download_button(id_)
        found_ = True
        thumb_ = await get_ytthumb(id_)
        if found_:
            results.append(
                InlineQueryResultPhoto(
                    photo_url=thumb_,
                    title=link_,
                    description="click to download",
                    caption=x.caption,
                    reply_markup=x.buttons,
                )
            )
        else:
            results.append(
                InlineQueryResultArticle(
                    title="not Found",
                    input_message_content=InputTextMessageContent(
                        f"No result found for `{query}`"
                    ),
                    description="INVALID",
                )
            )
        await inline_query.answer(
            results=results,
            cache_time=5
        )
        inline_query.stop_propagation()


    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"yt_dl\|(.*)"))
    @check_owner
    async def ytdl_gendl_callback(cq: CallbackQuery):
        callback = cq.data.split("|")
        key = callback[1]
        uid = callback[2]
        type_ = callback[3]
        if type_ == "a":
            format_ = "audio"
        else:
            format_ = "video"
        upload_key = await ytdl.download("https://www.youtube.com/watch?v="+key, uid, format_, cq, True, 3)
        await ytdl.upload(userge.bot, upload_key, format_, cq, True)


def get_yt_video_id(url: str):
    match = YOUTUBE_REGEX.search(url)
    if match:
        return match.group(1)


def get_link(query):
    vid_id = get_yt_video_id(query)
    link = f"https://www.youtube.com/watch?v={vid_id}"
    if vid_id is None:
        try:
            res_ = SearchVideos(query, offset=1, mode="json", max_results=1)
            link = json.loads(res_.result())["search_result"][0]["link"]
            return link
        except Exception as e:
            LOGGER.exception(e)
            return e
    else:
        return link


async def get_ytthumb(videoid: str):
    thumb_quality = [
        "maxresdefault.jpg",  # Best quality
        "hqdefault.jpg",
        "sddefault.jpg",
        "mqdefault.jpg",
        "default.jpg",  # Worst quality
    ]
    thumb_link = "https://i.imgur.com/4LwPLai.png"
    for qualiy in thumb_quality:
        link = f"https://i.ytimg.com/vi/{videoid}/{qualiy}"
        if await get_response.status(link) == 200:
            thumb_link = link
            break
    return thumb_link
