from rest_framework import serializers
from .models import Event, Participant,Address,Location, Reservation,Ticket
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields='__all__'

        
class EventSerializer(serializers.ModelSerializer):
    #location=LocationSerializer()
    class Meta:
        model=Event
        fields='__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    participation=EventSerializer(many=True)
    class Meta:
        model=Participant
        fields='__all__'

class  ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields='__all__'

class Organizer(serializers.ModelSerializer):
    class Meta:
        model=Participant
        fields='__all__'