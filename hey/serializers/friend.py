from rest_framework import serializers
from ..models import Friend

class FriendSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    group = serializers.StringRelatedField()

    class Meta:
        model = Friend
        fields = ['id', 'first_name', 'last_name', 'birthday', 'phone', 'last_contact', 'group']
