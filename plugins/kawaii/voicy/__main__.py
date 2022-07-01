## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from pyrogram.errors import YouBlockedUser

from userge import Message, userge


@userge.on_cmd(
    "voicy",
    about={
        "header": "Convert Voice",
        "description": "converte uma mensagem de audio em texto",
        "usage": "{tr}voicy reply audio",
    },
)
async def f_stat(message: Message):
    """convert voice to text"""
    bot_ = "voicybot"
    reply = message.reply_to_message
    if not reply:
        return await message.edit("`Você precisa responder a uma mensagem de audio.`")
    if not message.reply_to_message.voice:
        return await message.edit("`Isso não é uma mensagem de audio.`")
    voz = message.reply_to_message.voice.file_id

    async with userge.conversation(bot_, timeout=1000) as conv:
        try:
            await message.client.send_voice(bot_, voice=voz)
            await message.edit("`Processando...`")
            response = await conv.get_response(mark_read=True)
        except YouBlockedUser:
            return await message.err("Desbloqueie @voicybot primeiro...", del_in=5)
    resp = response.text.replace("Putin and his cronies kill civilians in the war in Ukraine #stopputin", "")
    msg = f"**Mensagem Convertida**:\n\n`{resp}`"
    await message.edit(msg)