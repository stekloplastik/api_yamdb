from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateUserViewSet, UserEdit, get_jwt_token,
                    send_confirmation_code)

router = DefaultRouter()
router.register('users', CreateUserViewSet)

urlpatterns = [
    path('auth/email/', send_confirmation_code),
    path('auth/token/', get_jwt_token),
    path('users/me/', UserEdit.as_view()),
    path('', include(router.urls)),
]