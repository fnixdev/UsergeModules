## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" manage your gdrive """

import logging
import os

from userge.utils import secured_env

logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)

G_DRIVE_CLIENT_ID = secured_env("G_DRIVE_CLIENT_ID")
G_DRIVE_CLIENT_SECRET = secured_env("G_DRIVE_CLIENT_SECRET")
G_DRIVE_PARENT_ID = os.environ.get("G_DRIVE_PARENT_ID")
G_DRIVE_INDEX_LINK = os.environ.get("G_DRIVE_INDEX_LINK")
G_DRIVE_IS_TD = bool(os.environ.get("G_DRIVE_IS_TD"))
