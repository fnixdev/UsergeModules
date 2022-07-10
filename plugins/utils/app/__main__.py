""" Fetch App Details from Playstore.
.app <app_name> to fetch app details.
"""

# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

# By - @kirito6969 | @Krishna_Singhal

import aiohttp
import bs4

from userge import userge, Message


DEVICE_LIST = "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_device.json"


@userge.on_cmd(
    "app",
    about={
        "header": "Search application details of any app in play store.",
        "usage": "{tr}app telegram",
    },
)
async def app(message: Message):
    try:
        await message.edit("`Searching...`")
        app_name = "+".join(message.input_str.split(" "))
        async with aiohttp.ClientSession() as ses, ses.get(
                f"https://play.google.com/store/search?q={app_name}&c=apps") as res:
            result = bs4.BeautifulSoup(await res.text(), "lxml")

        found = result.find("div", class_="vWM94c")
        if found:
            app_name = found.text
            app_dev = result.find("div", class_="LbQbAe").text
            app_rating = result.find(
                "div", class_="TT9eCd").text.replace("star", "")
            _app_link = result.find("a", class_="Qfxief")['href']
            app_icon = result.find("img", class_="T75of bzqKMd")['src']
        else:
            app_name = result.find("span", class_="DdYX5").text
            app_dev = result.find("span", class_="wMUdtb").text
            app_rating = result.find("span", class_="w2kbF").text
            _app_link = result.find("a", class_="Si6A0c Gy4nib")['href']
            app_icon = result.find("img", class_="T75of stzEZd")['src']

        app_dev_link = (
            "https://play.google.com/store/apps/developer?id="
            + app_dev.replace(" ", "+")
        )
        app_link = "https://play.google.com" + _app_link

        app_details = f"[📲]({app_icon}) **{app_name}**\n\n"
        app_details += f"`Developer :` [{app_dev}]({app_dev_link})\n"
        app_details += f"`Rating :` {app_rating} ⭐️\n"
        app_details += f"`Features :` [View in Play Store]({app_link})"
        await message.edit(app_details, disable_web_page_preview=False)
    except IndexError:
        await message.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await message.err(err)


@userge.on_cmd(
    "magisk",
    about={
        "header": "Fetch all magisk release from source.",
        "usage": "{tr}magisk",
    },
)
async def magisk(message: Message):
    """Scrap all magisk version from source."""
    magisk_branch = {"Stable": "stable", "Beta": "beta", "Canary": "canary"}
    magisk_raw_uri = "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/"
    releases = "**Latest Magisk Releases:**\n"
    async with aiohttp.ClientSession() as session:
        for _type, branch in magisk_branch.items():
            async with session.get(magisk_raw_uri + branch + ".json") as res:
                data = await res.json(content_type="text/plain")
                releases += (
                    f'**× {_type}:** `{data["magisk"]["version"]}-{data["magisk"]["versionCode"]}`|'
                    f'[Notes]({data["magisk"]["note"]})|'
                    f'[Magisk]({data["magisk"]["link"]})|\n'
                )
        await message.edit(releases)


@userge.on_cmd(
    "device",
    about={"header": "Search device with codename",
           "usage": "{tr}device [codename]"},
    allow_via_bot=True,
)
async def device_info(message: Message):
    query = message.input_str
    if not query:
        await message.err("You need insert codename")
        return
    try:
        async with aiohttp.ClientSession() as ses, ses.get(DEVICE_LIST) as res:
            getlist = await res.json(content_type="text/plain")
            target_device = query.lower()
            if target_device in list(getlist):
                device = getlist.get(target_device)
                text = ""
                for x in device:
                    text += f"Brand: `{x['brand']}`\nName: `{x['name']}`\nDevice: `{x['model']}`\nCodename: `{target_device}`"
                    text += "\n\n"
                await message.edit(text)
            else:
                await message.err(f"Device {target_device} not found.")
                return
    except Exception:
        await message.err("Request error")
        return
