"""
lms > djangoapps > course_api > blocks > serializers.py
Serializers for Course Blocks related return objects.
"""
from django.conf import settings
from rest_framework import serializers
from six import text_type
# from rest_framework.reverse import reverse

from lms.djangoapps.course_api.blocks.serializers import SUPPORTED_FIELDS


class BlockSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for single course block
    """
    def _get_field(self, block_key, transformer, field_name, default):
        """
        Get the field value requested.  The field may be an XBlock field, a
        transformer block field, or an entire tranformer block data dict.
        """
        value = None
        if transformer is None:
            value = self.context['block_structure'].get_xblock_field(block_key, field_name)
        elif field_name is None:
            try:
                value = self.context['block_structure'].get_transformer_block_data(block_key, transformer).fields
            except KeyError:
                pass
        else:
            value = self.context['block_structure'].get_transformer_block_field(block_key, transformer, field_name)

        return value if (value is not None) else default

    def to_representation(self, block_key):
        """
        Return a serializable representation of the requested block
        """
        # create response data dict for basic fields
        data = {
            'id': text_type(block_key),
            'block_id': text_type(block_key.block_id),
            # 'lms_web_url': reverse(
            #     'jump_to',
            #     kwargs={'course_id': text_type(block_key.course_key), 'location': text_type(block_key)},
            #     request=self.context['request'],
            # ),
            # 'student_view_url': reverse(
            #     'render_xblock',
            #     kwargs={'usage_key_string': text_type(block_key)},
            #     request=self.context['request'],
            # ),
        }

        # if settings.FEATURES.get("ENABLE_LTI_PROVIDER") and 'lti_url' in self.context['requested_fields']:
        #     data['lti_url'] = reverse(
        #         'lti_provider_launch',
        #         kwargs={'course_id': text_type(block_key.course_key), 'usage_id': text_type(block_key)},
        #         request=self.context['request'],
        #     )

        # add additional requested fields that are supported by the various transformers
        for supported_field in SUPPORTED_FIELDS:
            if supported_field.requested_field_name in self.context['requested_fields']:
                field_value = self._get_field(
                    block_key,
                    supported_field.transformer,
                    supported_field.block_field_name,
                    supported_field.default_value,
                )
                if field_value is not None:
                    # only return fields that have data
                    data[supported_field.serializer_field_name] = field_value

        if 'children' in self.context['requested_fields']:
            children = self.context['block_structure'].get_children(block_key)
            if children:
                data['children'] = [text_type(child) for child in children]

        return data


class BlockDictSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer that formats a BlockStructure object to a dictionary, rather
    than a list, of blocks
    """
    root = serializers.CharField(source='root_block_usage_key')
    blocks = serializers.SerializerMethodField()

    def get_blocks(self, structure):
        """
        Serialize to a dictionary of blocks keyed by the block's usage_key.
        """
        return {
            text_type(block_key): BlockSerializer(block_key, context=self.context).data
            for block_key in structure
        }
