from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    class Tiers(models.IntegerChoices):
        ONE = 1, 'Student'
        TWO = 2, 'Teacher'
        THREE = 3, 'General'

  #  TIER_CHOICES = [
   #     (1, 'General'),
    #    (2, 'Student'),
     #   (3, 'Teacher'),
    #]

    title = models.CharField(max_length=100)
    description = models.TextField()
    tier_level = models.IntegerField(choices=Tiers.choices, default=1)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#todo filter