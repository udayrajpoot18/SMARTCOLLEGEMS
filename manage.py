#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main():
    # Add the college_management directory to sys.path so 'apps' is importable
    BASE = Path(__file__).resolve().parent / 'college_management'
    if str(BASE) not in sys.path:
        sys.path.insert(0, str(BASE))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_management.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
