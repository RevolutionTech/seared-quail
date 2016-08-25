"""
Django settings for seared_quail project.
:Created: 4 May 2015
:Author: Lucas Connors

"""

import os

from cbsettings import switcher

from seared_quail.settings.travis import TravisSettings


SETTINGS_DIR = os.path.dirname(__file__)

dev_settings_exists = os.path.isfile(os.path.join(SETTINGS_DIR, 'dev.py'))
prod_settings_exists = os.path.isfile(os.path.join(SETTINGS_DIR, 'prod.py'))

switcher.register(TravisSettings, 'TRAVIS' in os.environ)

if dev_settings_exists:
    from seared_quail.settings.dev import DevSettings
    switcher.register(DevSettings, dev_settings_exists and not prod_settings_exists)

if prod_settings_exists:
    from seared_quail.settings.prod import ProdSettings
    switcher.register(ProdSettings, prod_settings_exists)
