from .utils import get_course_outline_block_tree
from six import text_type

def check_if_user_completed_course(user, course_id):
    try:
        course_block_tree = get_course_outline_block_tree(user, text_type(course_id))
    except Exception as e:
        raise Exception("course_block_tree.ERROR: {}".format(str(e)))

    chapters = course_block_tree.get('children', None)

    if chapters is None:
        raise Exception("check_if_user_completed_course.ERROR: course {} has no chapters.".format(course_id))

    incomplete_count = 0
    for chapter in chapters:
        sequentials = chapter.get('children', [])
        for sequential in sequentials:
            block_format = sequential.get('format', None)
            is_graded = sequential.get('graded', False)
            is_complete = sequential.get('complete', False)
            if is_graded and block_format is not None and not is_complete:
                incomplete_count += 1

    not_complete = incomplete_count > 0
    return not not_complete
