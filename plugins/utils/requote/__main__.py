""" Requote Text """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from requests.utils import requote_uri

from userge import userge, Message


@userge.on_cmd("requote", about={
    'header': "Requote Text",
    'description': "get requoted text from a normal text",
    'usage': "{tr}requote [text]"})
async def requote(update: Message):
    if not update.input_str:
        text = "Add requote text too."
    else:
        text = requote_uri(update.input_str)
    await update.edit(
        text=text,
        disable_web_page_preview=True
    )
