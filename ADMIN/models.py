from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True,upload_to='assets/images')
    is_active = models.BooleanField(default=True)
    
class Product(models.Model):
	name = models.CharField(max_length=200)
	brand = models.CharField(max_length=200)
	price = models.FloatField()
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True,upload_to='assets/images')
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
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

