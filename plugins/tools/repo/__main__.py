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
**Hey**, __I am using__ 🔥 **Userge** 🔥

    __Durable as a Serge__

• **userge version** : `{await versions.get_full_version()}`
• **loader version** : `{versions.__loader_version__}`
• **license** : {versions.__license__}
• **copyright** : {versions.__copyright__}
• **repo** : [Userge]({UPSTREAM_REPO})
"""
    await message.edit(output)
