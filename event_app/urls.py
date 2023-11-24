from django.urls import path,include
from rest_framework import routers
from .views import EventViewSet,LocationViewSet,AddressViewSet,ReservationViewSet,ParticipantViewSet,TicketViewSet
router=routers.DefaultRouter()
router.register(r'events',EventViewSet,basename='events')
router.register(r'participants',ParticipantViewSet)
router.register(r'locations',LocationViewSet)
router.register(r'addresses',AddressViewSet)
router.register(r'reservations',ReservationViewSet)
router.register(r'tickets',TicketViewSet)
urlpatterns = [
    path('',include(router.urls))
]
