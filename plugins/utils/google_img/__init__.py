## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" google image search """

import os

from userge.utils import secured_env

GCS_API_KEY = secured_env("GCS_API_KEY")
GCS_IMAGE_E_ID = os.environ.get("GCS_IMAGE_E_ID")
