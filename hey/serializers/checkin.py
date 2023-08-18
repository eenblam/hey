
from rest_framework import serializers
from ..models import Friend

class CheckinSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

    class Meta:
        model = Friend
        fields = ['id', 'first_name', 'last_name', 'last_contact', 'status']
