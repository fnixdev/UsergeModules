## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" Rss Feed Plugin to get regular updates from Feed """

from os import environ

from userge import config

RSS_CHAT_ID = [int(x) for x in environ.get("RSS_CHAT_ID", str(config.LOG_CHANNEL_ID)).split()]
