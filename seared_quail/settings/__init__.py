"""
Django settings for seared_quail project.
:Created: 4 May 2015
:Author: Lucas Connors

"""

import os

from cbsettings import switcher

from seared_quail.settings.base import BaseSettings
from seared_quail.settings.prod import ProdSettings


stage = os.environ.get("SEARED_QUAIL_STAGE", "dev")
switcher.register(BaseSettings, stage == "dev")
switcher.register(ProdSettings, stage == "production")
