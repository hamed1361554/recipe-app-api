from unittest.mock import patch

import django.db.utils
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    """Command Tests"""

    def test_wait_for_db_ready(self):
        """Test that db is ready"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test that db delays to start"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
