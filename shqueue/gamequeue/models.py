from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import math

class GameQueue(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=False)
    capacity = models.IntegerField(default=1)
    seconds_per_person = models.IntegerField()

    def __str__(self):
        return self.name + (" (" + str(self.queued.count()) + " i kø, ventetid: " + str(self.wait_time_minutes) + " min)" if self.active else " (inaktiv)")

    @property
    def queued(self):
        return QueuedPerson.objects.filter(queue=self, playing_at=None).order_by('queued_at')

    @property
    def currently_playing(self):
        return QueuedPerson.objects.filter(queue=self, finished_at=None).exclude(playing_at=None).order_by('playing_at')

    @property
    def people(self):
        return QueuedPerson.objects.filter(queue=self, finished_at=None).order_by('queued_at')

    @property
    def wait_time_minutes(self):
        return math.ceil(((min([(self.seconds_per_person - (timezone.now() - person.playing_at).total_seconds()) or 0 for person in self.currently_playing]) if len(self.currently_playing) is self.capacity else 0) + (self.seconds_per_person * self.queued.count() / self.capacity)) / 60)

    @property
    def info_text(self):
        if not self.active: return "Inaktiv"
        if self.queued.count() is 0 and self.currently_playing.count() is 0: return "Klar til å spille"
        return str(len(self.currently_playing)) + " spiller, " + str(len(self.queued)) + " venter<br/>Ventetid: " + str(self.wait_time_minutes) + " min"

class QueuedPerson(models.Model):
    name = models.CharField(max_length=200)
    queue = models.ForeignKey(GameQueue, on_delete=models.CASCADE, related_name='queued_people')

    queued_at = models.DateTimeField(auto_now_add=True)
    queued_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='queued')
    playing_at = models.DateTimeField(null=True)
    playing_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='playing')
    finished_at = models.DateTimeField(null=True)
    finished_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='finished')

    def __str__(self):
        return self.name
