from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    # Map frontend majorTags to backend major_tags
    majorTags = serializers.JSONField(source='major_tags', required=False)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'type', 'category', 'attendees', 'photo', 'majorTags']
