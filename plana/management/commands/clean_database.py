import pathlib

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _


class Command(BaseCommand):
    help = _("Resets database structure and content.")

    def handle(self, *args, **options):
        try:
            call_command("flush")
            call_command("migrate")
            apps_fixtures = list(pathlib.Path().glob("plana/apps/*/fixtures/*.json"))
            call_command("loaddata", *apps_fixtures)
            libs_fixtures = list(pathlib.Path().glob("plana/libs/*/fixtures/*.json"))
            call_command("loaddata", *libs_fixtures)
            self.stdout.write(self.style.SUCCESS(_("Database regenerated.")))

        except Exception as e:
            self.stdout.write(self.style.ERROR("Error : %s" % e))
