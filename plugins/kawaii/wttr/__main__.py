## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

import aiohttp

from html import escape

from pyrogram.enums import ParseMode
from pyrogram.errors import YouBlockedUser

from userge import Message, userge


@userge.on_cmd(
    "weather",
    about={
        "header": "use this to get weather details",
        "description": "get weather info for any city",
    },
)
async def weather_get(message: Message):
    """
    this function can get weather info
    """
    location = message.input_str
    if not location:
        return await message.err("`Especifique uma cidade.\n.Ex: .w Brasilia`", del_in=5)
    if len(location) > 1:
        headers = {"user-agent": "httpie"}
        url = f"https://wttr.in/{location}?mnTC0&lang=pt-br"
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as resp:
                    data = await resp.text()
        except Exception:
            return await message.err("`Falha ao obter weather deasa cidade.`", del_in=5)

        if "we processed more than 1M requests today" in data:
            await message.edit("`Você fez muitas requisições, espere ate amanhã e tente novamente!`")
        else:
            weather = f"<code>{escape(data.replace('report', 'Report'))}</code>"
            await message.edit(weather, parse_mode=ParseMode.HTML)
    else:
        await message.delete()