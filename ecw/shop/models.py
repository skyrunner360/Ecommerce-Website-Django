from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    pub_date = models.DateField()
    category = models.CharField(max_length=100,default="")
    subcategory = models.CharField(max_length=100,default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name