## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" setup gban """

from os import environ
from typing import Dict

WHITE_CACHE: Dict[int, str] = {}
FBAN_CHAT_ID = int(environ.get("FBAN_CHAT_ID") or 0)


async def is_whitelist(user_id: int) -> bool:
    return user_id in WHITE_CACHE
