import logging
log = logging.getLogger(__name__)

from django.contrib.auth.models import User
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from django.core.management.base import BaseCommand, CommandError

from util.milestones_helpers import fulfill_course_milestone


class Command(BaseCommand):
    help = 'Manually give learner milestone for prerequisite course.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--course',
            type=str,
            help='set filter for course_id',
        )
        parser.add_argument(
            '-u',
            '--username',
            type=str,
            help='set user to give milestone',
        )

    def handle(self, *args, **options):
        course_id = options.get('course', None)
        username = options.get('username', None)

        if course_id is None or username is None:
            raise CommandError("Arguments course_id -c --course and username -u --user are required.")

        try:
            course_key = CourseKey.from_string(course_id)
        except Exception as e:
            raise CommandError("Course does not exist: {}".format(str(e)))

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError("User does not exist: {}".format(username))

        try:
            fulfill_course_milestone(course_key, user=user)
        except Exception as e:
            raise CommandError("Error in giving milestone.".format(str(e)))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully gave learner milestone."))
