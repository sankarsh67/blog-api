from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True,blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft','Draft'),
        ('published','Published'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=200,blank=True)
    status =  models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_at']
        
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Commment by {self.author} on {self.post}'
    class Meta:
        ordering = ['created_at']
        
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} liked {self.post}'
    class Meta:
        unique_together = ['post','user']