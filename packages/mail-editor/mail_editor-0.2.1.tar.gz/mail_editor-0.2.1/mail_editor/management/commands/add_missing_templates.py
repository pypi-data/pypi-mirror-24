from django.core.management.base import BaseCommand

from ...helpers import find_template
from ... import settings


class Command(BaseCommand):
    help = "Create all new/missing templates (use this on every deploy)"

    def handle(self, *args, **options):
        choices = settings.get_choices()
        for key, name in choices:
            find_template(key)
