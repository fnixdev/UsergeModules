""" Wallpaper Module """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

import requests

from userge import userge, Message, pool


@userge.on_cmd("wall", about={
    'header': "Search Wallpaper",
    'flags': {
        '-l': "Limit of Wallpapers",
        '-doc': "Send as Documents (Recommended)"
    },
    'description': 'Search and Download Hd Wallpaper from AlphaCoders and upload to Telegram',
    'usage': "{tr}wall [Query]",
    'examples': "{tr}wall kanna"})
async def wall_(msg: Message):
    """ Wallpaper Search """
    limit = min(int(msg.flags.get('-l', 1)), 10)
    if msg.filtered_input_str:
        qu = msg.filtered_input_str
        await msg.edit(f"__searching wallpapers__ ... `{qu}`")
        await msg.delete()
        for i in range(limit):
            results = requests.get(f"https://kuuhaku-api-production.up.railway.app/api/wallpaper?query={qu}")
            if results.status_code != 200:
                return await msg.edit('**Result Not Found**')
            if "error" in results.json():
                return await msg.edit(f"{qu} don't have wallpapers")
            _json = results.json()['url']
            if '-doc' in msg.flags:
                await msg.client.send_document(msg.chat.id, document=_json)
            else:
                await msg.client.send_photo(msg.chat.id, photo=_json)
    else:
        await msg.edit('**Give me Something to search.**')
        await msg.reply_sticker('CAADAQADmQADTusQR6fPCVZ3EhDoFgQ')


@userge.on_cmd("mwall", about={
    'header': "Search Mobile Wallpaper",
    'flags': {
        '-l': "Limit of Wallpapers",
        '-doc': "Send as Documents (Recommended)"
    },
    'description': 'Search and Download Hd Wallpaper from AlphaCoders and upload to Telegram',
    'usage': "{tr}mwall [Query]",
    'examples': "{tr}mwall kanna"})
async def mobile_wall_(msg: Message):
    """ Wallpaper Mobile Search """
    limit = min(int(msg.flags.get('-l', 1)), 10)
    if msg.filtered_input_str:
        qu = msg.filtered_input_str
        await msg.edit(f"__searching wallpapers__ ... `{qu}`")
        await msg.delete()
        for i in range(limit):
            results = requests.get(f"https://kuuhaku-api-production.up.railway.app/api/wallpaper?query={qu}")
            if results.status_code != 200:
                return await msg.edit('**Result Not Found**')
            if "error" in results.json():
                return await msg.edit(f"{qu} don't have mobile wallpapers")
            _json = results.json()['url']
            if '-doc' in msg.flags:
                await msg.client.send_document(msg.chat.id, document=_json)
            else:
                await msg.client.send_photo(msg.chat.id, photo=_json)
    else:
        await msg.edit('**Give me Something to search.**')
        await msg.reply_sticker('CAADAQADmQADTusQR6fPCVZ3EhDoFgQ')
