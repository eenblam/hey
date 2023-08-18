from rest_framework.viewsets import ModelViewSet

from ..models import Friend
from ..serializers import FriendSerializer

class FriendsViewSet(ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user.id).select_related('group')

    def perform_create(self, serializer):
        serializer.data.user = self.request.user
        super(FriendsViewSet, self).perform_create(serializer)
