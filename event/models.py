from django.db import models

# Create your models here.
class events(models.Model):
    eventid = models.AutoField(primary_key=True)
    eventtitle=models.CharField(max_length=255,default="")
    eventdesc = models.TextField()
    eventstartdate=models.DateTimeField(blank = True)
    eventenddate=models.DateTimeField(blank = True)
    eventaddress=models.CharField(max_length=255)
    eventmap=models.CharField(max_length=255)
    eventemail=models.CharField(max_length=255)
    eventcontactno=models.CharField(max_length=255)
    eventtopics = models.TextField()
    eventspeacker1 = models.CharField(max_length=100,default="")
    eventimg=models.ImageField(upload_to='upload/',default="dummy.jpg")


    def __str__(self):
        return self.eventmap+ 'by'  + self.eventemail
