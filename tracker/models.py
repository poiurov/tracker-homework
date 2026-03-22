from django.db import models
from django.conf import settings


class Skill(models.Model):
    name = models.CharField(max_length=100)  # например "Python", "Английский", "Физуха"

    # можно добавить: description, level, user и т.д. позже

    def __str__(self):
        return self.name


class Goal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='владелец'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='навык'
    )

    text = models.CharField(
        max_length=200,
        verbose_name='основной текст цели'
    )

    description = models.TextField(
        blank=True,
        verbose_name='подробное описание'
    )

    done = models.BooleanField(
        default=False,
        verbose_name='выполнено'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создана'
    )

    class Meta:
        verbose_name = 'цель'
        verbose_name_plural = 'цели'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text} ({self.skill})"