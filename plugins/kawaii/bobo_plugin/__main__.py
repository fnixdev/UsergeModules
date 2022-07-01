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
        "description": "Obtenha todos os dados de um dispositivo.",
        "usage": "{tr}d [dispositivo]",
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
            await message.err("Desbloqueie @vegadata_bot primeiro...", del_in=5)
            return
        response = await conv.get_response(mark_read=True)
    await message.edit(response.text)