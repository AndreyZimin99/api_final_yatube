from django.urls import include, path
from rest_framework import routers

from api.views import (
    CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet,
)

router1_v1 = routers.DefaultRouter()
router2_v1 = routers.DefaultRouter()

router1_v1.register('posts', PostViewSet, basename='posts')
router1_v1.register('groups', GroupViewSet, basename='groups')
router1_v1.register('follow', FollowViewSet, basename='follow')
router2_v1.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router1_v1.urls)),
    path('v1/posts/<int:post_id>/', include(router2_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
