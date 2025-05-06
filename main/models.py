from django.db import models

# Create your models here.
class Blog(models.Model):

     STATUS_CHOICES = [
          ('draft', '임시저장'),
          ('published', '발행'),
          ]
     
     title = models.CharField(max_length=50)
     writer = models.CharField(max_length=30)
     content = models.TextField()
     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
     created_at = models.DateTimeField()
     image = models.ImageField(upload_to="blog/", blank=True, null=True)

     def __str__(self):
          return self.title
     
     def summary(self) :
          return self.content[:20]
