#!/usr/bin/env python
import os
import sys
import warnings

from django.utils.deprecation import RemovedInDjango20Warning

# Propagate warnings as errors when running tests
if len(sys.argv) >= 2 and sys.argv[1] == 'test':
    warnings.filterwarnings('error')
    # Filter warnings that are a result of dependencies
    # They can be removed once the dependency fixes the issue
    django20warnings = [
        # django-ordered-model: https://github.com/bfirsh/django-ordered-model/issues/99
        (
            'Deprecated allow_tags attribute used on field move_up_down_links\. '
            'Use django\.utils\.safestring\.format_html\(\), format_html_join\(\), or mark_safe\(\) instead\.'
        ),

        # django-ordered-model: https://github.com/bfirsh/django-ordered-model/issues/100
        'Importing from django\.core\.urlresolvers is deprecated in favor of django\.urls\.',
    ]
    for django20warning in django20warnings:
        warnings.filterwarnings('ignore', category=RemovedInDjango20Warning, message=django20warning)

import cbsettings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seared_quail.settings")
    cbsettings.configure('seared_quail.settings.switcher')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
