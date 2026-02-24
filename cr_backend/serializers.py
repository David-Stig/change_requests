from rest_framework import serializers

from .models import ChangeRequest, ChangeRequestLog, Ministry, System


class ChangeRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequestLog
        fields = ('id', 'action', 'performed_by', 'timestamp')
        read_only_fields = fields


class ChangeRequestSerializer(serializers.ModelSerializer):
    logs = ChangeRequestLogSerializer(many=True, read_only=True)
    system = serializers.PrimaryKeyRelatedField(queryset=System.objects.select_related('ministry'))
    ministry = serializers.PrimaryKeyRelatedField(queryset=Ministry.objects.all())

    class Meta:
        model = ChangeRequest
        fields = (
            'id',
            'title',
            'description',
            'created_by',
            'system',
            'ministry',
            'change_category',
            'status',
            'created_at',
            'updated_at',
            'logs',
        )
        read_only_fields = ('status', 'created_at', 'updated_at', 'logs')

    def validate(self, attrs):
        ministry = attrs.get('ministry', getattr(self.instance, 'ministry', None))
        system = attrs.get('system', getattr(self.instance, 'system', None))
        if ministry and system and system.ministry_id != ministry.id:
            raise serializers.ValidationError('System must belong to the selected ministry.')
        return attrs

    def validate_created_by(self, user):
        request = self.context['request']
        if not request.user.is_superuser and request.user != user:
            raise serializers.ValidationError('You can only create requests for yourself.')
        return user
