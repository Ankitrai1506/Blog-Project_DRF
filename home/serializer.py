from rest_framework import serializers
from .models import Blog, Comment, Like
from account.serializer import LoginSerializer

class BlogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model= Blog
        exclude= ['updated_at','user']


class CommentSerializer(serializers.ModelSerializer):
    #user= serializers.StringRelatedField(read_only= True)
    commented_by= serializers.ReadOnlyField(source= 'user.username')


    class Meta:
        model= Comment
        fields= ['uid', 'blog_id', 'comment','commented_by']


class LikeSerializer(serializers.ModelSerializer):
    liked_by= serializers.ReadOnlyField(source= 'user.username')
    class Meta:
        model= Like
        fields= ['user', 'blog','liked_by']