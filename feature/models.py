from django.db import models

class Feature(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=80, blank=True, help_text='Font Awesome class, e.g., fa-coffee')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title
