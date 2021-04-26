from django.urls import path, include
from rest_framework import routers

from .views import ReviewsViewSet, CommentsViewSet


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='ReviewsViewSet'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='CommentsViewSet'
)

urlpatterns = [
    path('v1/', include(router.urls))
]
