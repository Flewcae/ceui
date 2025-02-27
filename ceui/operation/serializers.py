from rest_framework import serializers
from .models import Task, ReviseStack, FileStack, ImageStack, ReportStack
from user.models import CustomUser
from chat.models import Chat


class FileStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileStack
        fields = '__all__'


class ImageStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStack
        fields = '__all__'


class ReviseStackSerializer(serializers.ModelSerializer):
    files = FileStackSerializer(many=True, read_only=True)
    images = ImageStackSerializer(many=True, read_only=True)

    class Meta:
        model = ReviseStack
        fields = '__all__'


class ReportStackSerializer(serializers.ModelSerializer):
    files = FileStackSerializer(many=True, read_only=True)
    images = ImageStackSerializer(many=True, read_only=True)

    class Meta:
        model = ReportStack
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    revises = ReviseStackSerializer(many=True, read_only=True)
    reports = ReportStackSerializer(many=True, read_only=True, source="reportstack_set")
    appointeds = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    appointer = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = Task
        fields = '__all__'
