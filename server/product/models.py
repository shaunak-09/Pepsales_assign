from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=5)
    description = models.TextField(null=True)
    category = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name





