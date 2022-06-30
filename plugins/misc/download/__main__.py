""" downloader """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from userge import userge, Message
from userge.utils.exceptions import ProcessCanceled

from .. import download

LOGGER = userge.getLogger(__name__)


@userge.on_cmd("download", about={
    'header': "Download files to server",
    'usage': "{tr}download [url | reply to telegram media]",
    'examples': "{tr}download https://speed.hetzner.de/100MB.bin | testing upload.bin"},
    check_downpath=True)
async def down_load_media(message: Message):
    """ download from tg and url """
    if message.reply_to_message:
        resource = message.reply_to_message
    elif message.input_str:
        resource = message.input_str
    else:
        await message.err("nothing found to download")
        return
    try:
        dl_loc, d_in = await download.handle_download(message, resource)
    except ProcessCanceled:
        await message.canceled()
    except Exception as e_e:  # pylint: disable=broad-except
        await message.err(str(e_e))
    else:
        await message.edit(f"Downloaded to `{dl_loc}` in {d_in} seconds")
