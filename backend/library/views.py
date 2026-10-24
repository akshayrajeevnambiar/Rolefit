"""CRUD for the signed-in account's own rows.

get_queryset filters by that account. A row owned by someone else is
a 404, the same answer as a missing row, so guessing an id does not
reveal that the row exists.
"""

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from library.models import JobDescription, Resume
from library.serializers import JobDescriptionSerializer, ResumeSerializer


class OwnedViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)


class ResumeViewSet(OwnedViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class JobDescriptionViewSet(OwnedViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
