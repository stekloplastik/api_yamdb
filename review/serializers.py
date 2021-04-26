from rest_framework import serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        if (self.context.get('request').method == 'POST'
            and Review.objects.filter(title_id=title_id,
                                      author_id=author.id).exists()):
            raise serializers.ValidationError(
                {'detail': 'Кыш, ты уже оставлял отзыв'})
        return data

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['author', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ['author', 'pub_date']
