""" see repo """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from userge import userge, Message, versions

from . import UPSTREAM_REPO


@userge.on_cmd("repo", about={'header': "get repo link and details"})
async def see_repo(message: Message):
    """see repo"""
    output = f"""
• **hilzu version** : `{versions.__hilzu_version__}`
• **repo** : [Hilzu]({UPSTREAM_REPO})
"""
    await message.edit(output)
