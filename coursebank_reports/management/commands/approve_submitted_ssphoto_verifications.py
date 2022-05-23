"""
Django admin commands related to verify_student
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from lms.djangoapps.verify_student.models import SoftwareSecurePhotoVerification

import datetime

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This method attempts to verify users who have submitted photos.
    Example usage:
    $ ./manage.py lms approve_submitted_ssphoto_verifications
    """
    help = 'Verifies users who have submitted photo verifications.'

    def handle(self, *args, **options):
        """
        Verifies users who have SoftwareSecurePhotoVerifications that have *submitted* status.
        """
        
        # IBALIK ITO SA 
        # submitted_verifications = SoftwareSecurePhotoVerification.objects.filter(
        #     status = 'ready'
        # )
        submitted_verifications = SoftwareSecurePhotoVerification.objects.exclude(
            status = 'approved'
        )

        if not submitted_verifications.exists():
            msg = "No verifications to approve."
            log.info(msg)
            return msg

        for submitted_verification in submitted_verifications:
            submitted_verification.status = 'approved'
            submitted_verification.updated_at = datetime.datetime.now()
            submitted_verification.save()

        msg = "Finished approving photo verifications."
        log.info(msg)
        return msg
