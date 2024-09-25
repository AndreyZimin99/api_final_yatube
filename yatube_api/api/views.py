from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Comment, Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# @api_view(['GET', 'POST'])
# def api_comments(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(author=request.user, post=post)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     comments = post.comments.all()
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def api_comment_detail(request, post_id, comment_id):
#     comment = get_object_or_404(Comment, post=post_id, id=comment_id)
#     if request.method == 'GET':
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#     user = request.user
#     if comment.author != user:
#         raise PermissionDenied('Нельзя редактировать чужие комментарии!')
#     if request.method == 'PUT' or request.method == 'PATCH':
#         serializer = CommentSerializer(comment, data=request.data,
#                                        partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = self.kwargs['post_id']
        return Comment.objects.filter(post=post)

    def create(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     super().perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('following__username',)
