# REST Framework
from rest_framework import serializers

# Models
from adventure import models

class JourneySerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()

class EndJourneySerializer(serializers.ModelSerializer):
    """End ride serializer."""

    # current_time = serializers.DateTimeField()

    class Meta:
        """Meta class."""

        model = models.Journey
        fields = ('vehicle', 'start', 'end')   
        read_only_fields = ('vehicle', 'start')

    def validate_end(self, data):
        """Verify journey has indeed started."""
        journey = self.context['view'].get_object()
        if data < journey.start:
            raise serializers.ValidationError('Journey has not started yet')
        return data