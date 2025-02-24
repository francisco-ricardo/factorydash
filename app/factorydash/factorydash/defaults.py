import os
import sys
import django


def default_path_definition() -> None:
    # Set up Django environment
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorydash.settings")
    django.setup()

# EOF
