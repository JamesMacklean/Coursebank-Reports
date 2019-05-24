from django.core.management.base import BaseCommand

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This management command generates reports.
    """
    help = 'This management command generates reports.'

    def handle(self, *args, **kwargs):
        msg = 'Successfully...'
        log.info(msg)
