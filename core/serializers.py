from rest_framework import serializers

from .models import ChangeRequest, Functionality, Ministry, System, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class MinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministry
        fields = '__all__'


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'


class FunctionalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Functionality
        fields = '__all__'


class ChangeRequestSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)

    class Meta:
        model = ChangeRequest
        fields = '__all__'
