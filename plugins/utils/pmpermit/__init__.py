## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" setup auto pm message """

from pyrogram import filters

ALLOWED_CHATS = filters.chat([])


class Dynamic:
    ALLOW_ALL_PMS = True
    IS_INLINE = True
