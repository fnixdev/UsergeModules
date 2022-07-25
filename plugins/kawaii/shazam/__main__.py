## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" shazan plugin """

import os

from shazamio import Shazam

from userge import userge, Message, config


shazam = Shazam()


@userge.on_cmd(
    "whichsong", about={
        'header': "Use shazam to find the name and artist of a song",
        'usage': "{tr}whichisong [reply audio]"},
    allow_channels=False
)
async def which_song(message: Message):
    """ discover song using shazam"""
    replied = message.reply_to_message
    if not replied or not replied.audio:
        await message.edit("<code>Reply audio needed.</code>")
        return
    await message.edit("<code>downloading audio..</code>")
    file = await message.client.download_media(
                message=message.reply_to_message,
                file_name=config.Dynamic.DOWN_PATH
            )
    try:
        await message.edit("<code>identifying music</code>")
        res = await shazam.recognize_song(file)
    except Exception as e:
        await message.reply(e)
        os.remove(file)
        return await message.err("<code>Failed to get sound data.</code>")
    song = res["track"]
    out = f"<b>Song Recognised!\n\n{song['title']}</b>\n<i>- {song['subtitle']}</i>"
    try:
        await message.delete()
        await message.reply_photo(photo=song["images"]["coverart"], caption=out)
    except KeyError:
        await message.edit(out)
    except Exception:
        os.remove(file)
        return await message.err("<code>Failed to get sound data.</code>")
    os.remove(file)