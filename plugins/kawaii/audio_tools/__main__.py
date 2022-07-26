# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" audio tools """

import os

from pyrogram.enums import MessageMediaType

from userge import userge, Message, config
from userge.utils import runcmd


@userge.on_cmd(
    "extractaudio", about={
        'header': "extract audio from a video",
        'usage': "{tr}extractaudio [reply video]"},
    allow_channels=False
)
async def extract_audio(message: Message):
    """ extract audio """
    replied = message.reply_to_message
    if not replied:
        await message.edit("<code>Reply video needed.</code>")
        return
    if replied.media == MessageMediaType.VIDEO:
        await message.edit("<code>downloading video..</code>")
        file = await message.client.download_media(
            message=replied,
            file_name=config.Dynamic.DOWN_PATH
        )
        dur = replied.video.duration
        out_file = file + ".mp3"
        try:
            await message.edit("<code>trying extract audio</code>")
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await runcmd(cmd)
            await message.edit("<code>uploading audio...</code>")
            await message.delete()
            await message.client.send_audio(
                message.chat.id,
                audio=out_file,
                caption="<b>Audio extracted by @HilzuUB</b>",
                duration=dur
            ) 
        except Exception:
            await message.edit("<code>Fail.</code>")
        os.remove(out_file)
        os.remove(file)
    else:
        await message.edit("<code>Reply video needed.</code>")
        return


@userge.on_cmd(
    "makevoice", about={
        'header': "convert audio/video in audio voice file",
        'usage': "{tr}makevoice [reply video or audio]"},
    allow_channels=False
)
async def make_voice(message: Message):
    """ make voice note """
    replied = message.reply_to_message
    if not replied:
        await message.edit("<code>Reply audio or video needed.</code>")
        return
    if replied.media == MessageMediaType.VIDEO or MessageMediaType.AUDIO:
        await message.edit("<code>downloading ...</code>")
        file = await message.client.download_media(
            message=replied,
            file_name=config.Dynamic.DOWN_PATH
        )
        if replied.video:
            dur = replied.video.duration
        else:
            if replied.audio:
                dur = replied.audio.duration
            if replied.voice:
                dur = replied.voice.duration
        try:
            await message.edit("<code>trying make audio</code>")
            cmd = f"ffmpeg -i '{file}' -map 0:a -codec:a libopus -b:a 100k -vbr on voice.opus"
            await runcmd(cmd)
            await message.edit("<code>uploading audio...</code>")
            await message.delete()
            await message.client.send_voice(
                message.chat.id,
                voice="voice.opus",
                caption="<b>Voice created by @HilzuUB</b>",
                duration=dur
            )
        except Exception:
            await message.edit("<code>Fail.</code>")
        os.remove("voice.opus")
        os.remove(file)
    else:
        await message.edit("<code>Reply audio or video needed.</code>")
        return