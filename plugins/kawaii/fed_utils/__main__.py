## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" federation utils """

import re
import asyncio

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, FloodWait, UserBannedInChannel

from userge import Message, get_collection, userge, config
from ...builtin import sudo
from . import FBAN_LOG_CHANNEL

FED_LIST = get_collection("FED_LIST")
PROOF_CHANNEL = FBAN_LOG_CHANNEL if FBAN_LOG_CHANNEL else config.LOG_CHANNEL_ID

CHANNEL = userge.getCLogger(__name__)
SUDO = list(sudo.USERS)

@userge.on_cmd(
    "addf",
    about={
        "header": "Add a chat to fed list",
        "description": "Add a chat to fed list where message is to be sent",
        "usage": "{tr}addf",
    },
    allow_bots=False,
    allow_channels=False,
    allow_private=False,
)
async def addfed_(message: Message):
    """Adds current chat to connected Feds."""
    name = message.input_str or message.chat.title
    chat_id = message.chat.id
    found = await FED_LIST.find_one({"chat_id": chat_id})
    if found:
        await message.edit(
            f"Chat __ID__: `{chat_id}`\nFed: **{found['fed_name']}**\n\nAlready exists in Fed List !",
            del_in=7,
        )
        return
    await FED_LIST.insert_one({"fed_name": name, "chat_id": chat_id})
    msg_ = f"__ID__ `{chat_id}` added to Fed: **{name}**"
    await message.edit(msg_, del_in=7)
    await CHANNEL.log(msg_)


@userge.on_cmd(
    "delf",
    about={
        "header": "Remove a chat from fed list",
        "flags": {"-all": "Remove all the feds from fedlist"},
        "description": "Remove a chat from fed list",
        "usage": "{tr}delf",
    },
    allow_bots=False,
    allow_channels=False,
)
async def delfed_(message: Message):
    """Removes current chat from connected Feds."""
    if "-all" in message.flags:
        msg_ = "**Disconnected from all connected federations!**"
        await message.edit(msg_, del_in=7)
        await FED_LIST.drop()
    else:
        try:
            chat_ = await message.client.get_chat(message.input_str or message.chat.id)
            chat_id = chat_.id
            chat_.title
        except (PeerIdInvalid, IndexError):
            chat_id = message.input_str
            id_ = chat_id.replace("-", "")
            if not id_.isdigit() or not chat_id.startswith("-"):
                return await message.err("Provide a valid chat ID...", del_in=7)
        out = f"Chat ID: {chat_id}\n"
        found = await FED_LIST.find_one({"chat_id": int(chat_id)})
        if found:
            msg_ = out + f"Successfully Removed Fed: **{found['fed_name']}**"
            await message.edit(msg_, del_in=7)
            await FED_LIST.delete_one(found)
        else:
            return await message.err(
                out + "**Does't exist in your Fed List !**", del_in=7
            )
    await CHANNEL.log(msg_)


@userge.on_cmd(
    "fban",
    about={
        "header": "Fban user",
        "description": "Fban the user from the list of fed",
        "usage": "{tr}fban [username|reply to user|user_id] [reason (optional)]",
    },
    allow_bots=False,
    allow_channels=False,
)
async def fban_(message: Message):
    """Bans a user from connected Feds."""
    fban_arg = ["❯", "❯❯", "❯❯❯", "❯❯❯ <b>FBanned {}</b>"]
    input = message.filtered_input_str
    await message.edit(fban_arg[0])
    sudo_ = False
    if (
        message.from_user.id in SUDO
    ):
        sudo_ = True
    if not message.reply_to_message:
        split_ = input.split(" ", 1)
        user = split_[0]
        if not user.isdigit() and not user.startswith("@"):
            user = extract_id(message.text)
        if len(split_) == 2:
            reason = split_[1]
        else:
            reason = "not specified"
    else:
        user = message.reply_to_message.from_user.id
        reason = input
    if user is None:
        return await message.err("Provide a user ID or reply to a user...", del_in=7)
    try:
        user_ = await message.client.get_users(user)
        user = user_.id
    except (PeerIdInvalid, IndexError):
        pass
    if (
        user in SUDO
        or user in config.OWNER_ID
        or user == (await message.client.get_me()).id
    ):
        if not input:
            await message.edit("Can't fban replied user, give user ID...", del_in=7)
            return
        user = input.split()[0]
        reason = input.split()[1:]
        reason = " ".join(reason)
        try:
            user_ = await message.client.get_users(user)
            user = user_.id
        except (PeerIdInvalid, IndexError):
            d_err = f"Failed to detect user **{user}**, fban might not work..."
            await message.edit(f"{d_err}\nType `y` to ontinue.")
            await CHANNEL.log(d_err)
            try:
                async with userge.conversation(message.chat.id) as conv:
                    response = await conv.get_response(
                        mark_read=True, filters=(filters.user([message.from_user.id]))
                    )
            except BaseException:
                return await message.edit(
                    f"`Fban terminated...\nReason: Response timeout.`"
                )
            if response.text == "y":
                pass
            else:
                return await message.edit(
                    f"`Fban terminated...\nReason: User didn't continue.`"
                )
        if (
            user in SUDO
            or user in config.OWNER_ID
            or user == (await message.client.get_me()).id
        ):
            return await message.err(
                "Can't fban user that exists in SUDO or OWNERS...", del_in=7
            )
    try:
        user_ = await userge.get_users(user)
        u_link = user_.mention
        u_id = user_.id
    except BaseException:
        u_link = user
        u_id = user
    failed = []
    total = 0
    reason = reason or "Not specified."
    await message.edit(fban_arg[1])
    async for data in FED_LIST.find():
        total += 1
        chat_id = int(data["chat_id"])
        try:
            await userge.send_message(
                chat_id,
                f"/fban {user} {reason}",
                disable_web_page_preview=True,
            )
        except UserBannedInChannel:
            pass
        try:
            async with userge.conversation(chat_id, timeout=8) as conv:
                response = await conv.get_response(
                    mark_read=True,
                    filters=(filters.user([609517172]) & ~filters.service),
                )
                resp = response.text
                if not (
                    ("New FedBan" in resp)
                    or ("starting a federation ban" in resp)
                    or ("start a federation ban" in resp)
                    or ("FedBan Reason update" in resp)
                ):
                    failed.append(f"{data['fed_name']}  \n__ID__: `{data['chat_id']}`")
        except FloodWait as f:
            await asyncio.sleep(f.x + 3)
        except BaseException:
            failed.append(data["fed_name"])
    if total == 0:
        return await message.err(
            "You Don't have any feds connected!\nsee .help addf, for more info."
        )
    await message.edit(fban_arg[2])

    if len(failed) != 0:
        status = f"Failed to fban in {len(failed)}/{total} feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Success! Fbanned in `{total}` feds."
    msg_ = (
        fban_arg[3].format(u_link)
        + f"\n**ID:** <code>{u_id}</code>\n**Reason:** {reason}\n**Status:** {status}\n"
    )
    if sudo_:
        msg_ += f"**By:** {message.from_user.mention}"
    await message.edit(msg_)
    await userge.send_message(int(PROOF_CHANNEL), msg_)



@userge.on_cmd(
    "unfban",
    about={
        "header": "Unfban user",
        "description": "Unfban the user from the list of fed",
        "usage": "{tr}unfban [username|reply to user|user_id]",
    },
    allow_bots=False,
    allow_channels=False,
)
async def unfban_(message: Message):
    """Unbans a user from connected Feds."""
    user = (message.extract_user_and_text)[0]
    fban_arg = ["❯", "❯❯", "❯❯❯", "❯❯❯ <b>Un-FBanned {}</b>"]
    await message.edit(fban_arg[0])
    input = message.input_str
    if message.reply_to_message:
        reason = input
    else:
        reason = input.split(" ", 1)[1]
    
    error_msg = "Provide a User ID or reply to a User"
    if user is None:
        return await message.err(error_msg, del_in=7)
    try:
        user_ = await message.client.get_users(user)
    except (PeerIdInvalid, IndexError):
        return await message.err(error_msg, del_in=7)
    user = user_.id
    reason = reason or "Not specified"
    failed = []
    total = 0
    await message.edit(fban_arg[1])
    async for data in FED_LIST.find():
        total += 1
        chat_id = int(data["chat_id"])
        try:
            async with userge.conversation(chat_id, timeout=8) as conv:
                await conv.send_message(f"/unfban {user} {reason}")
                response = await conv.get_response(
                    mark_read=True,
                    filters=(filters.user([609517172]) & ~filters.service),
                )
                resp = response.text
                if (
                    ("New un-FedBan" not in resp)
                    and ("I'll give" not in resp)
                    and ("Un-FedBan" not in resp)
                ):
                    failed.append(f"{data['fed_name']}  \n__ID__: `{data['chat_id']}`")

        except BaseException:
            failed.append(data["fed_name"])
    if total == 0:
        return await message.err(
            "You Don't have any feds connected!\nsee .help addf, for more info."
        )
    await message.edit(fban_arg[2])

    if len(failed) != 0:
        status = f"Failed to un-fban in `{len(failed)}/{total}` feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Success! Un-Fbanned in `{total}` feds."
    msg_ = (
        fban_arg[3].format(user_.mention)
        + f"\n<b>ID:</b> <code>{user}</code>\n<b>Reason:</b> {reason}\n**Status:** {status}"
    )
    await message.edit(msg_)
    await userge.send_message(int(PROOF_CHANNEL), msg_)


@userge.on_cmd(
    "listf",
    about={
        "header": "Fed Chat List",
        "description": "Get a list of chats added in fed",
        "flags": {
            "-id": "Show fed group id in list.",
        },
        "usage": "{tr}listf",
    },
)
async def fban_lst_(message: Message):
    """List all connected Feds."""
    out = ""
    total = 0
    async for data in FED_LIST.find():
        total += 1
        chat_id = data["chat_id"]
        id_ = f"'<code>{chat_id}</code>' - " if "-id" in message.flags else ""
        out += f"• Fed: {id_}<b>{data['fed_name']}</b>\n"
    await message.edit_or_send_as_file(
        f"**Connected federations: [{total}]**\n\n" + out
        if out
        else "**You haven't connected to any federations yet!**",
        caption="Connected Fed List",
    )


def extract_id(mention):
    if str(mention).isdigit():
        return "Input is not a mention but an ID..."
    elif mention.startswith("@"):
        return "Input is not a mention but a username..."
    try:
        men = mention.html
    except:
        return "Input is not a mention."
    filter = re.search(r"\d+", men)
    if filter: 
        return filter.group(0)
    return "ID not found."