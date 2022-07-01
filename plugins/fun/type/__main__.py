""" simulate a typewriter """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from userge import userge, Message


@userge.on_cmd("type", about={
    'header': "Simulate a typewriter",
    'usage': "{tr}type [text]"})
async def type_(message: Message):
    text = message.input_str
    if not text:
        await message.err("input not found")
        return
    typing_symbol = '|'
    old_text = ''
    await message.edit(typing_symbol)
    for character in text:
        if message.process_is_canceled:
            await message.edit("`process cancelled`")
            break
        old_text += character
        typing_text = old_text + typing_symbol
        await message.try_to_edit(typing_text, sudo=False)
        await message.try_to_edit(old_text, sudo=False)
