from django.db import models

class InfoSource(models.Model):
    CATEGORY_CHOICES = [
        ('blog', 'Blog'),
        ('website', 'Website'),
        ('news_portal', 'News Portal'),
        ('youtube', 'YouTube Channel'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    url = models.URLField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.CharField(max_length=255, help_text="Comma-separated tags")

    def __str__(self):
        return self.title
