from rest_framework import serializers
from .models import App, Run

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'image', 'envs', 'command']

    def validate_name(self, name):
        if len(name) < 4:
            raise serializers.ValidationError('name can not be less than 4 characters')
        return name

    def validate_command(self, command):
        if command != None:
            if command.startswith('#'):
                raise serializers.ValidationError('not an acceptable command')
        return command

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['id', 'status', 'running_time', 'name', 'image', 'envs', 'command', 'app', 'cont_id']
