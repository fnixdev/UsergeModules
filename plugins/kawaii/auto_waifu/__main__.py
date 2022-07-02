# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==
#
# by @fnixdev

""" auto protecc waifu """

import os
import requests

from bs4 import BeautifulSoup

from userge import userge, Message, filters, config, get_collection

BASE_URL = "http://www.google.com"
temp_folder = config.Dynamic.DOWN_PATH

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
}

IS_ENABLED = False
IS_ENABLED_FILTER = filters.create(lambda _, __, ___: IS_ENABLED)

USER_DATA = get_collection("CONFIGS")
CHANNEL = userge.getCLogger(__name__)


@userge.on_start
async def _init() -> None:
    global IS_ENABLED  # pylint: disable=global-statement
    data = await USER_DATA.find_one({'_id': 'AUTO_WAIFU'})
    if data:
        IS_ENABLED = data['on']


@userge.on_cmd(
    "autowaifu", about={
        'header': "Auto Waifu Protecc",
        'description': "enable or disable auto waifu protecc",
        'usage': "{tr}autowaifu"},
    allow_channels=False, allow_via_bot=False
)
async def auto_waifu(msg: Message):
    global IS_ENABLED  # pylint: disable=global-statement
    IS_ENABLED = not IS_ENABLED
    await USER_DATA.update_one({'_id': 'AUTO_WAIFU'},
                               {"$set": {'on': IS_ENABLED}}, upsert=True)
    await msg.edit(
        "Auto Waifu Protecc has been **{}** Successfully...".format(
            "Enabled" if IS_ENABLED else "Disabled"
        ),
        log=True, del_in=5
    )


@userge.on_filters(IS_ENABLED_FILTER & filters.group & filters.photo & filters.incoming
                   & filters.user([
                                1733263647, # @Collect_yours_waifus_bot
                                792028928 # @loli_harem_bot
                                ]),  # Bot IDs
                   group=-1, allow_via_bot=False)
async def waifu_handler(msg: Message):
    img = await msg.download(config.Dynamic.DOWN_PATH)
    try:
        search_url = f"{BASE_URL}/searchbyimage/upload"
        multipart = {"encoded_image": (
            img, open(img, "rb")), "image_content": "", }
        google_rs_response = requests.post(
            search_url, files=multipart, allow_redirects=False
        )
        the_location = google_rs_response.headers.get("Location")
        response = requests.get(the_location, headers=headers)
        os.remove(img)
        soup = BeautifulSoup(response.text, "html.parser")
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_text = prs_anchor_element.text
        out_str = f"/protecc {prs_text}"
        await msg.reply_text(out_str)
        await CHANNEL.log(f'Auto Waifu Responded in {msg.chat.title} [{msg.chat.id}]\n f"[View Message](https://t.me/c/{str(msg.chat.id)[4:]}/{msg.message_id})')
    except Exception as e_x:  # pylint: disable=broad-except
        await CHANNEL.log(str(e_x))
