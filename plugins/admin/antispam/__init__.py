## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" setup antispam """

from userge.utils import secured_env

USERGE_ANTISPAM_API = secured_env("USERGE_ANTISPAM_API")
SPAM_WATCH_API = secured_env("SPAM_WATCH_API")


class Dynamic:
    ANTISPAM_SENTRY = True
