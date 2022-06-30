""" create quote """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

import asyncio

from pyrogram.errors.exceptions.bad_request_400 import YouBlockedUser

from userge import userge, Message


@userge.on_cmd("quote", about={
    'header': "Quote a message",
    'usage': "{tr}quote [text or reply to msg]"}, allow_via_bot=False)
async def quotecmd(message: Message):
    """quotecmd"""
    asyncio.get_event_loop().create_task(message.delete())
    args = message.input_str
    replied = message.reply_to_message
    async with userge.conversation('QuotLyBot') as conv:
        try:
            if replied and not args:
                await conv.forward_message(replied)
            else:
                if not args:
                    await message.err('input not found!')
                    return
                await conv.send_message(args)
        except YouBlockedUser:
            await message.edit('first **unblock** @QuotLyBot')
            return
        quote = await conv.get_response(mark_read=True)
        if not quote.sticker:
            await message.edit('something went wrong!, see here: @QuotlyBot')
        else:
            message_id = replied.id if replied else None
            await userge.send_sticker(chat_id=message.chat.id,
                                      sticker=quote.sticker.file_id,
                                      reply_to_message_id=message_id)
