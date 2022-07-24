## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==


from pyrogram.errors import YouBlockedUser

from userge import Message, userge


@userge.on_cmd(
    "d",
    about={
        "header": "Device description",
        "description": "Get details from device.",
        "usage": "{tr}d [device]",
    },
)
async def ln_user_(message: Message):
    """device desc"""
    device_ = message.input_str 
    bot_ = "@vegadata_bot"
    async with userge.conversation(bot_, timeout=1000) as conv:
        try:
            await conv.send_message(f"!d {device_}")
        except YouBlockedUser:
            await message.err("Unblock @vegadata_bot first...", del_in=5)
            return
        response = await conv.get_response(mark_read=True)
    await message.edit(response.text)