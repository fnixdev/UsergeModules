## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" manage your group """

from typing import Dict, List

ENABLED_CHATS: List[int] = []
BAN_CHANNELS: List[int] = []  # list of chats which enabled ban_mode
ALLOWED: Dict[int, List[int]] = {}  # dict to store chat ids which are allowed to chat as channels
