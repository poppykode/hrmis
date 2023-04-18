from django.db import models
from django.conf import settings
from datetime import date
from project.models import Project

User = settings.AUTH_USER_MODEL

# Create your models here.
class Task(models.Model):
    STATUS = (('new','New'),('work in progress','Work In Progress'),('completed','Completed'))
    PRIORITY = (('','Select a Priority'),('low','Low'),('medium','Medium'),('high','High'))
    project = models.ForeignKey(Project, related_name='task_project',on_delete=models.CASCADE)
    resource = models.ForeignKey(User, related_name='task_resource',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    percentage_complition = models.PositiveIntegerField(default=0,null=True,blank=True)
    status = models.CharField(max_length=100,choices=STATUS,default='new',null=True,blank=True)
    priority = models.CharField(max_length=100, choices=PRIORITY)
    start_date= models.DateField()
    end_date = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def is_past_due(self):
        return date.today() > self.end_date

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-timestamp", ]


