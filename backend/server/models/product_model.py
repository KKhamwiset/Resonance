from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, default="DefaultType")
    brand = models.CharField(max_length=255, default="DefaultBrand")
    connections = models.CharField(max_length=255, default="DefaultConnections")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
