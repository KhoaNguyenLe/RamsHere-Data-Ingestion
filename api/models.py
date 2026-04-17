from django.db import models

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('live', 'Live'),
        ('upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    category = models.CharField(max_length=100)
    attendees = models.IntegerField(null=True, blank=True, default=0)
    photo = models.URLField(null=True, blank=True)
    major_tags = models.JSONField(null=True, blank=True, default=list)

    def __str__(self):
        return self.title
