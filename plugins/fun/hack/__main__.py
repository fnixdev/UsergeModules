""" Hack Animation """

## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

# by Alone

import asyncio

from userge import userge, Message


@userge.on_cmd("hack$", about={"header": "kensar hacking animation"})
async def hack_func(message: Message):
    user = await message.client.get_user_dict(message.from_user.id)
    heckerman = user["mention"]
    animation_chars = [
        "`Installing Files To Hacked Private Server...`",
        "`Target Selected.`",
        "`Installing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Installing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Installing... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`lnstallig... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Installing... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Installing... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Installing... 84%\n█████████████████████▒▒▒▒ `",
        "`Installing... 100%\n████████Installed██████████ `",
        "`Target files Uploading...\n\nDirecting To Remote  server to hack..`",
        "`root@hilzu:~#` ",
        "`root@hilzu:~# ls`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~#`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# `",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@hilzu:~# trap whoami`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@hilzu:~# trap whoami\n\nwhoami=user`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@hilzu:~# trap whoami\n\nwhoami=user\nboost_trap on force ...`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@hilzu:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nvictim detected in ghost ...`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@hilzu:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nvictim detected in ghost ...\n\nAll Done!`",
        "`root@hilzu:~# ls\n\n  usr  ghost  codes  \n\nroot@hilzu:~# # So Let's Hack it ...\nroot@hilzu:~# touch setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@hilzu:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nvictim detected  in ghost ...\n\nAll Done!\nInstalling Token!\nToken=`DJ65gulO90P90nlkm65dRfc8I`",
        "`Hacking... 0% completed.\nTERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (1.3) kB`",
        "`Hacking... 4% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package`",
        "`hacking.....6% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target account chat\n lding chat tg-bot bruteforce finished`",
        "`hacking.....8% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target account chat\n lding chat tg-bot bruteforce finished\n creating pdf of chat`",
        "`hacking....15% completed\n Terminal:chat history from telegram exporting to private database.\n terminal 874379gvrfghhuu5tlotruhi5rbh installing`",
        "`hacking....24% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target account chat\n lding chat tg-bot bruteforce finished\nerminal:chat history from telegram exporting to private database.\n terminal 874379gvrfghhuu5tlotruhi5rbh installed\n creting data into pdf`",
        "`hacking....32% completed\n looking for use history \n downloading-telegram -id prtggtgf . gfr (12.99 mb)\n collecting data starting imprute attack to user account\n chat history from telegram exporting to private database.\n terminal 874379gvrfghhuu5tlotruhi5rbh installed\n creted data into pdf\nDownload sucessful Bruteforce-Telegram-0.1.tar.gz (1.3)`",
        "`hacking....38% completed\n\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e`",
        "`hacking....52% completed\nexterting data from telegram private server\ndone with status 36748hdeg \n checking for more data in device`",
        "`hacking....60% completed\nmore data found im target device\npreparing to download data\n process started with status 7y75hsgdt365ege56es \n status changed to up`",
        "`hacking....73% completed\n downloading data from device\n process completed with status 884hfhjh\nDownloading-0.1.tar.gz (9.3 kB)\nCollecting Data Packageseeing target\n lding chat tg-bot bruteforce finished\n creating pdf of chat`",
        "`hacking...88% completed\nall data from telegram private server downloaded\nterminal download sucessfull--with status jh3233fdg66y yr4vv.irh\n data collected from tg-bot\nTERMINAL:\n Bruteforce-Telegram-0.1.tar.gz (1.3)downloaded`",
        "`100%\n█████████HACKED███████████ `\n\n\n  `TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: `",
        "`User Data Upload Completed: Target's User Data Stored `",
        "`at downloads/victim/telegram-authuser.data.sql`",
    ]
    hecked = (
        f"`Targeted Account Hacked\n\nPague 69$ a {heckerman}` "
        "`Para remover o hack.`"
    )
    max_ani = len(animation_chars)
    for i in range(max_ani):
        await asyncio.sleep(2)
        await message.edit(animation_chars[i % max_ani])
    await message.edit(hecked)