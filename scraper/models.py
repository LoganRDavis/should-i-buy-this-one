from django.db import models

class Lookup(models.Model):
    createdDate = models.DateTimeField(auto_now_add=True)
    requestIp = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    resultUrl = models.CharField(max_length=2083)
    resultValue = models.IntegerField()

    def __str__(self):
        return self.name