from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    head0 = models.CharField(max_length=500)
    chead0 = models.CharField(max_length=5000,default='abc')
    head1 = models.CharField(max_length=500)
    chead1 = models.CharField(max_length=5000,default='abc')
    head2 = models.CharField(max_length=500)
    chead2 = models.CharField(max_length=5000,default='abc')
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.title
