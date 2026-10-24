from rest_framework.routers import SimpleRouter

from library.views import JobDescriptionViewSet, ResumeViewSet

router = SimpleRouter()
router.register("resumes", ResumeViewSet, basename="resume")
router.register("job-descriptions", JobDescriptionViewSet, basename="job-description")

urlpatterns = router.urls
