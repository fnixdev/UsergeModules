""" see repo """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from userge import userge, Message, versions
from . import *


@userge.on_cmd("repo", about={'header': "get repo link and details"})
async def see_repo(message: Message):
    """see repo"""
    output = f"""
✾ 𝙷𝚒𝚕𝚣𝚞 𝚅𝚎𝚛𝚜𝚒𝚘𝚗 : `{versions.__hilzu_version__}`
✾ 𝙲𝚘𝚛𝚎 𝚁𝚎𝚙𝚘 : [Hilzu]({UPSTREAM_REPO})
✾ 𝙻𝚘𝚊𝚍𝚎𝚛 𝚁𝚎𝚙𝚘 : [Loader]({LOADER})
✾ 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝚁𝚎𝚙𝚘 : [Modules]({MODULES})
"""
    await message.edit(output, disable_web_page_preview=True)
