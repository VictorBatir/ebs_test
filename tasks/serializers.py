from rest_framework import serializers
from tasks.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'comment', 'created_at']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)