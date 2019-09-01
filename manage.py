#!/usr/bin/env python
import os
import sys

import cbsettings
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seared_quail.settings")
    cbsettings.configure("seared_quail.settings.switcher")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
