from django.db import models

#Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    timeStamp = models.DateTimeField(blank = True)
    slug = models.CharField(max_length=130,default='')
    img=models.ImageField(upload_to='upload/',default="dummy.jpg")
    def __str__(self):
        return self.title
    


    def __str__(self):
        return self.title + 'by'  + self.author
class Categroypost(models.Model):
    catPostId=models.AutoField(primary_key=True)
    catTitle=models.CharField(max_length=100,default="Category title")
    def __str__(self):
        return self.catTitle
    