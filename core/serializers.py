from rest_framework_mongoengine.serializers import DocumentSerializer

from core.models import UserMapping


class UserMappingSerializer(DocumentSerializer):
    class Meta:
        model = UserMapping
        depth = 1
