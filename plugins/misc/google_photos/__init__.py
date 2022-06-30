## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" Google Photos """

import os

from userge.utils import secured_env

G_PHOTOS_CLIENT_ID = secured_env("G_PHOTOS_CLIENT_ID") or secured_env("G_DRIVE_CLIENT_ID")

G_PHOTOS_CLIENT_SECRET = secured_env("G_PHOTOS_CLIENT_SECRET") or \
                         secured_env("G_DRIVE_CLIENT_SECRET")

G_PHOTOS_AUTH_TOKEN_ID = int(os.environ.get("G_PHOTOS_AUTH_TOKEN_ID") or 0)
