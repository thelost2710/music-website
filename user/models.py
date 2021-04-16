from django.db import models
from django.contrib.auth.models import User
class Album(models.Model):
	UserID = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	Name = models.CharField(max_length=100)
	Description = models.TextField()
	Public = models.BooleanField()
	Like = models.IntegerField(default = 0)
	Price = models.IntegerField()
	Image = models.ImageField(null=True, blank=True)
	def __str__(self):
		return self.Name
class Cart(models.Model):
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	AlbumID = models.ForeignKey(Album, default=None, on_delete=models.CASCADE)
class Category(models.Model):
	Name = models.CharField(max_length=100)
	Description = models.TextField()
	def __str__(self):
		return self.Name
class Music(models.Model):
	CategoryID = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
	Name = models.CharField(max_length=100)
	Singer = models.CharField(max_length=100)
	Description = models.TextField()
	Like = models.IntegerField(default = 0)
	Price = models.IntegerField()
	Image = models.ImageField(null=True, blank=True)
	Music = models.FileField(upload_to='music/')
	def __str__(self):
		return self.Name
class Group_music(models.Model):
	Music_ID = models.ForeignKey(Music, default=None, on_delete=models.CASCADE)
	AlbumID = models.ForeignKey(Album, default=None, on_delete=models.CASCADE)
class Rate_music(models.Model):
	Music_ID = models.ForeignKey(Music, default=None, on_delete=models.CASCADE)
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	isLike = models.BooleanField()
class Rate_album(models.Model):
	AlbumID = models.ForeignKey(Album, default=None, on_delete=models.CASCADE)
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	isLike = models.BooleanField()
class Bill(models.Model):
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	Bill = models.ImageField(null=True, blank=True)
	Shipped = models.BooleanField()
	Date = models.DateTimeField(auto_now_add = True)
class UserInfotmation(models.Model):
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	Name = models.CharField(max_length=100)
	DateofBirth = models.CharField(max_length=100)
	Gender = models.CharField(max_length=100)
	Address = models.CharField(max_length=500)
	Phone = models.IntegerField()

