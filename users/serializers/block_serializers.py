from rest_framework import serializers
from users.models.block_user import BlockUser
from users.serializers.custom import CustomSerializer

class BlockUserSerializers(CustomSerializer, serializers.ModelSerializer):
    class Meta:
        model = BlockUser
        fields = ("blocked",)