""" Wallpaper Module """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==


import requests
import wget

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
    limit = min(int(msg.flags.get('-l', 8)), 10)
    wall = []
    if msg.filtered_input_str:
        qu = msg.filtered_input_str
        await msg.edit(f"__searching wallpapers__ ... `{qu}`")
        for i in range(limit):
            results = requests.get(f"https://kuuhaku-api-production.up.railway.app/api/wallpaper?query={qu}")
            if results.status_code != 200:
                return await msg.edit('**Result Not Found**')
            _json = results.json()['url']
            wall.append(_json)
        await msg.edit(wall)
    else:
        await msg.edit('**Give me Something to search.**')
        await msg.reply_sticker('CAADAQADmQADTusQR6fPCVZ3EhDoFgQ')
