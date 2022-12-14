from rest_framework import serializers
from .models import App, Run

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'image', 'envs', 'command']

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['id', 'status', 'running_time', 'name', 'image', 'envs', 'command', 'app']