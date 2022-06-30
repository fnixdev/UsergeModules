## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" check user's info """

from userge.utils import secured_env


USERGE_ANTISPAM_API = secured_env("USERGE_ANTISPAM_API")
SPAM_WATCH_API = secured_env("SPAM_WATCH_API")
