from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post, User


def get_following(validated_data):
    following_username = validated_data.pop('following')
    following_user = User.objects.get(username=following_username)
    return following_user


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.CharField()

    class Meta:
        fields = '__all__'
        model = Follow

    def validate_following(self, value):
        follower = self.context['request'].user
        following = User.objects.get(username=value)
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем не найден.")
        if follower == following:
            raise serializers.ValidationError(
                "Вы не можете подпитсаться на себя.")
        if Follow.objects.filter(
            user=follower,
            following=following,
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя.")
        return value

    def create(self, validated_data):
        following_user = get_following(validated_data)
        user = self.context['request'].user
        return Follow.objects.create(user=user, following=following_user)

    def update(self, instance, validated_data):
        following_user = get_following(validated_data)
        instance.following = following_user
        instance.save()
        return instance
