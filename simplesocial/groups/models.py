from django.db import models
from django.utils.text import slugify

import misaka

# Allows to call things of the current user session
from django.contrib.auth import get_user_model
User = get_user_model()

# Allows usin custom template tags
from django import template
register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',
                                        blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,*kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'self':self.slug})

    class Meta:
        ordering = ['name']

class GroupMember(model.Model):
    group = models.ForeignKey(Group,related_name='memberships')
    user = models.ForeignKey(User,related_name='user_group')

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ('group','user')
