from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=300)
    phone = models.IntegerField()
    password = models.CharField(max_length=500)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name
