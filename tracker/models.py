from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify


class Skill(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="goals",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rank = models.CharField(max_length=10, blank=True)
    level = models.IntegerField(default=1)
    slug = models.SlugField(default='', null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Skill, self).save(*args, **kwargs)

class Goal(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skills",
        null=True,
        blank=True
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="goals"
    )
    text = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.text} ({self.skill})"