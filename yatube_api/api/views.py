from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from api.permissions import OwnerOrReadOnly, ReadOnly
from posts.models import Group, Post


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class BaseViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class PostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(BaseViewSet):
    serializer_class = CommentSerializer
    permission_classes = permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return user.followers.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
