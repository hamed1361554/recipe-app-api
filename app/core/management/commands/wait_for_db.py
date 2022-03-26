import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Wait for DB command"""

    def handle(self, *args, **options):
        """Handles wait for db command."""

        self.stdout.write('Waiting for database to come alive ...')

        db_connection = None
        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError as error:
                self.stdout.write(f'Database not ready yet, here is some clue: [{error}]')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Uh, finally it's coming to some good news about database: STARTED"))
