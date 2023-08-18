from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from ..models import Friend
from ..serializers import CheckinSerializer


class CheckinsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    serializer_class = CheckinSerializer

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user.id).select_related('group')

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Returns a list of friends who are overdue for contact."""
        friends = Friend.objects.filter(user=self.request.user.id).select_related('group')
        overdue = [friend for friend in friends if friend.is_overdue()]
        serializer = CheckinSerializer(overdue, many=True)
        return Response(serializer.data)
