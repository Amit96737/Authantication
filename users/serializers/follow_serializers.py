from rest_framework import serializers
from users.models.follow import Follow
from users.serializers.custom import CustomSerializer

class UserFollowSerializer(CustomSerializer, serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("follower", "following",)
        read_only_fields = ["follower"]