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
βΎ π·πππ£π πππππππ : `{versions.__hilzu_version__}`
βΎ π²πππ ππππ : [Hilzu]({UPSTREAM_REPO})
βΎ π»πππππ ππππ : [Loader]({LOADER})
βΎ πΌππππππ ππππ : [Modules]({MODULES})
"""
    await message.edit(output, disable_web_page_preview=True)
