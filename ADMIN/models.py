from email.mime import image
from email.policy import default
from unicodedata import name
from django.db import models



class Category(models.Model):
	name = models.CharField(max_length=100)
	sub_categories = models.ManyToManyField("self")
	is_active = models.BooleanField(default=True)
	
	@staticmethod
	def get_all_categories():
		return Category.objects.all()

	def __str__(self):
		return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
	
	
    
class Product(models.Model):
	name = models.CharField(max_length=200)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	price = models.FloatField()
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True,upload_to='assets/images')
	category= models.ManyToManyField(Category)
	quantity = models.IntegerField(default=1)
 
	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class Images(models.Model):
	image = models.ImageField(null=True, blank=True,upload_to='assets/images')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.image.url

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Offers(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    offer = models.IntegerField()
    offer_type = models.CharField(max_length=200, null=True, blank=True, default='product')
    start_date = models.DateField()
    end_date = models.DateField()
    max_value = models.IntegerField(default=0)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name
    
class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.IntegerField()
    start_date = models.DateField()
    min_amount = models.IntegerField(default=0)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
	

    def __str__(self):
        return self.code