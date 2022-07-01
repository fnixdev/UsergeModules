## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from io import BytesIO

from pyrogram.enums import ParseMode
from PIL import Image, ImageDraw, ImageFont
from requests import get

from userge import Message, userge
from userge.utils import runcmd


@userge.on_cmd(
    "neofetch",
    about={
        "header": "Neofetch is a command-line system information tool",
        "description": "displays information about your operating system, software and hardware in an aesthetic and visually pleasing way.",
        "usage": " {tr}neofetch",
        "flags": {"-img": "To Get output as Image"},
        "examples": ["{tr}neofetch", "{tr}neofetch -img"],
    },
)
async def neofetch_(message: Message):
    await message.edit("Getting System Info ...")
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if "-img" in message.flags:
        await message.delete()
        await message.client.send_photo(
            message.chat.id, await neo_image(), reply_to_message_id=reply_id
        )
    else:
        await message.edit(
            "<code>{}</code>".format((await runcmd("neofetch --stdout"))[0]),
            parse_mode=ParseMode.HTML,
        )


async def neo_image():
    neofetch = (await runcmd("neofetch --stdout"))[0]
    font_url = ("https://raw.githubusercontent.com/code-rgb/AmongUs/master/FiraCode-Regular.ttf")
    me = await userge.get_me()
    fnix = [838926101]

    # only for fnix
    if me.id in fnix:
        base_pic = "https://telegra.ph/file/4561b1d8e3af7e032b38c.png"
        before_color = (0, 0, 0) # Black
        font_color = (4, 123, 108) # Cyan
        photo = Image.open(BytesIO(get(base_pic).content))
        drawing = ImageDraw.Draw(photo)
        font = ImageFont.truetype(BytesIO(get(font_url).content), 14)
        x = 0
        y = 0
        for u_text in neofetch.splitlines():
            if ":" in u_text:
                ms = u_text.split(":", 1)
                drawing.text(
                    xy=(275, 45 + x),
                    text=ms[0] + ":",
                    font=font,
                    fill=font_color,
                )
                drawing.text(
                    xy=((8.5 * len(ms[0])) + 275, 45 + x), text=ms[1], font=font, fill=before_color
                )
            else:
                color = font_color if y == 0 else before_color
                drawing.text(xy=(275, 53 + y), text=u_text, font=font, fill=color)
            x += 20
            y += 13
        new_pic = BytesIO()
        photo = photo.resize(photo.size, Image.ANTIALIAS)
        photo.save(new_pic, format="PNG")
        new_pic.name = "NeoFetch.png"
        return new_pic
    else:
        font_color = (255, 42, 38)  # Red
        before_color = (255, 255, 255)
        if "Debian" in neofetch:
            base_pic = "https://telegra.ph/file/1f62cbef3fe8e24afc6f7.jpg"
        elif "Kali" in neofetch:
            base_pic = "https://i.imgur.com/iBJxExq.jpg"
            font_color = (87, 157, 255)  # Blue
        else:
            base_pic = "https://telegra.ph/file/f3191b7ecdf13867788c2.jpg"
        photo = Image.open(BytesIO(get(base_pic).content))
        drawing = ImageDraw.Draw(photo)
        font = ImageFont.truetype(BytesIO(get(font_url).content), 14)
        x = 0
        y = 0
        for u_text in neofetch.splitlines():
            if ":" in u_text:
                ms = u_text.split(":", 1)
                drawing.text(
                    xy=(315, 45 + x),
                    text=ms[0] + ":",
                    font=font,
                    fill=font_color,
                )
                drawing.text(
                    xy=((8.5 * len(ms[0])) + 315, 45 + x), text=ms[1], font=font, fill=before_color
                )
            else:
                color = font_color if y == 0 else before_color
                drawing.text(xy=(315, 53 + y), text=u_text, font=font, fill=color)
            x += 20
            y += 13
        new_pic = BytesIO()
        photo = photo.resize(photo.size, Image.ANTIALIAS)
        photo.save(new_pic, format="JPEG")
        new_pic.name = "NeoFetch.jpg"
        return new_pic