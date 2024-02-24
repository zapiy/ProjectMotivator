import os
import sys


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
else:
    from django import setup
    setup()
