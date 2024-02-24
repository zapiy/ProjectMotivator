#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging


def main():
    """Run administrative tasks.""" 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] - %(name)s - [%(filename)s(%(lineno)d) in %(funcName)s] => %(message)s"
    )
    
    args = sys.argv
        
    if len(args) <= 1:
        args.append('runserver')
    execute_from_command_line(args)


if __name__ == '__main__':
    main()
