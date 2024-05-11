from django.db import models
class Book(models.Model):
    require = models.CharField(max_length=200,null=True)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.TimeField()
# Create your models here.
