from django.db import models
from django.utils import timezone
# Create your models here.
#define Django Enumeration
class EventCategory(models.TextChoices):
    CONFERENCE='CONF','Conference'
    SEMINAR='SEMI','Seminar'
    CONGRESS='CONG','Congress'
    COURSE='COUR','Course'
    CONCERT='CONC','Concert'
    FESTIVAL='FEST','Festival'
    EXHIBITION='EXHI','Exhibition'
    TOURNAMENT='TOUR','Tournament'
    OTHER='OTHE','Other'
class Location(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=1000, default="")
    address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zipCode = models.CharField(max_length=100, default="")
    attitude=models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude=models.DecimalField(max_digits=9, decimal_places=6, default=0)
    #this inner class is used to add metadata on the table
    #like table name, constraints (unique_together) index_together
    #some Meta class attributes are:
    #db_table, ordering, get_latest_by, verbose_name_plural, unique,....
    class Meta:
        db_table='locations'
        ordering=['name'] #the location tuples will be ordered by name in ascending order
        #ordering=['-name'] #the location tuples will be ordered by name in descending order
    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=1000, default="")
   # date = models.DateField(default=timezone.now())
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now=True,)
    poster = models.ImageField(upload_to='event_app/images/')
    url = models.URLField(blank=True)
    #relationship between Event and Location (*-1)
    location=models.ForeignKey(Location, on_delete=models.SET_NULL,null=True, blank=True)
    category=models.CharField(max_length=4,choices=EventCategory.choices,default=EventCategory.OTHER)

    class Meta:
        db_table='events'
        ordering=['name', 'date', 'time']
        #the tuple (name, date, time) can't be repeated
        unique_together=['name', 'date', 'time']
    def __str__(self):
        #return "name=%s,date=%s,time=%s" % (self.name, self.date, self.time)
        #return self.name+" "+str(self.date)+" "+str(self.time)
        return f'name={self.name},date={self.date},time={self.time}

class Participant(models.Model):
    firstName = models.CharField(max_length=100, default="")
    lastName = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=100, default="", unique=True)
    phone = models.CharField(max_length=100, default="")
    birthday = models.DateField(default=timezone.now())
    #relationship between Event and Participant (*-*)
    participation=models.ManyToManyField(Event, through='Reservation',through_fields=('participant','event'))
       
    class Meta:
        db_table='participants'
        ordering=['email']

    def __str__(self):
            return self.name

class Reservation(models.Model):
    event=models.ForeignKey(Event,on_delete=models.SET_NULL,null=True, blank=True)
    participant=models.ForeignKey(Participant,on_delete=models.SET_NULL,null=True, blank=True)
    date=models.DateField(auto_now_add=True)
    nbPlaces=models.PositiveIntegerField(default=1)
    reservationType=models.CharField(max_length=10,choices=[('VIP','Very important Person'),('STD','Standard')],default='STD')
    class Meta:
        db_table='reservations'
        unique_together=['event','participant']

class Ticket(models.Model):
    reservation=models.OneToOneField(Reservation,on_delete=models.CASCADE,null=True, blank=True)
    price=models.DecimalField(max_digits=9,decimal_places=2,default=0)

    class Meta:
        db_table='tickets'

    def __str__(self):
        #return self.reservation.event.name+" "+self.reservation.participant.email
        return f'reservation=({self.reservation.event.name},{self.reservation.event.date},{self.reservation.event.time}) - participant = {self.reservation.participant.email}'

class Organizer(models.Model):
    name=models.CharField(max_length=150,default="")
    email=models.EmailField(max_length=150,default="")
    phone=models.CharField(max_length=150,default="")
    #relationship between Organizer and Event (*-*)
    OrganizerEvents=models.ManyToManyField(Event)
    class Meta:
        db_table='organizers'
        ordering=['name']

    def __str__(self):
        return self.name

class Animator(models.Model):
    name=models.CharField(max_length=150,default="")
    email=models.EmailField(max_length=150,default="")
    phone=models.CharField(max_length=150,default="")
    url=models.URLField(max_length=100,null=True, blank=True)
    #relationship between Animator and Event (*-*)
    AnimatorEvents=models.ManyToManyField(Event)
    class Meta:
        db_table='animators'
        ordering=['name']

    def __str__(self):
        return self.name
        