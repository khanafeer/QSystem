from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.forms.models import model_to_dict

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=45)
    start = models.PositiveIntegerField(default=0)
    end = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class Terminal(models.Model):
    name = models.CharField(max_length=150)
    details = models.TextField(null=True,blank=True)
    service = models.ForeignKey(Service,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class TerminalUser(models.Model):
    terminal = models.ForeignKey(Terminal,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('terminal','user',)
    def __str__(self):
        return self.terminal.name + " " + self.user.username

class ServiceUser(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('service', 'user',)

    def __str__(self):
        return self.service.name + " " + self.user.username


class QueAbc(models.Model):
    num = models.PositiveIntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal,null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

    date_join = models.DateTimeField(null=True,blank=True)
    date_call = models.DateTimeField(null=True,blank=True)
    date_end = models.DateTimeField(null=True,blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.num)

class QueLog(QueAbc):
    pass


class QueueManager(models.Manager):

    def enqueue(self,*args,**kwargs):
        self.create(**kwargs)

    def dequeue(self,service):
        if not self.is_empty():
            first = self.first(service)
            first_data = first.__dict__
            first.delete()
            return first_data
        else:
            return False

    def first(self,service):
        first = self.get_queryset().filter(service=service).first()
        return first

    def is_empty(self):
        return len(self.get_queryset().all()) ==0

    def length(self,service):
        return len(self.get_queryset().filter(service=service))

    def last(self,service):
        last = self.get_queryset().filter(service=service).last()
        return last


class Queue(models.Model):
    num = models.PositiveIntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_join = models.DateTimeField(auto_now=True)
    objects = QueueManager()


    def __str__(self):
        return self.service.name + " client : " +str(self.num)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
